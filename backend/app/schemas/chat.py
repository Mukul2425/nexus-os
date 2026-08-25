from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class Source(BaseModel):
    document: str
    chunk_id: int
    score: float


class ChatResponse(BaseModel):
    response: str
    sources: list[Source] = Field(
        default_factory=list
    )