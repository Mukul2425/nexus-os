from app.models.message import Message


class MessageRepository:

    def __init__(self, db):
        self.db = db

    def save(self, conversation_id, role, content):

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)

        self.db.commit()

    def get_messages(self, conversation_id):

        return (
            self.db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at)
            .all()
        )