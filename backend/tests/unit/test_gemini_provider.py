from unittest.mock import MagicMock, patch

from app.services.llm.gemini import GeminiProvider
from app.schemas.chat import ChatMessage


def test_gemini_generate():

    provider = GeminiProvider()

    fake_response = MagicMock()
    fake_response.text = "Hello Mukul!"

    with patch.object(
        provider.client.models,
        "generate_content",
        return_value=fake_response,
    ) as mock_generate:

        messages = [
            ChatMessage(
                role="user",
                content="Hello",
            )
        ]

        response = provider.generate(messages)

    assert response == "Hello Mukul!"

    mock_generate.assert_called_once()


def test_gemini_build_contents():

    provider = GeminiProvider()

    messages = [
        ChatMessage(
            role="user",
            content="Hello",
        ),
        ChatMessage(
            role="assistant",
            content="Hi!",
        ),
    ]

    system_instruction, contents = (
        provider._build_contents(messages)
    )

    assert system_instruction is None

    assert contents == [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Hello"
                }
            ],
        },
        {
            "role": "model",
            "parts": [
                {
                    "text": "Hi!"
                }
            ],
        },
    ]