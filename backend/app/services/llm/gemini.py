from collections.abc import AsyncGenerator
from time import perf_counter

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.chat import ChatMessage
from app.core.exceptions import LLMProviderError
from app.logging.logger import logger
from app.logging.context import get_request_id


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

MODEL_NAME = "gemini-2.5-flash"


def _build_contents(
    messages: list[ChatMessage],
) -> tuple[str | None, list[dict]]:
    """
    Separate the system instruction from the
    conversation messages because Gemini expects
    system instructions separately.
    """

    system_instruction = None
    contents = []

    for message in messages:

        if message.role == "system":

            system_instruction = message.content

        elif message.role == "user":

            contents.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": message.content
                        }
                    ],
                }
            )

        elif message.role == "assistant":

            contents.append(
                {
                    "role": "model",
                    "parts": [
                        {
                            "text": message.content
                        }
                    ],
                }
            )

    return system_instruction, contents

def generate_response(
    messages: list[ChatMessage],
) -> str:

    request_id = get_request_id()

    system_instruction, contents = _build_contents(
        messages
    )

    logger.info(
        "llm_request "
        "request_id=%s "
        "provider=gemini "
        "model=%s "
        "messages=%d",
        request_id,
        MODEL_NAME,
        len(messages),
    )

    start = perf_counter()

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        latency = perf_counter() - start

        logger.info(
            "llm_response "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "latency=%.3fs",
            request_id,
            MODEL_NAME,
            latency,
        )

        return response.text

    except Exception as exc:

        latency = perf_counter() - start

        logger.exception(
        "llm_error "
        "request_id=%s "
        "provider=gemini "
        "model=%s "
        "latency=%.3fs",
        request_id,
        MODEL_NAME,
        latency,
        )

        raise LLMProviderError() from exc
    
async def stream_response(
    messages: list[ChatMessage],
) -> AsyncGenerator[str, None]:

    request_id = get_request_id()

    system_instruction, contents = _build_contents(
        messages
    )

    logger.info(
        "llm_stream_start "
        "request_id=%s "
        "provider=gemini "
        "model=%s "
        "messages=%d",
        request_id,
        MODEL_NAME,
        len(messages),
    )

    start = perf_counter()
    chunk_count = 0

    try:

        stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        for chunk in stream:

            if chunk.text:
                chunk_count += 1
                yield chunk.text

        latency = perf_counter() - start

        logger.info(
            "llm_stream_complete "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "chunks=%d "
            "latency=%.3fs",
            request_id,
            MODEL_NAME,
            chunk_count,
            latency,
        )

    except Exception:

        latency = perf_counter() - start

        logger.exception(
            "llm_stream_error "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "chunks=%d "
            "latency=%.3fs",
            request_id,
            MODEL_NAME,
            chunk_count,
            latency,
        )

        raise