import uuid
from datetime import datetime

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
        ForeignKey("conversations.id"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )