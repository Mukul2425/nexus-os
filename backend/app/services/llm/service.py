from collections.abc import AsyncGenerator

from app.schemas.chat import ChatMessage
from app.services.llm.factory import create_llm_provider
from app.services.llm.provider import LLMProvider


class LLMService:

    def __init__(
        self,
        provider: LLMProvider | None = None,
    ):

        self.provider = (
            provider
            if provider is not None
            else create_llm_provider()
        )

    def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:

        return self.provider.generate(messages)

    async def stream(
        self,
        messages: list[ChatMessage],
    ) -> AsyncGenerator[str, None]:

        async for chunk in self.provider.stream(messages):

            yield chunk