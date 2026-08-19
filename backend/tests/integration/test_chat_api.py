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
    mock_generate.assert_called_once()
    args, kwargs = mock_generate.call_args

    messages = args[0]

    assert messages[-1].content == "Hello"
    assert messages[-1].role == "user"

    