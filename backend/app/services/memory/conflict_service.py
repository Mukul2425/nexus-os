from app.services.memory.vector_store import search_memories
from app.services.memory.conflict import MemoryConflictDetector


class MemoryConflictService:

    def __init__(self, llm_provider):
        self.detector = MemoryConflictDetector(
            llm_provider
        )

    def find_conflicts(
    self,
    content: str,
    top_k: int = 5,
) -> list[str]:

        results = search_memories(
            query=content,
            top_k=top_k,
        )

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        documents = results.get(
            "documents",
            [[]],
        )[0]

        conflicts = []

        for document, metadata in zip(
            documents,
            metadatas,
        ):
            if self.detector.is_conflict(
                existing_memory=document,
                new_memory=content,
            ):
                conflicts.append(
                    metadata["memory_id"]
                )

        return conflicts