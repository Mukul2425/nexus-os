from app.services.memory.context import (
    build_memory_context,
    build_memory_message,
)


def test_build_memory_context():
    memories = [
        {
            "memory_id": "1",
            "content": "User prefers Python.",
            "memory_type": "semantic",
            "importance": 4,
            "distance": 0.2,
        },
        {
            "memory_id": "2",
            "content": "User uses FastAPI.",
            "memory_type": "semantic",
            "importance": 5,
            "distance": 0.3,
        },
    ]

    context = build_memory_context(
        memories
    )

    assert context is not None
    assert "User prefers Python." in context
    assert "User uses FastAPI." in context


def test_build_memory_context_empty():
    assert build_memory_context([]) is None


def test_build_memory_message():
    memories = [
        {
            "memory_id": "1",
            "content": "User prefers Python.",
            "memory_type": "semantic",
            "importance": 4,
            "distance": 0.2,
        }
    ]

    message = build_memory_message(
        memories
    )

    assert message is not None
    assert message.role == "system"
    assert "User prefers Python." in message.content


def test_build_memory_message_empty():
    assert build_memory_message([]) is None