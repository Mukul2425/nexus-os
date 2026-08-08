from collections.abc import AsyncGenerator

from app.schemas.chat import ChatMessage

from .gemini import (
    generate_response as gemini_generate_response,
)

from .gemini import (
    stream_response as gemini_stream_response,
)


def generate_response(
    messages: list[ChatMessage],
) -> str:

    return gemini_generate_response(messages)


async def stream_response(
    messages: list[ChatMessage],
) -> AsyncGenerator[str, None]:

    async for chunk in gemini_stream_response(messages):
        yield chunk