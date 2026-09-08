from unittest.mock import MagicMock

from app.schemas.llm import (
    LLMResponse,
    ToolCall,
)

from app.services.conversation_service import (
    ConversationService,
)


def test_tool_calling_loop(db):

    provider = MagicMock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="calculator",
                    arguments={
                        "operation": "add",
                        "a": 10,
                        "b": 20,
                    },
                )
            ]
        ),
        LLMResponse(
            text="The answer is 30."
        ),
    ]

    service = ConversationService(
        db,
        provider,
    )

    conversation = (
        service.conversation_repository.create()
    )

    answer, sources = service.chat(
        conversation.id,
        "What is 10 plus 20?",
    )

    assert answer == "The answer is 30."

    assert sources == []

    assert (
        provider.generate_with_tools.call_count
        == 2
    )


def test_tool_failure_returns_result_to_llm(db):

    provider = MagicMock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="unknown_tool",
                    arguments={},
                )
            ]
        ),
        LLMResponse(
            text=(
                "I could not execute the "
                "requested tool."
            )
        ),
    ]

    service = ConversationService(
        db,
        provider,
    )

    conversation = (
        service.conversation_repository.create()
    )

    answer, _ = service.chat(
        conversation.id,
        "Do something unknown",
    )

    assert (
        answer
        == "I could not execute the requested tool."
    )

    assert (
        provider.generate_with_tools.call_count
        == 2
    )