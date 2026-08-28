from unittest.mock import patch

from evaluation.retriever import retrieve


def test_evaluation_retriever_returns_chunks():

    fake_results = {
        "documents": [
            [
                "Nexus uses ChromaDB."
            ]
        ],
        "metadatas": [
            [
                {
                    "document": "rag.md",
                    "document_id": "doc-123",
                    "chunk_id": 0,
                }
            ]
        ],
        "distances": [
            [
                0.12
            ]
        ],
    }

    with patch(
        "evaluation.retriever.embed_text",
        return_value=[0.1, 0.2, 0.3],
    ):

        with patch(
            "evaluation.retriever.search",
            return_value=fake_results,
        ):

            results = retrieve(
                "Which vector database does Nexus use?",
                top_k=1,
            )

    assert len(results) == 1

    assert results[0]["document"] == "rag.md"

    assert results[0]["chunk_id"] == 0

    assert results[0]["content"] == (
        "Nexus uses ChromaDB."
    )

    assert results[0]["distance"] == 0.12