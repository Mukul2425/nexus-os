from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.schemas.chat import ChatMessage
from app.schemas.llm import (
    LLMResponse,
    ToolDefinition,
    ToolResult,
)


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a complete response.
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[ChatMessage],
    ) -> AsyncGenerator[str, None]:
        """
        Stream the response chunk by chunk.
        """
        pass

    @abstractmethod
    def generate_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
        tool_results: list[ToolResult] | None = None,
    ) -> LLMResponse:
        """
        Generate a response with provider-neutral
        tool calling support.

        The provider may return:
        - final text
        - one or more tool calls
        """
        pass