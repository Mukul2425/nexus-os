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


## [0.7.0] — RAG Quality & Evaluation

### Added

- Added versioned RAG evaluation dataset.
- Added retrieval evaluation pipeline.
- Added Hit@1, Hit@3, Hit@5 and Hit@10 metrics.
- Added retrieval failure inspection.
- Added Top-K experiments.
- Added chunk-size experiments.
- Added generation evaluation pipeline.
- Added answer relevance evaluation.
- Added groundedness evaluation.
- Added hallucination and no-context regression cases.
- Added evaluation observability.
- Added RAG regression tests.

### Baseline

- Chunk size: 512
- Chunk overlap: 100
- Top-K: 3
- Hit@1: 83.33%
- Hit@3: 100%
- Hit@5: 100%
- Hit@10: 100%
- Answer relevance: 80%
- Groundedness: 60%

### Testing

- 43 tests passed.
- 3 dependency warnings.
- No test failures.


### [0.8.0] — Tool Calling & MCP Foundation ✅
### Core Architecture
- Tool abstraction
-   Provider-neutral tool definitions
-    Provider-neutral tool calls
-    Provider-neutral tool results
-    Structured LLM responses
-    Tool Infrastructure
-    Tool registry
-    Tool factory
-    Tool executor
-    Shared registry architecture
-    Built-in Tools
-    Calculator tool
-    Time tool
-    LLM Integration
-    Gemini function/tool calling
-    Tool definitions sent to provider
-    Provider-specific responses converted into provider-neutral schemas
-    Conversation Tool Loop
-    Tool-call detection
-    Tool execution
-    Tool result handling
-    Multi-step tool execution
-    Failed tool recovery
-    Maximum tool-call protection
-    MAX_TOOL_CALLS = 5
-    Integration
-   RAG preserved
-    Conversation history preserved
-    Message persistence preserved
-    Existing chat API preserved
-    Existing text streaming preserved
### Testing
-    64 passed
-    3 warnings


### Deferred from v0.8.0
-    Tool-Aware Streaming ⏳
###  Current streaming interface:
-    AsyncGenerator[str, None]
-    Current implementation only supports text deltas.
-    Tool-aware streaming requires a structured event architecture capable of representing:
-    text_delta
-    tool_call_started
-    tool_call_arguments_delta
-    tool_call_completed
-    tool_result
-    generation_resumed
-    error
-    This feature is intentionally deferred rather than forced into the existing string-based streaming interface.