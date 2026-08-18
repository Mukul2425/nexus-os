from app.prompts.chat import (
    prepare_chat_messages,
)

from app.schemas.chat import ChatMessage


def test_system_prompt_is_added():

    messages = [
        ChatMessage(
            role="user",
            content="Hello",
        )
    ]

    result = prepare_chat_messages(
        messages
    )

    assert result[0].role == "system"

    assert len(result) == 2

    assert result[1].content == "Hello"