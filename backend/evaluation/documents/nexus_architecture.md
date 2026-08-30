# Nexus Architecture

Nexus is an AI backend designed around a conversational RAG architecture.

The backend is implemented using FastAPI.

Nexus manages conversations through a conversation service and stores
conversation data using a repository layer.

The chat flow accepts a conversation ID and a user message.

The conversation service retrieves relevant information before generating
an answer from the language model.

Nexus supports streaming chat responses through a dedicated streaming endpoint.

The backend separates API, service, repository, provider, and RAG responsibilities.

The application exposes a document ingestion endpoint at /documents.

The application exposes a conversation creation endpoint at /conversation.

The application exposes a chat endpoint at /chat.