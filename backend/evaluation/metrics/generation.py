import re


def _normalize(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[^\w\s]", "", text.lower()),
    ).strip()


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

    normalized_answer = _normalize(answer)
    normalized_context = _normalize(context)

    # Strong baseline:
    # the complete normalized answer must be
    # supported by the retrieved context.
    if normalized_answer in normalized_context:
        return True

    # For longer answers, check whether the answer's
    # individual sentences are supported by context.
    sentences = [
        _normalize(sentence)
        for sentence in re.split(
            r"[.!?]+",
            answer,
        )
        if sentence.strip()
    ]

    if not sentences:
        return False

    grounded_sentences = sum(
        sentence in normalized_context
        for sentence in sentences
    )

    return (
        grounded_sentences / len(sentences)
        >= 0.5
    )