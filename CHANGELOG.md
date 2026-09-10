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



### [v0.9.0] — Memory Foundation
## Added
## Memory Model
-   Added SQLAlchemy Memory model.
-   Added UUID-based memory IDs.
-   Added memory content.
-   Added semantic and episodic memory types.
-   Added importance scores from 1–5.
-   Added creation and update timestamps.
-   Added database indexes.
-   Added SQLite memories table.
##  Memory CRUD API
##   Added:
-   POST   /memories
-   GET    /memories
-   GET    /memories/{id}
-   PATCH  /memories/{id}
-   DELETE /memories/{id}
##   Also added:
-   Pagination.
-   Input validation.
-   Invalid-memory handling.
-   Memory-not-found handling.
-   Nexus exception integration.
-   Standardized API errors.
-   Automatic Memory Extraction
##  Added:
-  MemoryCandidate.
-   MemoryExtractionResult.
-   LLM-based memory extraction.
-   Confidence scores.
-   Importance scores.
-   Semantic/episodic classification.
-   Extraction of explicit user information.
-   Extraction of persistent preferences.
-   Extraction of useful project/user information.
-   Malformed LLM response handling.
-   Memory Eligibility
##   Added filtering for:
-  Low-confidence candidates.
-   Blank memories.
-   Invalid memory types.
-   Ordinary questions.
-   Temporary requests.
-   Greetings.
-   Small talk.
-   Assistant-inferred information.
-   Memory Deduplication
##   Added:
-  Whitespace normalization.
-   Case normalization.
-   Punctuation normalization.
-   Repeated-whitespace normalization.
-   Duplicate detection.
-   Duplicate persistence prevention.
-   Vector Memory Store
-   Added a dedicated ChromaDB memory collection.
-   The memory vector layer supports:
-   Embedding generation.
-   Memory vector storage.
-   Memory metadata.
-   SQLite memory ID references.
-   Vector updates.
-   Vector deletion.
-   Semantic search.
-   Distance-based filtering.
-   SQLite remains the authoritative source for persisted memory records.
-   Conflict Detection
##  Added:
-  Related-memory retrieval.
-   Semantic conflict detection.
-   LLM-based contradiction classification.
-   Failure-safe conflict detection.
 
   Example:
    "I prefer Python."

    vs.

    "I prefer TypeScript instead of Python."
    can be identified as a potential conflict.

    Automatic conflict resolution is intentionally deferred.
    Memory Retrieval
##   Added:
    MemoryRetriever.
    Semantic search.
    Configurable top-K.
    Distance thresholds.
    Stale-vector handling.
    SQLite source-of-truth lookup.
    Retrieval latency logging.
    Retrieval lifecycle logging.
    Chat Integration
    Memory is now integrated into:
    POST /chat
    POST /chat/stream
    The chat pipeline can:
    Retrieve relevant memories.
    Build memory context.
    Combine memory with conversation and RAG context.
    Generate the response.
    Extract new memories after response generation.
    Memory failures are isolated from normal chat execution.
    Compatibility
    Verified compatibility with:
    Conversation history.
    RAG.
    Tool calling.
    Streaming.
    Existing provider abstraction.
    Existing exception handling.
    Existing observability.
    Testing
    Expanded the test suite across memory functionality.
    Final result:
    108 passed
    Changed
    Conversation context now supports relevant persistent memories.
    Chat requests can use long-term memory in addition to conversation history and RAG.
    Memory extraction occurs after response generation.
    Memory indexing is best-effort so vector-store failures do not invalidate successful SQLite CRUD operations.
    Reliability
    Memory functionality was designed with failure isolation:
    Memory Retrieval Failure
            ↓
        Log Error
            ↓
    Continue Chat
    Memory Extraction Failure
            ↓
        Log Error
            ↓
    Continue Chat
    This prevents optional memory functionality from becoming a single point of failure for the core chat pipeline.
    Deferred
    The following is intentionally deferred:
    Automatic Conflict Resolution
    The system currently detects potential conflicts but does not automatically replace or update an existing memory when a contradiction is detected.
    This will be reconsidered when memory behavior is extended in future versions.
    Validation
    The v0.9 implementation was validated through:
    Automated test suite.
    SQLite persistence checks.
    Manual memory creation.
    ChromaDB indexing checks.
    Extraction-path validation.
    Failure-path validation.
    Chat integration tests.
    Streaming integration tests.
    RAG compatibility tests.
    Tool compatibility tests.