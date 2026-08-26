from time import perf_counter

from app.services.rag.embeddings import embed_text
from app.services.rag.vector_store import search

from app.logging.context import get_request_id
from app.logging.logger import logger


def retrieve(
    question: str,
    top_k: int = 5,
) -> list[dict]:

    request_id = get_request_id()

    start = perf_counter()

    logger.info(
        "rag_retrieval_started "
        "request_id=%s "
        "top_k=%d",
        request_id,
        top_k,
    )

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
                "document_id": metadata["document_id"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance,
            }
        )

    latency = perf_counter() - start

    logger.info(
        "rag_retrieval_complete "
        "request_id=%s "
        "documents_retrieved=%d "
        "latency=%.3fs",
        request_id,
        len(retrieved),
        latency,
    )

    return retrieved