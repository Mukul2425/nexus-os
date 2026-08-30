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


## v0.7.0 — RAG Quality & Evaluation

**Status: ✅ Complete**

### RAG Evaluation Theory

- [x] Retrieval vs generation evaluation
- [x] Precision
- [x] Recall
- [x] Hit@K
- [x] Context relevance
- [x] Answer relevance
- [x] Faithfulness / groundedness
- [x] Hallucination
- [x] LLM-as-a-judge concepts

### Evaluation Dataset

- [x] Versioned evaluation documents
- [x] 20 evaluation questions
- [x] Expected sources
- [x] Expected information
- [x] Missing-answer cases
- [x] Similar-but-wrong cases
- [x] Cross-document questions

### Retrieval Evaluation

- [x] Retrieval evaluation runner
- [x] Hit@1
- [x] Hit@3
- [x] Hit@5
- [x] Hit@10
- [x] Retrieval failure inspection

### RAG Experiments

- [x] Top-K experiment
- [x] Chunk-size experiment
- [x] Baseline configuration
- [x] Retrieval result comparison

### Generation Evaluation

- [x] Answer relevance
- [x] Groundedness
- [x] Context availability
- [x] Hallucination detection
- [x] No-context behavior
- [x] Generation failure analysis

### Observability

- [x] Evaluation run logging
- [x] Retrieval metrics logging
- [x] Generation metrics logging
- [x] Failure-case reporting

### Testing

- [x] Retrieval metric tests
- [x] Hit@K tests
- [x] Evaluation runner tests
- [x] Generation metric tests
- [x] Generation runner tests
- [x] RAG regression tests
- [x] Existing API regression tests

### v0.7.0 Baseline

| Configuration | Value |
|---|---|
| Vector Store | ChromaDB |
| Embedding | Gemini embedding model |
| Chunk Size | 512 |
| Chunk Overlap | 100 |
| Top-K | 3 |
| Hit@1 | 83.33% |
| Hit@3 | 100% |
| Hit@5 | 100% |
| Hit@10 | 100% |
| Answer Relevance | 80% |
| Groundedness | 60% |

> Generation metrics are deterministic baseline metrics for learning and regression testing. They should not be interpreted as production-grade semantic evaluation.

### Deferred

- [ ] Advanced LLM-as-a-judge evaluation
- [ ] Ragas / DeepEval integration
- [ ] Reranking
- [ ] Hybrid search
- [ ] Query rewriting
- [ ] Advanced retrieval strategies