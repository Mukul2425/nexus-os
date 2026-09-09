import pytest

from app.core.exceptions import (
    InvalidMemoryError,
    MemoryNotFoundError,
)
from app.services.memory.service import MemoryService
from unittest.mock import MagicMock


def test_memory_service_create(db):
    service = MemoryService(db)

    memory = service.create(
        content="User prefers FastAPI.",
        memory_type="semantic",
        importance=4,
    )

    assert memory.content == "User prefers FastAPI."


def test_memory_service_rejects_empty_content(db):
    service = MemoryService(db)

    with pytest.raises(InvalidMemoryError):
        service.create(content="   ")


def test_memory_service_rejects_invalid_type(db):
    service = MemoryService(db)

    with pytest.raises(InvalidMemoryError):
        service.create(
            content="Something",
            memory_type="invalid",
        )


def test_memory_service_get_missing(db):
    service = MemoryService(db)

    with pytest.raises(MemoryNotFoundError):
        service.get("does-not-exist")


def test_memory_service_delete(db):
    service = MemoryService(db)

    memory = service.create(
        content="Delete me.",
    )

    service.delete(memory.id)

    with pytest.raises(MemoryNotFoundError):
        service.get(memory.id)





def test_extract_and_create_memory(db):
    provider = MagicMock()

    provider.generate.return_value = """
    {
        "memories": [
            {
                "content": "User prefers Python.",
                "memory_type": "semantic",
                "importance": 4,
                "confidence": 0.95
            }
        ]
    }
    """

    service = MemoryService(
        db,
        llm_provider=provider,
    )

    memories = service.extract_and_create(
        "I prefer Python."
    )

    assert len(memories) == 1
    assert memories[0].content == (
        "User prefers Python."
    )


def test_extract_and_create_rejects_irrelevant_memory(db):
    provider = MagicMock()

    provider.generate.return_value = """
    {
        "memories": [
            {
                "content": "What is Python?",
                "memory_type": "semantic",
                "importance": 2,
                "confidence": 0.99
            }
        ]
    }
    """

    service = MemoryService(
        db,
        llm_provider=provider,
    )

    memories = service.extract_and_create(
        "What is Python?"
    )

    assert memories == []