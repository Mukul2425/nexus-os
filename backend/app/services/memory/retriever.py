from time import perf_counter

from app.logging.context import get_request_id
from app.logging.logger import logger
from app.repositories.memory_repository import MemoryRepository
from app.services.memory.vector_store import search_memories


DEFAULT_TOP_K = 5
DEFAULT_DISTANCE_THRESHOLD = 0.8


class MemoryRetriever:

    def __init__(
        self,
        db,
        top_k: int = DEFAULT_TOP_K,
        distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
    ):
        self.repository = MemoryRepository(db)
        self.top_k = top_k
        self.distance_threshold = distance_threshold

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict]:

        request_id = get_request_id()
        start = perf_counter()

        limit = top_k or self.top_k

        logger.info(
            "memory_retrieval_started "
            "request_id=%s "
            "top_k=%d",
            request_id,
            limit,
        )

        if not query or not query.strip():
            return []

        results = search_memories(
            query=query,
            top_k=limit,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        retrieved = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            if distance > self.distance_threshold:
                continue

            memory_id = metadata.get("memory_id")

            if not memory_id:
                continue

            memory = self.repository.get(
                memory_id
            )

            # Chroma can contain stale vectors.
            # SQLite is the source of truth.
            if memory is None:
                logger.warning(
                    "memory_vector_stale "
                    "request_id=%s "
                    "memory_id=%s",
                    request_id,
                    memory_id,
                )
                continue

            retrieved.append(
                {
                    "memory_id": memory.id,
                    "content": memory.content,
                    "memory_type": memory.memory_type,
                    "importance": memory.importance,
                    "distance": distance,
                }
            )

        latency = perf_counter() - start

        logger.info(
            "memory_retrieval_complete "
            "request_id=%s "
            "memories_retrieved=%d "
            "latency=%.3fs",
            request_id,
            len(retrieved),
            latency,
        )

        return retrieved