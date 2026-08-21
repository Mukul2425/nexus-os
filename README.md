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

