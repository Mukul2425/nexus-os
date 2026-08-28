from pathlib import Path

from app.services.rag.chunker import chunk_text
from app.services.rag.embeddings import embed_documents
from app.services.rag.loader import load_document

from evaluation.vector_store import (
    add_chunks,
    reset_collection,
)


DOCUMENTS_DIR = (
    Path(__file__).parent / "documents"
)


def ingest_evaluation_documents(
    chunk_size: int = 1000,
    overlap: int = 200,
):
    reset_collection()

    documents = sorted(
        DOCUMENTS_DIR.glob("*.md")
    )

    for path in documents:

        content = load_document(
            path.name,
            path.read_bytes(),
        )

        chunks = chunk_text(
            content,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        if not chunks:
            continue

        embeddings = embed_documents(
            chunks
        )

        add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_name=path.name,
        )

        print(
            f"Ingested {path.name}: "
            f"{len(chunks)} chunks"
        )


if __name__ == "__main__":
    ingest_evaluation_documents()