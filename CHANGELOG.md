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
-  MemoryRetriever.
-  Semantic search.
-  Configurable top-K.
-  Distance thresholds.
-  Stale-vector handling.
-  SQLite source-of-truth lookup.
-  Retrieval latency logging.
-  Retrieval lifecycle logging.
-  Chat Integration
-  Memory is now integrated into:
-  POST /chat
-  POST /chat/stream
-  The chat pipeline can:
-  Retrieve relevant memories.
-  Build memory context.
-  Combine memory with conversation and RAG context.
-  Generate the response.
-  Extract new memories after response generation.
-  Memory failures are isolated from normal chat execution.
-  Compatibility
-  Verified compatibility with:
-  Conversation history.
-  RAG.
-  Tool calling.
-  Streaming.
-  Existing provider abstraction.
-  Existing exception handling.
-  Existing observability.
-  Testing
-  Expanded the test suite across memory functionality.
##  Final result:
-  108 passed
-  Changed
-  Conversation context now supports relevant persistent memories.
-  Chat requests can use long-term memory in addition to conversation history and RAG.
-  Memory extraction occurs after response generation.
-  Memory indexing is best-effort so vector-store failures do not invalidate successful SQLite CRUD operations.
-  Reliability
-  Memory functionality was designed with failure isolation:
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


# Changelog

All notable changes to Nexus OS are documented here.

---

## [1.0.0] — Agentic Orchestration

### Added

#### Agent Core

* Introduced `AgentService` for agent orchestration.
* Added explicit `AgentState`.
* Added `AgentStep`.
* Added `AgentResult`.
* Added agent execution statuses.
* Added controlled agent execution lifecycle.
* Separated agent orchestration from `ConversationService`.

#### Agent Execution Loop

* Added multi-step agent execution loop.
* Added sequential action execution.
* Added observation → next-action flow.
* Added agent-controlled termination.
* Added configurable maximum execution steps.
* Added infinite-loop protection.
* Added multi-step execution support.

#### Tool Integration

* Agent receives available tool definitions.
* Added agent-driven tool selection.
* Added tool argument handling.
* Added tool execution through the existing tool infrastructure.
* Added tool result feedback to the agent.
* Added support for multiple tool calls within an execution.
* Added unknown-tool protection.
* Added invalid-argument handling.
* Added tool failure handling.
* Added unnecessary tool usage evaluation.

#### RAG Integration

* Agent can invoke RAG retrieval.
* Retrieved documents are available as agent observations.
* Agent can continue execution after retrieval.
* Existing RAG source attribution is preserved.
* Added RAG relevance handling during agent execution.
* RAG failures are isolated from the overall agent execution.
* Added agent-level RAG evaluation.

#### Memory Integration

* Agent can retrieve relevant persistent memories.
* Retrieved memories are available as agent context.
* Agent can use memory during task execution.
* Existing memory safety rules are preserved.
* Memory failures are isolated from agent execution.
* Integrated persistent memory into the agent execution flow.
* Added stale-memory/vector protection.
* Added agent-level memory evaluation.

#### Task Planning

* Added lightweight task planning.
* Tasks can be represented as execution steps.
* Added short-plan generation.
* Added sequential plan execution.
* Added completed-step tracking.
* Added failed-step tracking.
* Added plan progress tracking.
* Added plan length limitations.
* Added plan termination.
* Preserved agent state across execution steps.

#### Execution Safety

* Added `MAX_AGENT_STEPS`.
* Added `MAX_TOOL_CALLS`.
* Added configurable execution timeout.
* Added invalid-action handling.
* Added unknown-tool protection.
* Added malformed agent-response handling.
* Added invalid tool-argument handling.
* Added repeated-action / loop protection.
* Added controlled agent termination.
* Added configurable execution safety limits.

#### Agent State

Agent execution state now tracks:

* Task
* Conversation ID
* Current step
* Plan
* Observations
* Tool calls
* Retrieved memories
* Retrieved documents
* Execution status
* Final response
* Step history
* Plan progress

#### Agent API

Added:

* `POST /agent/run`
* Agent request schema
* Agent response schema
* Execution ID
* Execution metadata
* Agent-specific error handling
* Request validation

Existing APIs remain available:

* `POST /chat`
* `POST /chat/stream`

#### Agent Observability

Added agent execution lifecycle logging:

* `agent_execution_started`
* `agent_step_started`
* `agent_action_selected`
* `agent_tool_execution_started`
* `agent_tool_execution_complete`
* `agent_observation_received`
* `agent_step_complete`
* `agent_execution_complete`
* `agent_execution_failed`
* `agent_max_steps_reached`

Added tracking for:

* Execution ID
* Request ID
* Conversation ID
* Step number
* Execution latency
* Tool-call count
* Final execution status

Sensitive information is not unnecessarily included in agent logs.

#### Failure & Recovery

Added handling for:

* LLM failures
* Tool failures
* RAG failures
* Memory failures
* Invalid actions
* Invalid arguments
* Maximum-step failures
* Execution timeouts
* Malformed agent responses

Optional systems such as RAG and memory are isolated so their failures do not unnecessarily terminate the entire agent execution.

#### Agent Evaluation

Added:

```text
evaluation/agent/tasks.json
```

Evaluation coverage includes:

* Direct-answer tasks
* Tool tasks
* RAG tasks
* Memory tasks
* Multi-step tasks
* Mixed-capability tasks

Added live `AgentService` evaluation with:

* Provider failure handling
* Evaluation fail-fast behavior
* Stale-memory handling
* Evaluation report generation

#### Evaluation Metrics

Added evaluation for:

* Task success rate
* Tool-selection accuracy
* Tool-execution success
* Unnecessary tool calls
* Average execution steps
* Maximum-step failures
* Final answer relevance
* Answer groundedness
* Numeric answer normalization
* Multi-tool execution

### Improved

* Nexus can now execute controlled multi-step tasks instead of only performing single-turn LLM/tool interactions.
* Tool calling is now orchestrated by an agent execution loop.
* RAG and persistent memory can participate in agent execution.
* Agent state is explicitly tracked across multiple execution steps.
* Agent execution is bounded by configurable safety limits.
* Agent failures are handled without unnecessarily breaking existing capabilities.
* Existing conversation, RAG, memory, tool-calling, and provider abstractions remain compatible.
* Agent execution is observable through request-level and execution-level logging.


### Testing

* Added agent core tests.
* Added agent state tests.
* Added agent step/result tests.
* Added execution-loop tests.
* Added multi-step execution tests.
* Added maximum-step tests.
* Added loop-protection tests.
* Added tool selection tests.
* Added multi-tool tests.
* Added tool failure tests.
* Added invalid-tool tests.
* Added invalid-argument tests.
* Added RAG integration tests.
* Added memory integration tests.
* Added agent API tests.
* Added regression tests.
* Full regression suite passing.

### Out of Scope

The following were intentionally excluded from v1.0:

* Multi-agent systems
* Autonomous background agents
* Agent marketplace
* Complex planning algorithms
* Reinforcement learning
* Graph-based agent memory
* Browser automation
* Arbitrary code execution
* Self-modifying agents
* Distributed agent execution
* Frontend / agent UI

### Status

**v1.0.0 — Agentic Orchestration: Complete**

```text
Batch 1 — Agent Core                 ✅
Batch 2 — Memory + RAG               ✅
Batch 3 — Lightweight Planning       ✅
Batch 4 — Safety & Failure Recovery  ✅
Batch 5 — Agent API Integration      ✅
Batch 6 — Agent Evaluation           ✅
```
