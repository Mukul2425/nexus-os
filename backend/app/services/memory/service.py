from app.core.exceptions import (
    InvalidMemoryError,
    MemoryNotFoundError,
)
from app.logging.context import get_request_id
from app.logging.logger import logger
from app.repositories.memory_repository import MemoryRepository
from app.services.memory.eligibility import (
    MemoryEligibilityService,
)
from app.services.memory.extractor import MemoryExtractor


class MemoryService:

    def __init__(
        self,
        db,
        llm_provider=None,
    ):
        self.repository = MemoryRepository(db)

        self.eligibility = (
            MemoryEligibilityService()
        )

        self.extractor = (
            MemoryExtractor(llm_provider)
            if llm_provider is not None
            else None
        )

    # ---------------------------------------------------------
    # Manual memory management
    # ---------------------------------------------------------

    def create(
        self,
        *,
        content: str,
        memory_type: str = "semantic",
        importance: int = 3,
    ):
        content = content.strip()

        if not content:
            raise InvalidMemoryError(
                "Memory content cannot be empty."
            )

        if memory_type not in {
            "semantic",
            "episodic",
        }:
            raise InvalidMemoryError(
                "Memory type must be semantic or episodic."
            )

        if not 1 <= importance <= 5:
            raise InvalidMemoryError(
                "Memory importance must be between 1 and 5."
            )

        memory = self.repository.create(
            content=content,
            memory_type=memory_type,
            importance=importance,
        )

        logger.info(
            "memory_created "
            "request_id=%s "
            "memory_id=%s "
            "memory_type=%s "
            "importance=%d",
            get_request_id(),
            memory.id,
            memory.memory_type,
            memory.importance,
        )

        return memory

    def get(self, memory_id: str):
        memory = self.repository.get(memory_id)

        if memory is None:
            raise MemoryNotFoundError()

        return memory

    def list(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ):
        if limit < 1 or limit > 1000:
            raise InvalidMemoryError(
                "Limit must be between 1 and 1000."
            )

        if offset < 0:
            raise InvalidMemoryError(
                "Offset cannot be negative."
            )

        return self.repository.list(
            limit=limit,
            offset=offset,
        )

    def update(
        self,
        memory_id: str,
        *,
        content: str | None = None,
        memory_type: str | None = None,
        importance: int | None = None,
    ):
        memory = self.get(memory_id)

        if content is not None:
            content = content.strip()

            if not content:
                raise InvalidMemoryError(
                    "Memory content cannot be empty."
                )

        if memory_type is not None:
            if memory_type not in {
                "semantic",
                "episodic",
            }:
                raise InvalidMemoryError(
                    "Memory type must be semantic or episodic."
                )

        if importance is not None:
            if not 1 <= importance <= 5:
                raise InvalidMemoryError(
                    "Memory importance must be between 1 and 5."
                )

        updated = self.repository.update(
            memory,
            content=content,
            memory_type=memory_type,
            importance=importance,
        )

        logger.info(
            "memory_updated "
            "request_id=%s "
            "memory_id=%s",
            get_request_id(),
            memory_id,
        )

        return updated

    def delete(self, memory_id: str) -> None:
        memory = self.get(memory_id)

        self.repository.delete(memory)

        logger.info(
            "memory_deleted "
            "request_id=%s "
            "memory_id=%s",
            get_request_id(),
            memory_id,
        )

    # ---------------------------------------------------------
    # Automatic extraction
    # ---------------------------------------------------------

    def extract_and_create(
        self,
        message: str,
    ):
        if self.extractor is None:
            raise RuntimeError(
                "Memory extractor requires an LLM provider."
            )

        request_id = get_request_id()

        candidates = self.extractor.extract(
            message
        )

        eligible = self.eligibility.filter(
            candidates
        )

        logger.info(
            "memory_candidates_filtered "
            "request_id=%s "
            "candidates=%d "
            "eligible=%d",
            request_id,
            len(candidates),
            len(eligible),
        )

        created = []

        for candidate in eligible:
            memory = self.create(
                content=candidate.content,
                memory_type=candidate.memory_type,
                importance=candidate.importance,
            )

            created.append(memory)

        logger.info(
            "memory_extraction_persisted "
            "request_id=%s "
            "created=%d",
            request_id,
            len(created),
        )

        return created