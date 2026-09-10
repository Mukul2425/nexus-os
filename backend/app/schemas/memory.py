from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


MemoryType = Literal["semantic", "episodic"]


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    memory_type: MemoryType = "semantic"
    importance: int = Field(default=3, ge=1, le=5)


class MemoryUpdate(BaseModel):
    content: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )
    memory_type: MemoryType | None = None
    importance: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )


class MemoryResponse(BaseModel):
    id: str
    content: str
    memory_type: MemoryType
    importance: int
    created_at: datetime
    updated_at: datetime


class MemoryListResponse(BaseModel):
    memories: list[MemoryResponse]
    total: int