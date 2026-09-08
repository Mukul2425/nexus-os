# Nexus OS

Nexus OS is an AI backend designed to progressively evolve from a conversational AI system into a tool-using, retrieval-augmented, agentic AI platform.

## Current Version

**v0.8.0 — Tool Calling & MCP Foundation**

## Current Capabilities

Nexus OS currently supports:

* Persistent conversations
* SQLite and SQLAlchemy-based message storage
* Centralized prompt management
* Streaming LLM responses
* Centralized logging and request observability
* Request IDs and request correlation
* Production-oriented error handling
* Automated testing
* Provider abstraction
* Gemini LLM provider
* Retrieval-Augmented Generation (RAG)
* Document ingestion
* Vector search using ChromaDB
* RAG evaluation and regression testing
* Tool calling
* Multi-step tool execution
* Tool failure recovery
* Built-in calculator tool
* Built-in time tool

---

# Current Architecture

```text
                         User
                           │
                           ▼
                    FastAPI API Layer
                           │
                           ▼
                  Conversation Service
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      Conversation History         RAG Retrieval
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                     Prompt Context
                           │
                           ▼
                    LLM Provider
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              Final Answer    Tool Call Requested
                    │             │
                    │             ▼
                    │       Tool Executor
                    │             │
                    │             ▼
                    │        Tool Registry
                    │             │
                    │      ┌──────┴──────┐
                    │      │             │
                    ▼      ▼             ▼
                 Response Calculator    Time
                    ▲
                    │
                    └──── Tool Result ────
                           │
                           ▼
                      LLM Provider
                           │
                           ▼
                      Final Answer
                           │
                           ▼
                    Save to Database
                           │
                           ▼
                        Response
```

---

# Tool Calling Architecture

Nexus uses provider-neutral abstractions for tool calling.

```text
ConversationService
        │
        ▼
   LLM Provider
        │
        ▼
    LLMResponse
        │
        ├───────────────┐
        │               │
        ▼               ▼
 Final Response      Tool Calls
                         │
                         ▼
                    ToolExecutor
                         │
                         ▼
                    ToolRegistry
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        CalculatorTool          TimeTool
              │                     │
              └──────────┬──────────┘
                         ▼
                     ToolResult
                         │
                         ▼
                    LLM Provider
                         │
                         ▼
                    Final Answer
```

---

# Tool Execution Flow

```text
User Message
     │
     ▼
ConversationService
     │
     ▼
RAG Retrieval
     │
     ▼
LLM + Tool Definitions
     │
     ▼
Does the LLM request a tool?
     │
 ┌───┴────┐
 │        │
No       Yes
 │        │
 ▼        ▼
Final   ToolExecutor
Answer      │
 │          ▼
 │      Execute Tool
 │          │
 │          ▼
 │      ToolResult
 │          │
 │          ▼
 │      Send Result to LLM
 │          │
 │          ▼
 │      Tool Requested Again?
 │          │
 │      ┌───┴────┐
 │      │        │
 │     No       Yes
 │      │        │
 │      ▼        └──── Repeat
 │   Final
 │   Answer
 │
 ▼
Save Assistant Message
 │
 ▼
API Response
```

---

# Built-in Tools

## Calculator Tool

Supported operations:

* add
* subtract
* multiply
* divide

The tool validates:

* Invalid operations
* Invalid numeric arguments
* Division by zero

---

## Time Tool

Returns the current time for valid IANA timezones.

Examples:

```text
Asia/Kolkata
America/New_York
Europe/London
```

The tool validates:

* Missing timezone
* Invalid timezone
* Invalid argument types

---

# Tool Safety and Reliability

The tool-calling architecture includes:

* Unknown tool detection
* Invalid argument validation
* Tool execution error handling
* Tool failure recovery
* Maximum tool-call limit

The maximum number of tool calls prevents infinite execution loops.

```text
MAX_TOOL_CALLS = 5
```

---

# Streaming

Text streaming remains supported.

Current streaming architecture:

```text
/chat/stream
      │
      ▼
Conversation History
      │
      ▼
RAG Retrieval
      │
      ▼
LLM Text Streaming
      │
      ▼
Streaming Response
```

Tool-aware streaming is intentionally deferred.

The current streaming interface:

```text
AsyncGenerator[str, None]
```

only supports text chunks.

Future tool-aware streaming will require structured events such as:

```text
text_delta
tool_call_started
tool_call_arguments_delta
tool_call_completed
tool_result
generation_resumed
error
```

This will require a dedicated structured streaming architecture.

---

# Current API

```text
POST /conversation

Creates a new conversation.


POST /chat

Loads conversation history
→ Retrieves relevant RAG context
→ Calls LLM
→ Executes tools if requested
→ Returns final response
→ Saves assistant response


POST /chat/stream

Loads conversation history
→ Retrieves relevant RAG context
→ Streams text response

Current streaming does not execute tools.
```

---

# Current Testing Status

```text
64 passed
3 warnings
```

The warnings are dependency/deprecation warnings and do not indicate failures in Nexus OS.

Tool-related coverage includes:

* Tool registry
* Tool factory
* Calculator tool
* Time tool
* Tool executor
* Tool-calling loop
* Multi-step execution
* Tool failure handling
* Existing regression tests

---

# Current Development Direction

```text
v0.6.0
RAG Foundation
      │
      ▼
v0.7.0
RAG Evaluation
      │
      ▼
v0.8.0
Tool Calling
      │
      ▼
v0.9.0
Memory
      │
      ▼
v1.0.0
Agentic Orchestration
```

Nexus OS is now capable of:

```text
Remembering conversations
        +
Retrieving knowledge
        +
Using external tools
```

The next major step is giving the system controlled long-term memory.
