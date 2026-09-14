from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    MAX_STEPS_REACHED = "max_steps_reached"


class AgentActionType(str, Enum):
    ANSWER = "answer"
    TOOL = "tool"
    RAG = "rag"
    MEMORY = "memory"
    STOP = "stop"


class AgentAction(BaseModel):
    type: AgentActionType

    tool_name: str | None = None

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )

    query: str | None = None

    response: str | None = None


class AgentStep(BaseModel):
    step_number: int

    action: AgentAction

    observation: Any | None = None

    success: bool = True

    error: str | None = None


class AgentState(BaseModel):
    task: str
    conversation_id: str
    current_step: int = 0

    plan: list[str] = Field(default_factory=list)
    plan_progress: list[str] = Field(default_factory=list)
    current_plan_step: int = 0
    
    observations: list[Any] = Field(default_factory=list)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)

    retrieved_memories: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_documents: list[dict[str, Any]] = Field(default_factory=list)

    status: AgentStatus = AgentStatus.CREATED
    final_response: str | None = None

    steps: list[AgentStep] = Field(default_factory=list)


class AgentResult(BaseModel):
    execution_id: str
    conversation_id: str
    status: AgentStatus

    response: str | None = None

    steps: list[AgentStep] = Field(default_factory=list)

    step_count: int = 0
    tool_call_count: int = 0

    plan: list[str] = Field(default_factory=list)
    plan_progress: list[str] = Field(default_factory=list)

    retrieved_memories: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_documents: list[dict[str, Any]] = Field(default_factory=list)

    error: str | None = None



