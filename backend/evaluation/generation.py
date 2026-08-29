from evaluation.metrics.generation import (
    answer_contains_expected,
    is_grounded,
)


def evaluate_answer(
    answer: str,
    context: str,
    expected_text: str | None,
) -> dict:

    return {
        "answer_relevant": answer_contains_expected(
            answer,
            expected_text,
        ),
        "grounded": is_grounded(
            answer,
            context,
        ),
        "has_context": bool(context.strip()),
    }