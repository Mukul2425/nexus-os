from unittest.mock import MagicMock, patch


def test_chat(client):

    conversation_response = client.post(
        "/conversation"
    )

    assert conversation_response.status_code == 200

    conversation_id = (
        conversation_response
        .json()["conversation_id"]
    )

    mock_provider = MagicMock()

    mock_provider.generate.return_value = (
        "Hello Mukul!"
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

    assert response.status_code == 200

    assert response.json() == {
    "response": "Hello Mukul!",
    "sources": [],
    }

    mock_provider.generate.assert_called_once()