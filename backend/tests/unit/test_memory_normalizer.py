from app.services.memory.normalizer import (
    normalize_memory_content,
)


def test_normalize_memory_content():
    assert (
        normalize_memory_content(
            "  I   prefer Python!  "
        )
        == "i prefer python"
    )


def test_normalize_memory_content_case_insensitive():
    assert (
        normalize_memory_content(
            "User Prefers Python."
        )
        == normalize_memory_content(
            "user prefers python"
        )
    )