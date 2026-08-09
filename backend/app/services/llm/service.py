from collections.abc import AsyncGenerator

from app.prompts.chat import prepare_chat_messages
from app.schemas.chat import ChatMessage

from .gemini import (
    generate_response as gemini_generate,
    stream_response as gemini_stream,
)


def generate_response(
    messages: list[ChatMessage],
) -> str:

    prompt = prepare_chat_messages(messages)

    return gemini_generate(prompt)


async def stream_response(
    messages: list[ChatMessage],
) -> AsyncGenerator[str, None]:

    prompt = prepare_chat_messages(messages)

    async for chunk in gemini_stream(prompt):
        yield chunk