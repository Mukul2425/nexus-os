from unittest.mock import patch

from evaluation.runner import evaluate_retrieval


def test_evaluate_retrieval_calculates_hit_at_k():

    questions = [
        {
            "id": "q01",
            "question": "Which vector database does Nexus use?",
            "expected_source": "rag.md",
            "expected_chunk_contains": "ChromaDB",
            "type": "easy",
        },
        {
            "id": "q02",
            "question": "Which framework does Nexus use?",
            "expected_source": "nexus_architecture.md",
            "expected_chunk_contains": "FastAPI",
            "type": "easy",
        },
    ]

    fake_results = {
        "Which vector database does Nexus use?": [
            {
                "document": "rag.md",
                "chunk_id": 0,
                "content": "Nexus uses ChromaDB.",
                "distance": 0.1,
            }
        ],
        "Which framework does Nexus use?": [
            {
                "document": "wrong.md",
                "chunk_id": 0,
                "content": "Nexus uses something else.",
                "distance": 0.1,
            }
        ],
    }

    def fake_retrieve(question, top_k):
        return fake_results[question]

    with patch(
        "evaluation.runner.retrieve",
        side_effect=fake_retrieve,
    ):
        report = evaluate_retrieval(
            questions,
            k=1,
        )

    assert report["total_questions"] == 2
    assert report["hits"] == 1
    assert report["hit_at_k"] == 0.5

    assert report["results"][0]["hit"] is True
    assert report["results"][1]["hit"] is False