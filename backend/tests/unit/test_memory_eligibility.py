from app.schemas.memory_extraction import MemoryCandidate
from app.services.memory.eligibility import (
    MemoryEligibilityService,
)


def test_accepts_useful_memory():
    service = MemoryEligibilityService()

    candidate = MemoryCandidate(
        content="User prefers Python.",
        memory_type="semantic",
        importance=4,
        confidence=0.95,
    )

    assert service.is_eligible(candidate)


def test_rejects_low_confidence():
    service = MemoryEligibilityService()

    candidate = MemoryCandidate(
        content="User probably likes Python.",
        confidence=0.4,
    )

    assert not service.is_eligible(candidate)


def test_rejects_question():
    service = MemoryEligibilityService()

    candidate = MemoryCandidate(
        content="What is Python?",
        confidence=0.99,
    )

    assert not service.is_eligible(candidate)


def test_rejects_temporary_request():
    service = MemoryEligibilityService()

    candidate = MemoryCandidate(
        content="Can you explain binary search?",
        confidence=0.99,
    )

    assert not service.is_eligible(candidate)


def test_filter_returns_only_eligible():
    service = MemoryEligibilityService()

    candidates = [
        MemoryCandidate(
            content="User prefers Python.",
            confidence=0.95,
        ),
        MemoryCandidate(
            content="What is Python?",
            confidence=0.99,
        ),
    ]

    result = service.filter(candidates)

    assert len(result) == 1
    assert result[0].content == "User prefers Python."