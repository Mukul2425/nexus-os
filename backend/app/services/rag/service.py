from app.services.rag.loader import load_document
from app.services.rag.chunker import chunk_text
from app.services.rag.embeddings import embed_documents
from app.services.rag.vector_store import add_chunks


def ingest_document(
    filename: str,
    content: bytes,
):

    text = load_document(
        filename,
        content,
    )

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "Document contains no readable text"
        )

    embeddings = embed_documents(
        chunks
    )

    add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_name=filename,
    )

    return {
        "document": filename,
        "chunks": len(chunks),
    }