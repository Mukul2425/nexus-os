from unittest.mock import MagicMock

from app.services.memory.extractor import MemoryExtractor


def test_extracts_memories():
    provider = MagicMock()

    provider.generate.return_value = """
    {
        "memories": [
            {
                "content": "User prefers Python.",
                "memory_type": "semantic",
                "importance": 4,
                "confidence": 0.98
            }
        ]
    }
    """

    extractor = MemoryExtractor(provider)

    result = extractor.extract(
        "I prefer Python."
    )

    assert len(result) == 1
    assert result[0].content == (
        "User prefers Python."
    )

    provider.generate.assert_called_once()


def test_extractor_handles_invalid_json():
    provider = MagicMock()

    provider.generate.return_value = (
        "not valid json"
    )

    extractor = MemoryExtractor(provider)

    result = extractor.extract(
        "I prefer Python."
    )

    assert result == []