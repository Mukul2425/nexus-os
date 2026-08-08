from collections.abc import AsyncGenerator

from google import genai

from app.core.config import settings
from app.schemas.chat import ChatMessage

client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def _build_contents(messages: list[ChatMessage]):
    """
    Convert our internal ChatMessage schema
    into Gemini's expected format.
    """
    return [
        {
            "role": message.role,
            "parts": [{"text": message.content}],
        }
        for message in messages
    ]


def generate_response(messages: list[ChatMessage]) -> str:
    """
    Non-streaming response.
    Used by /chat
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=_build_contents(messages),
    )

    return response.text


async def stream_response(
    messages: list[ChatMessage],
) -> AsyncGenerator[str, None]:
    """
    Streaming response.
    Used by /chat/stream
    """

    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=_build_contents(messages),
    )

    for chunk in stream:

        if chunk.text:
            yield chunk.text