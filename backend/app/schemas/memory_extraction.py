from pydantic import BaseModel, Field


class MemoryCandidate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=2000,
    )

    memory_type: str = "semantic"

    importance: int = Field(
        default=3,
        ge=1,
        le=5,
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class MemoryExtractionResult(BaseModel):
    memories: list[MemoryCandidate] = Field(
        default_factory=list
    )