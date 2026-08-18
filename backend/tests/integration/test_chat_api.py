from unittest.mock import patch


def test_chat(client):

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

        mock_generate.return_value = (
            "Hello Mukul!"
        )

        response = client.post(
            "/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Hello",
            },
        )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Hello Mukul!"
    }

    mock_generate.assert_called_once()