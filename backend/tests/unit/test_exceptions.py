from app.core.exceptions import (
    LLMProviderError,
    ConversationNotFoundError,
)


def test_llm_provider_error():

    exc = LLMProviderError()

    assert exc.code == "LLM_PROVIDER_ERROR"
    assert exc.message == "Unable to generate a response"
    assert exc.status_code == 502


def test_conversation_not_found_error():

    exc = ConversationNotFoundError()

    assert exc.code == "CONVERSATION_NOT_FOUND"
    assert exc.message == "Conversation not found"
    assert exc.status_code == 404