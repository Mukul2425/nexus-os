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




def test_chat_returns_rag_sources(client):

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
        "Gemini is used by Nexus."
    )

    fake_retrieved_results = [
        {
            "content": "Nexus uses Gemini.",
            "document": "nexus.txt",
            "document_id": "doc-123",
            "chunk_id": 0,
            "distance": 0.12,
        },
        {
            "content": "Some unrelated information.",
            "document": "other.txt",
            "document_id": "doc-456",
            "chunk_id": 3,
            "distance": 0.81,
        },
    ]

    with patch(
        "app.services.rag.context.retrieve",
        return_value=fake_retrieved_results,
    ):

        with patch(
            "app.api.chat.create_llm_provider",
            return_value=mock_provider,
        ):

            response = client.post(
                "/chat",
                json={
                    "conversation_id": conversation_id,
                    "message": "Which LLM does Nexus use?",
                },
            )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Gemini is used by Nexus.",
        "sources": [
            {
                "document": "nexus.txt",
                "document_id": "doc-123",
                "chunk_id": 0,
                "distance": 0.12,
            }
        ],
    }