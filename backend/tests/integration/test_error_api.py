from unittest.mock import patch

from app.core.exceptions import ConversationNotFoundError

from unittest.mock import MagicMock, patch

from app.core.exceptions import LLMProviderError


def test_llm_provider_error(client):

    conversation_response = client.post(
        "/conversation"
    )

    conversation_id = (
        conversation_response
        .json()["conversation_id"]
    )

    mock_provider = MagicMock()

    mock_provider.generate.side_effect = (
        LLMProviderError()
    )

    with patch(
        "app.api.chat.create_llm_provider",
        return_value=mock_provider,
    ):

        response = client.post(
            "/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Hello",
            },
        )

    assert response.status_code == 502

    data = response.json()

    assert data["error"]["code"] == (
        "LLM_PROVIDER_ERROR"
    )

    assert data["error"]["message"] == (
        "Unable to generate a response"
    )

    assert "request_id" in data["error"]


    
def test_conversation_not_found_error(client):

    with patch(
        "app.services.conversation_service.ConversationService.chat",
        side_effect=ConversationNotFoundError(),
    ):

        response = client.post(
            "/chat",
            json={
                "conversation_id": "00000000-0000-0000-0000-000000000000",
                "message": "Hello",
            },
        )

    assert response.status_code == 404

    assert response.json()["error"]["code"] == (
        "CONVERSATION_NOT_FOUND"
    )

    assert response.json()["error"]["message"] == (
        "Conversation not found"
    )

    assert "request_id" in response.json()["error"]