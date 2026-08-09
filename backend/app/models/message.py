import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class Message(Base):

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id")
    )

    role: Mapped[str]

    content: Mapped[str]

    created_at: Mapped[DateTime] = mapped_column(
        server_default=func.now()
    )