from unittest.mock import MagicMock

from app.services.conversation_service import ConversationService


def test_chat_service(db):
    mock_provider = MagicMock()

    mock_provider.generate.return_value = "Hello Mukul!"

    service = ConversationService(
        db,
        mock_provider,
    )

    # Create conversation
    conversation = service.conversation_repository.create()

    response,sources = service.chat(
        conversation.id,
        "Hello",
    )

    assert response == "Hello Mukul!"
    assert sources == []

    mock_provider.generate.assert_called_once()


def test_chat_service_saves_messages(db):
    mock_provider = MagicMock()

    mock_provider.generate.return_value = "Hello!"

    service = ConversationService(
        db,
        mock_provider,
    )

    conversation = service.conversation_repository.create()

    service.chat(
        conversation.id,
        "My name is Mukul",
    )

    messages = service.message_repository.get_messages(
        conversation.id
    )

    assert len(messages) == 2

    assert messages[0].role == "user"
    assert messages[0].content == "My name is Mukul"

    assert messages[1].role == "assistant"
    assert messages[1].content == "Hello!"