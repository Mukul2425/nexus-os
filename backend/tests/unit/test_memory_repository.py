from app.repositories.memory_repository import MemoryRepository


def test_create_memory(db):
    repository = MemoryRepository(db)

    memory = repository.create(
        content="User prefers Python.",
        memory_type="semantic",
        importance=4,
    )

    assert memory.id
    assert memory.content == "User prefers Python."
    assert memory.memory_type == "semantic"
    assert memory.importance == 4


def test_get_memory(db):
    repository = MemoryRepository(db)

    created = repository.create(
        content="User works on Nexus.",
    )

    loaded = repository.get(created.id)

    assert loaded is not None
    assert loaded.id == created.id


def test_update_memory(db):
    repository = MemoryRepository(db)

    memory = repository.create(
        content="User prefers Python.",
    )

    updated = repository.update(
        memory,
        content="User prefers TypeScript.",
        importance=5,
    )

    assert updated.content == "User prefers TypeScript."
    assert updated.importance == 5


def test_delete_memory(db):
    repository = MemoryRepository(db)

    memory = repository.create(
        content="Temporary memory.",
    )

    repository.delete(memory)

    assert repository.get(memory.id) is None