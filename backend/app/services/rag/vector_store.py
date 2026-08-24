import chromadb


client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="nexus_documents"
)

def add_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    document_name: str,
):
    
    ids = [
        f"{document_name}-{index}"
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "document": document_name,
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