import json
from pathlib import Path

from evaluation.generation import evaluate_answer
from evaluation.retriever import retrieve


QUESTIONS_PATH = (
    Path(__file__).parent / "questions.json"
)


def load_questions() -> list[dict]:

    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_context(
    results: list[dict],
) -> str:

    return "\n\n".join(
        result["content"]
        for result in results
    )


def evaluate_generation(
    questions: list[dict],
    k: int = 3,
) -> dict:

    results = []

    for question in questions:

        retrieved = retrieve(
            question["question"],
            top_k=k,
        )

        context = build_context(
            retrieved
        )

        # We intentionally don't call Gemini here.
        # Generation evaluation needs a supplied answer.
        results.append(
            {
                "id": question["id"],
                "question": question["question"],
                "expected": question[
                    "expected_chunk_contains"
                ],
                "context_available": bool(
                    context.strip()
                ),
            }
        )

    return {
        "total_questions": len(results),
        "results": results,
    }


def print_report(report: dict):

    print("\nGeneration Evaluation Preparation")
    print("=" * 50)

    print(
        f"Questions: "
        f"{report['total_questions']}"
    )

    with_context = sum(
        result["context_available"]
        for result in report["results"]
    )

    print(
        f"Questions with retrieved context: "
        f"{with_context}/"
        f"{report['total_questions']}"
    )


if __name__ == "__main__":

    questions = load_questions()

    report = evaluate_generation(
        questions,
        k=3,
    )

    print_report(report)