from collections.abc import AsyncGenerator

from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.schemas.chat import ChatMessage

from app.services.llm import (
    generate_response,
    stream_response,
)

from app.logging.logger import logger
from app.logging.context import get_request_id

from app.core.exceptions import ConversationNotFoundError

class ConversationService:

    def __init__(self, db):

        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

    # ---------------------------------------------------------
    # Normal chat
    # ---------------------------------------------------------

    def chat(
        self,
        conversation_id: str,
        message: str,
    ):
        request_id = get_request_id()

        conversation = self.conversation_repository.get(conversation_id)
        if conversation is None:
            raise ConversationNotFoundError()

        

        logger.info(
            "chat_request request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # Save user's message
        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        logger.info(
            "user_message_saved "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # Load conversation history
        history = self.message_repository.get_messages(
            conversation_id
        )

        logger.info(
            "conversation_history_loaded "
            "request_id=%s conversation_id=%s messages=%d",
            request_id,
            conversation_id,
            len(history),
        )

        # Convert database messages into ChatMessage objects
        messages = [
            ChatMessage(
                role=m.role,
                content=m.content,
            )
            for m in history
        ]

        # Call LLM
        answer = generate_response(messages)

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

        # ---------------------------------------------------------
        # Validate conversation
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # Save user message
        # ---------------------------------------------------------

        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

        logger.info(
            "stream_user_message_saved "
            "request_id=%s conversation_id=%s",
            request_id,
            conversation_id,
        )

        # ---------------------------------------------------------
        # Load conversation history
        # ---------------------------------------------------------

        history = self.message_repository.get_messages(
            conversation_id
        )

        logger.info(
            "stream_conversation_history_loaded "
            "request_id=%s conversation_id=%s messages=%d",
            request_id,
            conversation_id,
            len(history),
        )

        # ---------------------------------------------------------
        # Convert database messages to ChatMessage
        # ---------------------------------------------------------

        messages = [
            ChatMessage(
                role=m.role,
                content=m.content,
            )
            for m in history
        ]

        # ---------------------------------------------------------
        # Stream LLM response
        # ---------------------------------------------------------

        response_chunks = []

        try:

            async for chunk in stream_response(messages):

                response_chunks.append(chunk)

                # Send chunk immediately to client
                yield chunk

            # -----------------------------------------------------
            # Reconstruct complete response
            # -----------------------------------------------------

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

            # -----------------------------------------------------
            # Save assistant response
            # -----------------------------------------------------

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