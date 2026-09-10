from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    memory_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="semantic",
    )

    importance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("ix_memories_memory_type", "memory_type"),
        Index("ix_memories_created_at", "created_at"),
    )