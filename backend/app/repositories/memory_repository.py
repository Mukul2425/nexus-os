from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        content: str,
        memory_type: str = "semantic",
        importance: int = 3,
    ) -> Memory:
        memory = Memory(
            content=content,
            memory_type=memory_type,
            importance=importance,
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def get(self, memory_id: str) -> Memory | None:
        return self.db.get(Memory, memory_id)

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Memory]:
        statement = (
            select(Memory)
            .order_by(Memory.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def count(self) -> int:
        from sqlalchemy import func

        statement = select(func.count()).select_from(Memory)

        return int(self.db.scalar(statement) or 0)

    def update(
        self,
        memory: Memory,
        *,
        content: str | None = None,
        memory_type: str | None = None,
        importance: int | None = None,
    ) -> Memory:
        if content is not None:
            memory.content = content

        if memory_type is not None:
            memory.memory_type = memory_type

        if importance is not None:
            memory.importance = importance

        memory.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(memory)

        return memory

    def delete(self, memory: Memory) -> None:
        self.db.delete(memory)
        self.db.commit()