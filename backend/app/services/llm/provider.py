from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.schemas.chat import ChatMessage


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