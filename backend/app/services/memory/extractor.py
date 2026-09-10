import json
from time import perf_counter

from app.logging.context import get_request_id
from app.logging.logger import logger
from app.prompts.memory import MEMORY_EXTRACTION_PROMPT
from app.schemas.chat import ChatMessage
from app.schemas.memory_extraction import (
    MemoryCandidate,
    MemoryExtractionResult,
)
from app.services.llm.provider import LLMProvider


class MemoryExtractor:

    def __init__(
        self,
        llm_provider: LLMProvider,
    ):
        self.llm_provider = llm_provider

    def extract(
        self,
        message: str,
    ) -> list[MemoryCandidate]:

        request_id = get_request_id()
        start = perf_counter()

        prompt = (
            f"{MEMORY_EXTRACTION_PROMPT}\n\n"
            f"USER MESSAGE:\n{message}"
        )

        response = self.llm_provider.generate(
            [
                ChatMessage(
                    role="user",
                    content=prompt,
                )
            ]
        )

        latency = perf_counter() - start

        try:
            payload = json.loads(response)

            result = MemoryExtractionResult.model_validate(
                payload
            )

        except Exception:
            logger.exception(
                "memory_extraction_parse_failed "
                "request_id=%s",
                request_id,
            )

            return []

        logger.info(
            "memory_extraction_complete "
            "request_id=%s "
            "candidates=%d "
            "latency=%.3fs",
            request_id,
            len(result.memories),
            latency,
        )

        return result.memories