from app.services.rag.retriever import retrieve


def build_rag_context(
    question: str,
    top_k: int = 5,
    max_distance: float = 0.3,
):
    results = retrieve(
        question,
        top_k=top_k,
    )

    relevant = [
        result
        for result in results
        if result["distance"] <= max_distance
    ]

    if not relevant:
        return "", []

    context_parts = []

    for result in relevant:
        context_parts.append(
            f"[Source: {result['document']} "
            f"chunk {result['chunk_id']}]\n"
            f"{result['content']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    sources = [
        {
            "document": result["document"],
            "document_id": result["document_id"],
            "chunk_id": result["chunk_id"],
            "distance": result["distance"],
        }
        for result in relevant
    ]

    return context, sources