# nexus-os
## Features

### Backend

- FastAPI-based REST API
- Conversation management
- Persistent conversation history
- UUID-based conversations
- SQLite database
- SQLAlchemy ORM

### LLM

- Gemini integration
- Prompt management
- Multi-turn conversations
- Streaming responses
- Provider-isolated LLM layer

## [0.5.0] — LLM Provider Abstraction

- Introduced LLMProvider abstraction.
- Added GeminiProvider implementation.
- Added provider factory.
- Added configuration-based provider selection.
- Added provider-level streaming abstraction.
- Isolated Gemini-specific implementation from ConversationService.
- Added provider unit and integration tests.


### Reliability

- Environment-based configuration
- Pydantic Settings
- Custom application exceptions
- Global API exception handling
- Safe and consistent error responses
- Request ID tracking
- Structured application logging
- LLM latency and failure logging

### Testing

- Pytest test suite
- Unit tests
- Integration tests
- Isolated SQLite test database
- Mocked LLM provider calls
- API error handling tests

## v0.6.0 — RAG Foundation

**Status: ✅ Complete**

> Note: Nexus does not manually calculate cosine similarity. Vector similarity/distance is handled by the vector store.

### Implementation

- [x] Document loader
- [x] Text chunker
- [x] Embedding generation
- [x] Persistent vector store using ChromaDB
- [x] Retrieval service
- [x] RAG context assembly
- [x] RAG integration with ConversationService
- [x] Document ingestion API
- [x] Source attribution
- [x] RAG error handling

### Testing

- [x] Chunking tests
- [x] Retrieval tests
- [x] RAG prompt tests
- [x] Document API tests
- [x] Chat/API integration tests
- [x] RAG failure-case coverage

### Observability

- [x] Retrieval latency
- [x] Number of chunks retrieved
- [x] Retrieval distances
- [x] RAG error logging

### Deliberately deferred

- [ ] Explicit token/context budgeting
- [ ] Reranking
- [ ] Hybrid search
- [ ] Query rewriting
- [ ] Multi-query retrieval
- [ ] Advanced document formats
- [ ] RAG evaluation framework