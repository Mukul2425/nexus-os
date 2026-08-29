from evaluation.generation_runner import (
    build_context,
    evaluate_generation,
)


def test_build_context():

    results = [
        {
            "content": "Nexus uses ChromaDB.",
        },
        {
            "content": "Nexus uses Gemini.",
        },
    ]

    context = build_context(results)

    assert "Nexus uses ChromaDB." in context
    assert "Nexus uses Gemini." in context


def test_generation_evaluation():

    questions = [
        {
            "id": "q1",
            "question": "Which vector database?",
            "expected_chunk_contains": "ChromaDB",
        }
    ]

    report = evaluate_generation(
        questions,
        k=3,
    )

    assert report["total_questions"] == 1
    assert len(report["results"]) == 1