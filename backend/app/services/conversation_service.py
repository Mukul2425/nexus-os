from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.schemas.chat import ChatMessage

from app.services.llm import generate_response

from app.logging.logger import logger
from app.logging.context import get_request_id


class ConversationService:

    def __init__(self, db):

        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

    def chat(
        self,
        conversation_id: str,
        message: str,
    ):

        request_id = get_request_id()

        # Log that we received a message for this conversation
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
            "user_message_saved request_id=%s conversation_id=%s",
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