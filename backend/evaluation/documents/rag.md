# Retrieval Augmented Generation

Retrieval Augmented Generation, commonly called RAG, combines information
retrieval with language generation.

Nexus uses ChromaDB as its vector database.

Documents are loaded and divided into smaller chunks before being embedded.

Each chunk is converted into a vector representation using an embedding model.

The resulting vectors are stored in ChromaDB.

When a user asks a question, Nexus generates an embedding for the question.

The retriever searches the vector database for semantically similar chunks.

Nexus currently retrieves the top 5 chunks by default.

The retrieved chunks are filtered using a maximum distance threshold.

The relevant chunks are assembled into a context before being sent to the
language model.

Source attribution records the document name, chunk ID, and retrieval score
associated with retrieved information.

RAG allows the language model to answer questions using information retrieved
from the knowledge base rather than relying only on its internal knowledge.