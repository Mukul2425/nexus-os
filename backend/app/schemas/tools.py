from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """
    Provider-independent definition of a tool that can
    be exposed to an LLM.
    """

    name: str

    description: str

    input_schema: dict[str, Any]


class ToolCall(BaseModel):
    """
    Provider-independent tool call requested by an LLM.
    """

    id: str | None = None

    name: str

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )


class ToolResult(BaseModel):
    """
    Provider-independent result returned after tool execution.
    """

    tool_call_id: str | None = None

    name: str

    success: bool

    result: Any | None = None

    error: str | None = None