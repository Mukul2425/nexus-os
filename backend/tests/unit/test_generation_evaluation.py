from evaluation.generation_runner import (
    evaluate_generation_cases,
)


def test_generation_evaluation_cases():

    cases = [
        {
            "id": "g1",
            "question": "Which database?",
            "context": "Nexus uses ChromaDB.",
            "answer": "Nexus uses ChromaDB.",
            "expected_answer": "ChromaDB",
        },
        {
            "id": "g2",
            "question": "Which database?",
            "context": "Nexus uses ChromaDB.",
            "answer": "Nexus uses Pinecone.",
            "expected_answer": "ChromaDB",
        },
    ]

    report = evaluate_generation_cases(
        cases
    )

    assert report["total"] == 2
    assert report["answer_relevance"] == 0.5
    assert report["groundedness"] == 0.5