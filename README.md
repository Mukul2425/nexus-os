# Nexus OS Roadmap

## Vision

Nexus OS is evolving from a simple LLM backend into a modular AI application platform.

```text
Chat
  ↓
Conversation
  ↓
Observability
  ↓
Production Hardening
  ↓
Provider Abstraction
  ↓
RAG
  ↓
RAG Evaluation
  ↓
Tool Calling
  ↓
Memory
  ↓
Agentic Orchestration
```

---

# Completed Milestones

## v0.1 — Backend Foundation

**Status: ✅ Complete**

* FastAPI backend
* Gemini integration
* Chat API
* Multi-turn interaction
* Streaming responses
* Initial project architecture

---

## v0.2 — Session Management

**Status: ✅ Complete**

* SQLite
* SQLAlchemy
* Conversation model
* Message model
* Conversation repositories
* Message repositories
* Conversation service
* Persistent conversation history

---

## v0.3 — Logging & Observability

**Status: ✅ Complete**

* Centralized logging
* Request IDs
* Request middleware
* Latency logging
* LLM operation logging
* Streaming observability
* Correlated request logging

---

## v0.4 — Production Hardening

**Status: ✅ Complete**

* Pydantic Settings
* Environment configuration
* `.env` support
* Centralized exceptions
* Standardized API errors
* Provider failure handling
* Test infrastructure

---

## v0.5 — LLM Provider Abstraction

**Status: ✅ Complete**

* `LLMProvider`
* Gemini provider
* Provider factory
* Provider-neutral errors
* Normal generation
* Streaming generation
* Provider tests

---

## v0.6 — RAG Foundation

**Status: ✅ Complete**

* Document ingestion
* Text chunking
* Embeddings
* ChromaDB
* Semantic retrieval
* Context assembly
* Source attribution
* RAG observability

---

## v0.7 — RAG Evaluation

**Status: ✅ Complete**

* Evaluation dataset
* Retrieval evaluation
* Hit@K
* Top-K experiments
* Chunk-size experiments
* Generation evaluation
* Groundedness evaluation
* Failure analysis
* Evaluation observability

---

## v0.8 — Tool Calling

**Status: ✅ Complete**

* Tool definitions
* Tool calls
* Tool results
* Tool registry
* Tool executor
* Calculator tool
* Time tool
* Tool error handling
* Gemini function calling
* Tool execution loop
* Maximum tool-call protection
* RAG + tools compatibility

Tool-aware streaming was intentionally deferred because the existing streaming abstraction currently produces plain text events.

---

## v0.9 — Memory Foundation

**Status: ✅ Complete**

### Memory

* SQLAlchemy memory model
* UUID memory IDs
* Semantic and episodic memory
* Importance scoring
* Memory timestamps
* Indexed database records

### CRUD

* Create
* Read
* List
* Update
* Delete
* Pagination
* Validation
* Error handling

### Extraction

* Memory candidate schema
* LLM extraction
* Confidence scoring
* Importance scoring
* Memory classification
* Malformed-output handling

### Eligibility

* Confidence filtering
* Blank-content rejection
* Invalid-type rejection
* Question filtering
* Temporary-request filtering
* Small-talk filtering
* Inference rejection

### Deduplication

* Content normalization
* Whitespace normalization
* Punctuation normalization
* Duplicate detection
* Duplicate persistence prevention

### Vector Memory

* ChromaDB memory collection
* Existing embedding infrastructure
* Memory embeddings
* Metadata linking
* Vector update
* Vector deletion
* Semantic search
* Distance thresholding

### Conflict Detection

* Related-memory retrieval
* Semantic conflict detection
* LLM conflict classification
* Failure-safe behavior

Automatic conflict resolution is intentionally deferred.

### Retrieval

* Semantic memory retrieval
* Configurable top-K
* Distance filtering
* Stale-vector handling
* SQLite source-of-truth lookup
* Retrieval observability

### Chat Integration

* Memory retrieval in `/chat`
* Memory retrieval in `/chat/stream`
* Post-generation memory extraction
* RAG compatibility
* Tool compatibility
* Failure isolation

### Testing

**108 tests passing**

---

# Current Architecture

```text
                         ┌─────────────┐
                         │    User     │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │   FastAPI   │
                         └──────┬──────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ ConversationService │
                    └───────┬─────┬────────┘
                            │     │
             ┌──────────────┘     └──────────────┐
             ▼                                   ▼
      ┌─────────────┐                     ┌─────────────┐
      │ Conversation│                     │    Memory   │
      │   History   │                     │   System    │
      └──────┬──────┘                     └──────┬──────┘
             │                                   │
             ▼                                   ▼
         SQLite                              SQLite
                                                 │
                                                 ▼
                                            ChromaDB

                    ┌─────────────┐
                    │     RAG     │
                    └──────┬──────┘
                           │
                           ▼
                       ChromaDB

                            │
                            ▼
                    ┌─────────────┐
                    │   Context   │
                    │   Builder   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ LLM Provider│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Tools    │
                    └─────────────┘
```

---

# v1.0 — Agentic Orchestration

**Status: ⏳ Planned**

The next major milestone will focus on orchestrating the capabilities already built.

Potential areas:

* Agent state
* Planning
* Tool selection
* Multi-step execution
* Task decomposition
* Agent execution loop
* Memory usage during execution
* RAG usage during execution
* Tool usage during execution
* Agent failure recovery
* Execution limits
* Agent evaluation

The goal is not to create a complex autonomous system immediately.

The goal is to build a **controlled, observable, testable agent execution loop**.

---

# Deferred / Future Work

The following are intentionally not part of the current roadmap milestones unless justified by future requirements:

* Automatic memory conflict resolution
* Graph-based memory
* Multi-agent memory
* Cognitive memory simulation
* Reinforcement-learning memory
* Multiple vector databases
* Enterprise privacy platform
* Complex autonomous behavior
* Frontend before the core AI architecture is mature

Future features should be driven by actual system requirements and evaluation results rather than complexity for its own sake.
