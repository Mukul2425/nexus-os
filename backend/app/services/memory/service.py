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
from app.services.memory.normalizer import normalize_memory_content
from app.services.memory.vector_store import (
    add_memory,
    delete_memory,
    update_memory,
)

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
    content: str,
    memory_type: str = "semantic",
    importance: int = 3,
    ):
        if not content or not content.strip():
            raise InvalidMemoryError(
                "Memory content cannot be empty."
            )

        if memory_type not in {"semantic", "episodic"}:
            raise InvalidMemoryError(
                "Invalid memory type."
            )

        if not isinstance(importance, int) or not 1 <= importance <= 5:
            raise InvalidMemoryError(
                "Memory importance must be between 1 and 5."
            )

        normalized_content = normalize_memory_content(
            content
        )

        for existing in self.repository.list(limit=1000):
            if (
                normalize_memory_content(existing.content)
                == normalized_content
            ):
                raise InvalidMemoryError(
                    "A memory with the same content already exists."
                )

        memory = self.repository.create(
            content=content.strip(),
            memory_type=memory_type,
            importance=importance,
        )

        try:
            add_memory(
                memory_id=memory.id,
                content=memory.content,
                memory_type=memory.memory_type,
                importance=memory.importance,
            )
        except Exception:
            logger.exception(
                "memory_vector_index_failed memory_id=%s",
                memory.id,
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
        memory = self.repository.get(memory_id)

        if memory is None:
            raise MemoryNotFoundError()

        if content is not None:
            normalized_content = normalize_memory_content(content)

            for existing in self.repository.list(limit=1000):
                if existing.id == memory.id:
                    continue

                if (
                    normalize_memory_content(existing.content)
                    == normalized_content
                ):
                    raise InvalidMemoryError(
                        "A memory with the same content already exists."
                    )

        memory = self.repository.update(
            memory,
            content=content,
            memory_type=memory_type,
            importance=importance,
        )

        try:
            update_memory(
                memory_id=memory.id,
                content=memory.content,
                memory_type=memory.memory_type,
                importance=memory.importance,
            )
        except Exception:
            logger.exception(
                "memory_vector_update_failed memory_id=%s",
                memory.id,
            )

        return memory



    
    def delete(self, memory_id: str) -> None:
        memory = self.repository.get(memory_id)

        if memory is None:
            raise MemoryNotFoundError()

        self.repository.delete(memory)

        try:
            delete_memory(memory.id)
        except Exception:
            logger.exception(
                "memory_vector_delete_failed memory_id=%s",
                memory.id,
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
            memory = self.persist_candidate(candidate)

            if memory is not None:
                created.append(memory)


        logger.info(
            "memory_extraction_persisted "
            "request_id=%s "
            "created=%d",
            request_id,
            len(created),
        )

        return created


    def persist_candidate(self, candidate):
        normalized_content = normalize_memory_content(
            candidate.content
        )

        existing_memories = self.repository.list(
            limit=1000
        )

        for existing in existing_memories:
            if (
                normalize_memory_content(existing.content)
                == normalized_content
            ):
                logger.info(
                    "memory_duplicate_skipped memory_id=%s",
                    existing.id,
                )
                return existing

        return self.create(
            content=candidate.content,
            memory_type=candidate.memory_type,
            importance=candidate.importance,
        )