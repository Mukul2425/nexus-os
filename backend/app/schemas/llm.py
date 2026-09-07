from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """
    Provider-neutral description of an available tool.
    """

    name: str
    description: str
    input_schema: dict[str, Any]


class ToolCall(BaseModel):
    """
    Provider-neutral request from an LLM to execute a tool.
    """

    id: str | None = None
    name: str
    arguments: dict[str, Any] = Field(
        default_factory=dict
    )


class ToolResult(BaseModel):
    """
    Provider-neutral result returned after tool execution.
    """

    tool_call_id: str | None = None
    name: str
    result: Any
    success: bool = True
    error: str | None = None


class LLMResponse(BaseModel):
    """
    Structured provider response.

    The provider can either return final text,
    request one or more tools, or both.
    """

    text: str | None = None

    tool_calls: list[ToolCall] = Field(
        default_factory=list
    )