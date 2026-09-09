from unittest.mock import patch

from app.services.memory.retriever import (
    MemoryRetriever,
)


def test_retrieve_relevant_memories(db):
    service = MemoryRetriever(
        db,
        top_k=3,
        distance_threshold=0.8,
    )

    memory = service.repository.create(
        content="User prefers Python.",
        memory_type="semantic",
        importance=4,
    )

    chroma_results = {
        "documents": [
            ["User prefers Python."]
        ],
        "metadatas": [
            [
                {
                    "memory_id": memory.id,
                    "memory_type": "semantic",
                    "importance": 4,
                }
            ]
        ],
        "distances": [
            [0.2]
        ],
    }

    with patch(
        "app.services.memory.retriever.search_memories",
        return_value=chroma_results,
    ):
        results = service.retrieve(
            "What programming language do I prefer?"
        )

    assert len(results) == 1
    assert results[0]["memory_id"] == memory.id
    assert results[0]["content"] == "User prefers Python."



def test_retrieve_filters_distant_memories(db):
    service = MemoryRetriever(
        db,
        top_k=5,
        distance_threshold=0.5,
    )

    memory = service.repository.create(
        content="User prefers Python.",
        memory_type="semantic",
        importance=4,
    )

    chroma_results = {
        "documents": [
            ["User prefers Python."]
        ],
        "metadatas": [
            [
                {
                    "memory_id": memory.id,
                    "memory_type": "semantic",
                    "importance": 4,
                }
            ]
        ],
        "distances": [
            [0.9]
        ],
    }

    with patch(
        "app.services.memory.retriever.search_memories",
        return_value=chroma_results,
    ):
        results = service.retrieve(
            "What language do I like?"
        )

    assert results == []




def test_retrieve_ignores_deleted_memory(db):
    service = MemoryRetriever(db)

    chroma_results = {
        "documents": [
            ["User prefers Python."]
        ],
        "metadatas": [
            [
                {
                    "memory_id": "does-not-exist",
                    "memory_type": "semantic",
                    "importance": 4,
                }
            ]
        ],
        "distances": [
            [0.1]
        ],
    }

    with patch(
        "app.services.memory.retriever.search_memories",
        return_value=chroma_results,
    ):
        results = service.retrieve(
            "What language do I prefer?"
        )

    assert results == []




def test_retrieve_empty_query_returns_empty(db):
    service = MemoryRetriever(db)

    with patch(
        "app.services.memory.retriever.search_memories"
    ) as mock_search:

        results = service.retrieve("")

    assert results == []

    mock_search.assert_not_called()