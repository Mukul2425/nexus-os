from app.services.rag.embeddings import embed_text

from evaluation.vector_store import search


def retrieve(
    question: str,
    top_k: int = 5,
):
    embedding = embed_text(question)

    results = search(
        embedding,
        top_k=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

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
                "document_id": metadata["document_id"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance,
            }
        )

    return retrieved