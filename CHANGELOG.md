v0.1.0
## Unreleased

### Added

- Backend project structure
- FastAPI setup
- Initial API endpoint

### Added

- Chat endpoint
- Request and response schemas
- LLM service abstraction

### Added

- Gemini API integration
- Environment-based configuration
- LLM service implementation

## v0.3.0 - Logging & Observability

### Added
- FastAPI backend
- Swagger documentation
- Chat endpoint
- Gemini integration
- Multi-turn conversations
- Session Memory Management
- Logging 

## [0.4.0] - Production Hardening

### Added

- Centralized application configuration using Pydantic Settings.
- Environment-based configuration support.
- `.env.example` for development setup.
- Application-level exception hierarchy.
- Global FastAPI exception handler.
- Standardized API error responses.
- Request IDs in error responses.
- Gemini provider error handling.
- LLM failure and latency logging.
- Streaming LLM error handling.
- Pytest-based automated testing infrastructure.
- Unit tests for configuration, exceptions, conversation service, and prompts.
- Integration tests for chat, conversation, and error APIs.
- SQLite-based isolated test database.
- Mocked LLM provider calls for deterministic tests.

### Improved

- Internal provider errors are no longer exposed directly to API clients.
- Conversation errors now return appropriate HTTP status codes.
- Configuration and error handling are separated from business logic.
- Backend reliability improved through automated regression testing.

### Testing

- 11 tests passing.


## [0.5.0] — LLM Provider Abstraction

### Added

- Introduced LLMProvider abstraction.
- Added GeminiProvider implementation.
- Added provider factory.
- Added configuration-based provider selection.
- Added provider-level streaming abstraction.
- Isolated Gemini-specific implementation from ConversationService.
- Added provider unit and integration tests.

### Testing

- 16 tests passing.
- 2 dependency warnings.


## [0.6.0] — RAG Foundation

### Added

- Added document ingestion pipeline.
- Added text chunking.
- Added Gemini embedding generation.
- Added persistent ChromaDB vector store.
- Added semantic retrieval with configurable Top-K retrieval.
- Added RAG context assembly.
- Integrated retrieval into the conversation flow.
- Added document ingestion API.
- Added source attribution for retrieved context.
- Added retrieval distance information.
- Added RAG-specific observability.

### Testing

- Added chunking tests.
- Added retrieval tests.
- Added RAG prompt tests.
- Added document API tests.
- Added RAG integration and failure-case tests.

### Testing

- 27 tests passing.
- 3 dependency warnings.