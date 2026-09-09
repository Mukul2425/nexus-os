import hashlib

import chromadb

from app.services.rag.embeddings import embed_text


client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="nexus_memories"
)


def _memory_id(memory_id: str) -> str:
    return hashlib.sha256(
        memory_id.encode("utf-8")
    ).hexdigest()[:16]


def add_memory(
    memory_id: str,
    content: str,
    memory_type: str,
    importance: int,
):
    vector_id = _memory_id(memory_id)

    embedding = embed_text(content)

    collection.upsert(
        ids=[vector_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[
            {
                "memory_id": memory_id,
                "memory_type": memory_type,
                "importance": importance,
            }
        ],
    )


def update_memory(
    memory_id: str,
    content: str,
    memory_type: str,
    importance: int,
):
    add_memory(
        memory_id=memory_id,
        content=content,
        memory_type=memory_type,
        importance=importance,
    )


def delete_memory(memory_id: str):
    vector_id = _memory_id(memory_id)

    collection.delete(
        ids=[vector_id]
    )


def search_memories(
    query: str,
    top_k: int = 5,
):
    embedding = embed_text(query)

    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )