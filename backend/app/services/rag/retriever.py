from app.services.rag.embeddings import embed_text
from app.services.rag.vector_store import search


def retrieve(
    question: str,
    top_k: int = 5,
):

    question_embedding = embed_text(
        question
    )

    results = search(
        question_embedding,
        top_k,
    )

    documents = results.get(
        "documents",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    distances = results.get(
        "distances",
        [[]],
    )[0]

    retrieved = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):

        retrieved.append(
            {
                "content": document,
                "document": metadata["document"],
                "chunk_id": metadata["chunk_id"],
                "score": distance,
            }
        )

    return retrieved