from app.prompts.rag import build_rag_prompt
from app.services.rag.context import build_rag_context


def prepare_rag_question(
    question: str,
    top_k: int = 5,
):
    context, sources = build_rag_context(
        question,
        top_k=top_k,
    )

    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    return {
        "prompt": prompt,
        "sources": sources,
    }