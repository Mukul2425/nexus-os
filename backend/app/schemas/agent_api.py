from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent import (
    AgentStatus,
    AgentStep,
)


class AgentRunRequest(BaseModel):
    """
    HTTP request payload for running the Nexus agent.
    """

    conversation_id: str = Field(
        min_length=1,
        description="Conversation identifier.",
    )

    message: str = Field(
        min_length=1,
        description="Task to execute with the agent.",
    )


class AgentRunResponse(BaseModel):
    """
    Public HTTP response for an agent execution.

    This intentionally exposes execution metadata without
    exposing the complete internal AgentState.
    """

    execution_id: str
    conversation_id: str

    status: AgentStatus

    response: str | None = None

    steps: list[AgentStep] = Field(
        default_factory=list,
    )

    plan: list[str] = Field(
        default_factory=list,
    )

    plan_progress: list[dict[str, Any]] = Field(default_factory=list)

    step_count: int = 0

    tool_call_count: int = 0

    error: str | None = None