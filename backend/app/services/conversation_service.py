from collections.abc import AsyncGenerator

from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.schemas.chat import ChatMessage

from app.services.llm.provider import LLMProvider
from app.services.rag.rag_service import prepare_rag_question

from app.logging.logger import logger
from app.logging.context import get_request_id

from app.core.exceptions import ConversationNotFoundError
from app.schemas.llm import ToolResult

from app.tools.factory import (
    create_tool_executor,
    create_tool_registry,
)

MAX_TOOL_CALLS = 5

class ConversationService:

    def __init__(
        self,
        db,
        llm_provider: LLMProvider,
    ):
        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

        self.llm_provider = llm_provider

        self.tool_registry = create_tool_registry()

        self.tool_executor = create_tool_executor(
            self.tool_registry
        )

    # ---------------------------------------------------------
    # Normal chat
    # ---------------------------------------------------------

    def chat(
        self,
        conversation_id: str,
        message: str,
    ) -> tuple[str, list[dict]]:

        request_id = get_request_id()

        conversation = self.conversation_repository.get(
            conversation_id
        )

        if conversation is None:
            raise ConversationNotFoundError()

        logger.info(
            "chat_request request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # -----------------------------------------------------
        # Save user message
        # -----------------------------------------------------

        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        # -----------------------------------------------------
        # Load conversation history
        # -----------------------------------------------------

        history = self.message_repository.get_messages(
            conversation_id
        )

        messages = [
            ChatMessage(
                role=m.role,
                content=m.content,
            )
            for m in history
        ]

        # -----------------------------------------------------
        # Retrieve relevant knowledge
        # -----------------------------------------------------

        rag_result = prepare_rag_question(
            question=message,
            top_k=5,
        )

        rag_prompt = rag_result["prompt"]
        sources = rag_result["sources"]

        logger.info(
            "rag_context_prepared "
            "request_id=%s "
            "conversation_id=%s "
            "sources=%d",
            request_id,
            conversation_id,
            len(sources),
        )

        # -----------------------------------------------------
        # Replace current user message with RAG-aware prompt
        # -----------------------------------------------------

        messages[-1] = ChatMessage(
            role="user",
            content=rag_prompt,
        )

        # -----------------------------------------------------
        # LLM
        # -----------------------------------------------------

        answer = self._generate_with_tools(
        messages
        )

        logger.info(
            "llm_response_received "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # -----------------------------------------------------
        # Save assistant response
        # -----------------------------------------------------

        self.message_repository.save(
            conversation_id,
            "assistant",
            answer,
        )

        logger.info(
            "assistant_message_saved "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        return answer, sources

    # ---------------------------------------------------------
    # Streaming chat
    # ---------------------------------------------------------

    async def stream_chat(
        self,
        conversation_id: str,
        message: str,
    ) -> AsyncGenerator[str, None]:

        request_id = get_request_id()

        conversation = self.conversation_repository.get(
            conversation_id
        )

        if conversation is None:

            logger.warning(
                "stream_conversation_not_found "
                "request_id=%s conversation_id=%s",
                request_id,
                conversation_id,
            )

            raise ConversationNotFoundError()

        logger.info(
            "stream_chat_request "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # -----------------------------------------------------
        # Save user message
        # -----------------------------------------------------

        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        # -----------------------------------------------------
        # Load history
        # -----------------------------------------------------

        history = self.message_repository.get_messages(
            conversation_id
        )

        messages = [
            ChatMessage(
                role=m.role,
                content=m.content,
            )
            for m in history
        ]

        # -----------------------------------------------------
        # Retrieve relevant knowledge
        # -----------------------------------------------------

        rag_result = prepare_rag_question(
            question=message,
            top_k=5,
        )

        rag_prompt = rag_result["prompt"]
        sources = rag_result["sources"]

        logger.info(
            "rag_context_prepared "
            "request_id=%s "
            "conversation_id=%s "
            "sources=%d",
            request_id,
            conversation_id,
            len(sources),
        )

        messages[-1] = ChatMessage(
            role="user",
            content=rag_prompt,
        )

        # -----------------------------------------------------
        # Stream LLM response
        # -----------------------------------------------------

        response_chunks = []

        try:

            async for chunk in self.llm_provider.stream(
                messages
            ):

                response_chunks.append(chunk)

                yield chunk

            # -------------------------------------------------
            # Reconstruct complete response
            # -------------------------------------------------

            answer = "".join(response_chunks)

            logger.info(
                "stream_llm_response_complete "
                "request_id=%s "
                "conversation_id=%s "
                "chunks=%d "
                "response_length=%d",
                request_id,
                conversation_id,
                len(response_chunks),
                len(answer),
            )

            # -------------------------------------------------
            # Save assistant response
            # -------------------------------------------------

            self.message_repository.save(
                conversation_id,
                "assistant",
                answer,
            )

            logger.info(
                "stream_assistant_message_saved "
                "request_id=%s conversation_id=%s",
                request_id,
                conversation_id,
            )

        except Exception:

            logger.exception(
                "stream_chat_failed "
                "request_id=%s "
                "conversation_id=%s "
                "chunks=%d",
                request_id,
                conversation_id,
                len(response_chunks),
            )

            raise


    def _generate_with_tools(
        self,
        messages: list[ChatMessage],
    ) -> str:

        request_id = get_request_id()

        tool_definitions = (
            self.tool_registry.get_definitions()
        )

        tool_results: list[ToolResult] = []

        tool_call_count = 0

        while tool_call_count < MAX_TOOL_CALLS:

            response = (
                self.llm_provider.generate_with_tools(
                    messages=messages,
                    tools=tool_definitions,
                    tool_results=tool_results or None,
                )
            )

            # ---------------------------------------------
            # Final answer
            # ---------------------------------------------

            if not response.tool_calls:

                return response.text or ""


            # ---------------------------------------------
            # Execute requested tools
            # ---------------------------------------------

            for tool_call in response.tool_calls:

                if tool_call_count >= MAX_TOOL_CALLS:

                    break

                tool_call_count += 1

                logger.info(
                    "tool_call_requested "
                    "request_id=%s "
                    "tool_name=%s "
                    "tool_call_count=%d",
                    request_id,
                    tool_call.name,
                    tool_call_count,
                )

                try:

                    execution = (
                        self.tool_executor.execute(
                            tool_name=tool_call.name,
                            arguments=tool_call.arguments,
                            request_id=request_id,
                        )
                    )

                    tool_results.append(
                        ToolResult(
                            tool_call_id=tool_call.id,
                            name=tool_call.name,
                            result=execution["result"],
                            success=True,
                        )
                    )

                except Exception as exc:

                    logger.warning(
                        "tool_execution_failed "
                        "request_id=%s "
                        "tool_name=%s "
                        "error=%s",
                        request_id,
                        tool_call.name,
                        str(exc),
                    )

                    tool_results.append(
                        ToolResult(
                            tool_call_id=tool_call.id,
                            name=tool_call.name,
                            result=None,
                            success=False,
                            error=(
                                "The requested tool "
                                "could not be executed."
                            ),
                        )
                    )

        logger.warning(
            "tool_call_limit_reached "
            "request_id=%s "
            "max_tool_calls=%d",
            request_id,
            MAX_TOOL_CALLS,
        )

        return (
            "I could not complete the request because "
            "the maximum number of tool calls was reached."
        )