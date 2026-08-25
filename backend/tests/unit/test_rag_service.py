from unittest.mock import patch


def test_ingest_document():

    with patch(
        "app.services.rag.service.load_document",
        return_value="Nexus uses Gemini.",
    ):

        with patch(
            "app.services.rag.service.chunk_text",
            return_value=[
                "Nexus uses Gemini."
            ],
        ):

            with patch(
                "app.services.rag.service.embed_documents",
                return_value=[
                    [0.1, 0.2, 0.3]
                ],
            ):

                with patch(
                    "app.services.rag.service.add_chunks"
                ) as mock_add:

                    from app.services.rag.service import (
                        ingest_document,
                    )

                    result = ingest_document(
                        "nexus.txt",
                        b"Nexus uses Gemini.",
                    )

    assert result == {
        "document": "nexus.txt",
        "chunks": 1,
    }

    mock_add.assert_called_once()