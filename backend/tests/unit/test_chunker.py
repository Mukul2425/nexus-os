import pytest

from app.services.rag.chunker import chunk_text


from app.services.rag.chunker import chunk_text


def test_chunk_text():

    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) == 4

    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 1000
    assert len(chunks[2]) == 900
    assert len(chunks[3]) == 100

    assert chunks[0][-200:] == chunks[1][:200]
    assert chunks[1][-200:] == chunks[2][:200]

    

def test_empty_text():

    assert chunk_text("") == []


def test_invalid_overlap():

    with pytest.raises(ValueError):

        chunk_text(
            "hello",
            chunk_size=100,
            overlap=100,
        )