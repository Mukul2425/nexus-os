def answer_contains_expected(
    answer: str,
    expected_text: str | None,
) -> bool:
    if expected_text is None:
        return True

    return expected_text.lower() in answer.lower()


def is_grounded(
    answer: str,
    context: str,
) -> bool:
    if not answer.strip():
        return False

    if not context.strip():
        return False

    # Simple v0.7 baseline:
    # consider the answer grounded when at least one
    # meaningful sentence/phrase from the answer appears
    # in the retrieved context.
    answer_words = {
        word.strip(".,!?;:()[]{}").lower()
        for word in answer.split()
        if len(word.strip(".,!?;:()[]{}")) >= 4
    }

    context_words = {
        word.strip(".,!?;:()[]{}").lower()
        for word in context.split()
    }

    if not answer_words:
        return False

    overlap = answer_words & context_words

    return len(overlap) / len(answer_words) >= 0.3