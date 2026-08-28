def hit_at_k(
    results: list[dict],
    expected_source: str | None,
    expected_chunk_contains: str | None,
    k: int,
) -> bool:
    """
    Return True if the expected information appears
    within the top-k retrieved results.
    """

    if expected_source is None:
        return False

    for result in results[:k]:
        if result["document"] != expected_source:
            continue

        if expected_chunk_contains is None:
            return True

        if expected_chunk_contains.lower() in result["content"].lower():
            return True

    return False