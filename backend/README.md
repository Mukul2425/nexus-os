## Current Status

- [x] Repository initialized
- [x] Project documentation
- [x] Backend foundation
- [x] LLM integration
- [ ] Frontend
- [x] Streaming
- [x] Logging
- [x] Session Management
- [x] LLM Provider Abstraction
- [x] Provider Factory
- [x] Gemini Provider
- [x] Streaming through LLM abstraction
- [x] Persistent conversations
- [x] Prompt management
- [x] Streaming responses
- [x] Logging & observability
- [x] Production configuration & error handling
- [x] LLM provider abstraction
- [x] RAG foundation
- [x] Document ingestion
- [x] Semantic retrieval
- [x] Source attribution
- [x] RAG evaluation
- [x] Retrieval quality evaluation
- [x] Generation quality evaluation
- [x] RAG regression testing
Backend Foundation

✔ FastAPI

✔ Swagger

✔ Chat Endpoint

✔ Gemini Integration

✔ LLM Abstraction

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

## Architectural diagram after v0.4.0

                         Nexus Backend
                              │
                         Configuration
                              │
                              ▼
Request ──► Logging Middleware
                  │
                  ▼
              API Routes
                  │
                  ▼
        Conversation Service
          │       │       │
          │       │       └────► Prompt Builder
          │       │
          │       └────────────► LLM Service
          │                           │
          │                           ▼
          │                         Gemini
          │
          ▼
      Repositories
          │
          ▼
       SQLite


      ┌───────────────────────────────┐
      │       Error Handling          │
      │                               │
      │ Custom Exceptions             │
      │ Global Exception Handler      │
      │ Safe API Errors               │
      └───────────────────────────────┘

      ┌───────────────────────────────┐
      │          Testing              │
      │                               │
      │ Unit Tests                    │
      │ Integration Tests             │
      │ Mocked LLM                    │
      │ Test Database                 │
      └───────────────────────────────┘




## Architectural diagram after v0.5.0

                         ┌─────────────────────┐
                         │       Client        │
                         └──────────┬──────────┘
                                    │
                         HTTP / REST / Streaming
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         │                     │
                         │ /conversation       │
                         │ /chat               │
                         │ /chat/stream        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ ConversationService │
                         │                     │
                         │ • history           │
                         │ • persistence       │
                         │ • prompt building   │
                         │ • orchestration     │
                         └───────┬───────┬─────┘
                                 │       │
                    ┌────────────┘       └─────────────┐
                    ▼                                  ▼
          ┌──────────────────┐              ┌─────────────────┐
          │    Repositories  │              │  Prompt Builder │
          │                  │              └─────────────────┘
          │ ConversationRepo │
          │ MessageRepo      │
          └──────────────────┘                     
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │    LLMProvider      │
                         │     Interface       │
                         │                     │
                         │ generate()          │
                         │ stream()            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Provider Factory  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   GeminiProvider    │
                         │                     │
                         │ Gemini-specific     │
                         │ implementation      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              Gemini API

                ┌─────────────────────────────────────────┐
                │           Cross-Cutting Concerns        │
                │                                         │
                │ Logging • Error Handling • Configuration│
                │ Testing • Request Correlation           │
                └─────────────────────────────────────────┘


## Architectural diagram after v0.6.0

                
                        Client
                           │
                           ▼
                      FastAPI API
                           │
                           ▼
                  ConversationService
                    │           │
                    │           ├──────────────┐
                    ▼           ▼              ▼
              Repositories   RAG Service   Prompt Builder
                                 │
                         ┌───────┴────────┐
                         ▼                ▼
                   Embeddings       ChromaDB
                         │                │
                         └───────┬────────┘
                                 │
                         Retrieved Context
                                 │
                                 ▼
                          Prompt Builder
                                 │
                                 ▼
                           LLMProvider
                                 │
                                 ▼
                         GeminiProvider
                                 │
                                 ▼
                             Gemini



## Architectural diagram for v0.7.0


                         ┌──────────────────────┐
                         │ Evaluation Dataset   │
                         │                      │
                         │ Documents            │
                         │ Questions            │
                         │ Expected Sources     │
                         │ Expected Information │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Evaluation Runner    │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
          ┌──────────────────┐              ┌──────────────────┐
          │ Retrieval        │              │ Generation       │
          │ Evaluation       │              │ Evaluation       │
          └────────┬─────────┘              └────────┬─────────┘
                   │                                 │
                   ▼                                 ▼
             Hit@K Metrics                    Answer Relevance
             Retrieval Failures               Groundedness
             Distance Analysis                Hallucination
                   │                                 │
                   └───────────────┬─────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │ Evaluation Results   │
                         │                      │
                         │ Metrics              │
                         │ Failed Cases         │
                         │ Baselines            │
                         └──────────────────────┘