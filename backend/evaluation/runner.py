import json
from pathlib import Path

from app.services.rag.retriever import retrieve

from evaluation.metrics.retrieval import hit_at_k


QUESTIONS_PATH = (
    Path(__file__).parent / "questions.json"
)


def load_questions() -> list[dict]:
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_retrieval(
    questions: list[dict],
    k: int,
) -> dict:
    total = len(questions)
    hits = 0
    results = []

    for question in questions:
        retrieved = retrieve(
            question["question"],
            top_k=k,
        )

        hit = hit_at_k(
            results=retrieved,
            expected_source=question["expected_source"],
            expected_chunk_contains=question[
                "expected_chunk_contains"
            ],
            k=k,
        )

        if hit:
            hits += 1

        results.append(
            {
                "id": question["id"],
                "question": question["question"],
                "hit": hit,
                "expected_source": question[
                    "expected_source"
                ],
                "retrieved": [
                    {
                        "document": item["document"],
                        "chunk_id": item["chunk_id"],
                        "distance": item["distance"],
                    }
                    for item in retrieved[:k]
                ],
            }
        )

    return {
        "total_questions": total,
        "hits": hits,
        "hit_at_k": hits / total if total else 0.0,
        "results": results,
    }


def run_evaluation(
    k_values: list[int] | None = None,
):
    if k_values is None:
        k_values = [1, 3, 5]

    questions = load_questions()

    reports = {}

    for k in k_values:
        reports[k] = evaluate_retrieval(
            questions,
            k,
        )

    return reports


def print_report(
    reports: dict,
):
    print("\nRetrieval Evaluation")
    print("=" * 40)

    for k, report in reports.items():
        print(
            f"Hit@{k}: "
            f"{report['hit_at_k']:.2%} "
            f"({report['hits']}/{report['total_questions']})"
        )

    print()


if __name__ == "__main__":
    reports = run_evaluation(
        k_values=[1, 3, 5]
    )

    print_report(reports)