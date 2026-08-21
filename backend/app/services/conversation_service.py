from collections.abc import AsyncGenerator

from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.schemas.chat import ChatMessage

from app.services.llm.provider import LLMProvider

from app.logging.logger import logger
from app.logging.context import get_request_id

from app.core.exceptions import ConversationNotFoundError


class ConversationService:

    def __init__(
        self,
        db,
        llm_provider: LLMProvider,
    ):
        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)
        self.llm_provider = llm_provider

    # ---------------------------------------------------------
    # Normal chat
    # ---------------------------------------------------------

    def chat(
        self,
        conversation_id: str,
        message: str,
    ) -> str:

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

        # Save user message
        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        # Load conversation history
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

        # LLM abstraction
        answer = self.llm_provider.generate(
            messages
        )

        logger.info(
            "llm_response_received "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # Save assistant response
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

        return answer

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

        # Save user message
        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        # Load history
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

        response_chunks = []

        try:

            async for chunk in self.llm_provider.stream(
                messages
            ):

                response_chunks.append(chunk)

                # Immediately send chunk to client
                yield chunk

            # Reconstruct complete response
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

            # Save complete assistant response
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