from app.models.conversation import Conversation


class ConversationRepository:

    def __init__(self, db):
        self.db = db

    def create(self):

        conversation = Conversation()

        self.db.add(conversation)

        self.db.commit()

        self.db.refresh(conversation)

        return conversation