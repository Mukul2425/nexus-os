import hashlib

import chromadb


client = chromadb.PersistentClient(
    path="./evaluation/chroma_data"
)

collection = client.get_or_create_collection(
    name="nexus_evaluation"
)


def _document_id(document_name: str) -> str:
    return hashlib.sha256(
        document_name.encode("utf-8")
    ).hexdigest()[:16]


def reset_collection():
    global collection

    try:
        client.delete_collection(
            name="nexus_evaluation"
        )
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="nexus_evaluation"
    )


def add_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    document_name: str,
):
    document_id = _document_id(document_name)

    ids = [
        f"{document_id}-{index}"
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "document": document_name,
                "document_id": document_id,
                "chunk_id": index,
            }
            for index in range(len(chunks))
        ],
    )


def search(
    embedding: list[float],
    top_k: int = 5,
):
    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )