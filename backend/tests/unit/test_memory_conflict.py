from unittest.mock import MagicMock

from app.services.memory.conflict import (
    MemoryConflictDetector,
)


def test_detects_conflict():
    provider = MagicMock()

    provider.generate.return_value = """
    {
        "conflict": true
    }
    """

    detector = MemoryConflictDetector(
        provider
    )

    assert detector.is_conflict(
        existing_memory="User prefers Python.",
        new_memory="User prefers TypeScript.",
    ) is True


def test_detects_no_conflict():
    provider = MagicMock()

    provider.generate.return_value = """
    {
        "conflict": false
    }
    """

    detector = MemoryConflictDetector(
        provider
    )

    assert detector.is_conflict(
        existing_memory="User prefers Python.",
        new_memory="User uses FastAPI.",
    ) is False


def test_invalid_response_is_safe():
    provider = MagicMock()

    provider.generate.return_value = "invalid json"

    detector = MemoryConflictDetector(
        provider
    )

    assert detector.is_conflict(
        existing_memory="User prefers Python.",
        new_memory="User prefers TypeScript.",
    ) is False