import pytest

from app.core.exceptions import (
    InvalidMemoryError,
    MemoryNotFoundError,
)
from app.services.memory.service import MemoryService


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