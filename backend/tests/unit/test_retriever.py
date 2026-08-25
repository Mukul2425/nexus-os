from unittest.mock import patch


def test_retrieve_returns_chunks():

    fake_embedding = [0.1, 0.2, 0.3]

    fake_results = {
        "documents": [
            [
                "Nexus uses Gemini.",
                "Nexus has conversation management.",
            ]
        ],
        "metadatas": [
            [
                {
                    "document": "nexus.txt",
                    "document_id": "doc-123",
                    "chunk_id": 0,
                },
                {
                    "document": "nexus.txt",
                    "document_id": "doc-123",
                    "chunk_id": 1,
                },
            ]
        ],
        "distances": [
            [
                0.12,
                0.35,
            ]
        ],
    }

    with patch(
        "app.services.rag.retriever.embed_text",
        return_value=fake_embedding,
    ):

        with patch(
            "app.services.rag.retriever.search",
            return_value=fake_results,
        ):

            from app.services.rag.retriever import retrieve

            results = retrieve(
                "What is Nexus?",
                top_k=2,
            )

    assert len(results) == 2

    assert results[0]["content"] == (
        "Nexus uses Gemini."
    )

    assert results[0]["document"] == (
        "nexus.txt"
    )

    assert results[0]["chunk_id"] == 0

    assert results[0]["distance"] == 0.12

def test_retrieve_returns_empty_when_no_documents():

    fake_results = {
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    with patch(
        "app.services.rag.retriever.embed_text",
        return_value=[0.1, 0.2, 0.3],
    ):

        with patch(
            "app.services.rag.retriever.search",
            return_value=fake_results,
        ):

            from app.services.rag.retriever import retrieve

            results = retrieve(
                "Something unknown",
                top_k=5,
            )

    assert results == []