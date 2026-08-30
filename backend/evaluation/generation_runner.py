import json
from pathlib import Path

from evaluation.generation import evaluate_answer
from evaluation.retriever import retrieve
from app.logging.logger import logger

CASES_PATH = (
    Path(__file__).parent
    / "generation_cases.json"
)


def load_generation_cases() -> list[dict]:

    with open(
        CASES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_context(
    results: list[dict],
) -> str:
    """
    Combine retrieved chunks into a single context string.
    """

    return "\n\n---\n\n".join(
        result["content"]
        for result in results
    )


def evaluate_generation(
    questions: list[dict],
    k: int = 5,
) -> dict:
    """
    Evaluate generation preparation using the
    retrieval pipeline.

    This function retrieves context for each question
    and evaluates the resulting context/answer setup.
    """

    results = []

    for question in questions:

        retrieved = retrieve(
            question["question"],
            top_k=k,
        )

        context = build_context(
            retrieved
        )

        expected_text = question.get(
            "expected_chunk_contains"
        )

        results.append(
            {
                "id": question["id"],
                "question": question["question"],
                "has_context": bool(context),
                "context": context,
                "expected_text": expected_text,
            }
        )

    return {
        "total_questions": len(questions),
        "results": results,
    }


def evaluate_generation_cases(
    cases: list[dict],
) -> dict:

    logger.info(
        "generation_evaluation_started cases=%d",
        len(cases),
    )
    results = []

    for case in cases:

        evaluation = evaluate_answer(
            answer=case["answer"],
            context=case["context"],
            expected_text=case["expected_answer"],
        )

        results.append(
            {
                "id": case["id"],
                "question": case["question"],
                **evaluation,
            }
        )

    total = len(results)

    answer_relevant = sum(
        result["answer_relevant"]
        for result in results
    )

    grounded = sum(
        result["grounded"]
        for result in results
    )

    report = {
        "total": total,
        "answer_relevance": (
            answer_relevant / total
            if total
            else 0.0
        ),
        "groundedness": (
            grounded / total
            if total
            else 0.0
        ),
        "results": results,
    }

    logger.info(
        "generation_evaluation_complete "
        "cases=%d "
        "answer_relevance=%.3f "
        "groundedness=%.3f",
        total,
        report["answer_relevance"],
        report["groundedness"],
    )

    return report


def print_report(report: dict):

    print("\nGeneration Evaluation")
    print("=" * 50)

    print(
        f"Questions: {report['total']}"
    )

    print(
        f"Answer relevance: "
        f"{report['answer_relevance']:.2%}"
    )

    print(
        f"Groundedness: "
        f"{report['groundedness']:.2%}"
    )

    print("\nCases")

    for result in report["results"]:

        print(
            f"{result['id']} | "
            f"relevant={result['answer_relevant']} | "
            f"grounded={result['grounded']} | "
            f"context={result['has_context']}"
        )

    failed = [
        result
        for result in report["results"]
        if not result["answer_relevant"]
        or not result["grounded"]
    ]

    print("\nFailures")

    if not failed:
        print("None")
        return

    for result in failed:
        print(
            f"{result['id']} | "
            f"relevant={result['answer_relevant']} | "
            f"grounded={result['grounded']} | "
            f"context={result['has_context']}"
        )





if __name__ == "__main__":

    cases = load_generation_cases()

    report = evaluate_generation_cases(
        cases
    )

    print_report(report)