from app.repositories.message_repository import MessageRepository
from app.schemas.chat import ChatMessage

from app.services.llm import generate_response
from backend.app.repositories.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(self, db):

        self.conversation_repository = ConversationRepository(db)

        self.message_repository = MessageRepository(db)

    def chat(
        self,
        conversation_id,
        message,
    ):

        self.message_repository.save(
            conversation_id,
            "user",
            message,
        )

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

        answer = generate_response(messages)

        self.repo.save(
            conversation_id,
            "assistant",
            answer,
        )

        return answer