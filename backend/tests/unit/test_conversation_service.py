
from unittest.mock import patch

def test_chat_preserves_conversation_history(
    client,
):

    conversation_response = client.post(
        "/conversation"
    )

    conversation_id = (
        conversation_response
        .json()["conversation_id"]
    )

    with patch(
        "app.services.conversation_service.generate_response"
    ) as mock_generate:

        mock_generate.side_effect = [
            "Hello Mukul!",
            "Your name is Mukul.",
        ]

        first = client.post(
            "/chat",
            json={
                "conversation_id": conversation_id,
                "message": "My name is Mukul.",
            },
        )

        second = client.post(
            "/chat",
            json={
                "conversation_id": conversation_id,
                "message": "What is my name?",
            },
        )

    assert first.status_code == 200
    assert second.status_code == 200

    assert (
        second.json()["response"]
        == "Your name is Mukul."
    )

    assert mock_generate.call_count == 2

def test_chat_invalid_conversation(client):

    response = client.post(
        "/chat",
        json={
            "conversation_id": (
                "does-not-exist"
            ),
            "message": "Hello",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["code"] == (
        "CONVERSATION_NOT_FOUND"
    )

    assert data["error"]["message"] == (
        "Conversation not found"
    )

    assert (
        "request_id"
        in data["error"]
    )