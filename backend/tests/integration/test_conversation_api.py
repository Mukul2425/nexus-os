def test_create_conversation(client):

    response = client.post(
        "/conversation"
    )

    assert response.status_code == 200

    data = response.json()

    assert "conversation_id" in data
    assert data["conversation_id"]