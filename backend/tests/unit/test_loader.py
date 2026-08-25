import pytest

from app.services.rag.loader import load_document


def test_load_txt():

    content = b"Hello Nexus"

    result = load_document(
        "test.txt",
        content,
    )

    assert result == "Hello Nexus"


def test_load_markdown():

    content = b"# Nexus"

    result = load_document(
        "test.md",
        content,
    )

    assert result == "# Nexus"


def test_unsupported_document():

    with pytest.raises(ValueError):

        load_document(
            "test.pdf",
            b"content",
        )


def test_invalid_encoding():

    with pytest.raises(ValueError):

        load_document(
            "test.txt",
            b"\xff\xfe",
        )