from unittest.mock import MagicMock, patch

from app.schemas.llm import LLMResponse
from app.services.conversation_service import ConversationService


def test_chat_uses_retrieved_memory(db):
    provider = MagicMock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="You prefer Python."
    )

    service = ConversationService(
        db,
        provider,
    )

    conversation = service.conversation_repository.create()

    with patch.object(
        service.memory_retriever,
        "retrieve",
        return_value=[
            {
                "memory_id": "memory-1",
                "content": "User prefers Python.",
                "memory_type": "semantic",
                "importance": 4,
                "distance": 0.2,
            }
        ],
    ), patch(
        "app.services.conversation_service.prepare_rag_question",
        return_value={
            "prompt": "What language do I prefer?",
            "sources": [],
        },
    ):

        answer, sources = service.chat(
            conversation_id=conversation.id,
            message="What programming language do I prefer?",
        )

    assert answer == "You prefer Python."
    assert sources == []

    call_args = provider.generate_with_tools.call_args
    messages = call_args.kwargs["messages"]

    assert any(
        message.role == "system"
        and "User prefers Python." in message.content
        for message in messages
    )


def test_chat_extracts_memory(db):
    provider = MagicMock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="Sounds good."
    )

    service = ConversationService(
        db,
        provider,
    )

    conversation = service.conversation_repository.create()

    with patch.object(
        service.memory_retriever,
        "retrieve",
        return_value=[],
    ), patch.object(
        service.memory_service,
        "extract_and_create",
    ) as extract_mock, patch(
        "app.services.conversation_service.prepare_rag_question",
        return_value={
            "prompt": "I prefer Python.",
            "sources": [],
        },
    ):

        service.chat(
            conversation_id=conversation.id,
            message="I prefer Python.",
        )

    extract_mock.assert_called_once_with(
        "I prefer Python."
    )


def test_memory_extraction_failure_does_not_break_chat(
    db,
):
    provider = MagicMock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="The answer is 42."
    )

    service = ConversationService(
        db,
        provider,
    )

    conversation = service.conversation_repository.create()

    with patch.object(
        service.memory_retriever,
        "retrieve",
        return_value=[],
    ), patch.object(
        service.memory_service,
        "extract_and_create",
        side_effect=RuntimeError(
            "memory failure"
        ),
    ), patch(
        "app.services.conversation_service.prepare_rag_question",
        return_value={
            "prompt": "What is 42?",
            "sources": [],
        },
    ):

        answer, sources = service.chat(
            conversation_id=conversation.id,
            message="What is 42?",
        )

    assert answer == "The answer is 42."
    assert sources == []


def test_memory_failure_does_not_disable_rag(
    db,
):
    provider = MagicMock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="The document says FastAPI."
    )

    service = ConversationService(
        db,
        provider,
    )

    conversation = service.conversation_repository.create()

    with patch.object(
        service.memory_retriever,
        "retrieve",
        side_effect=RuntimeError(
            "memory unavailable"
        ),
    ), patch(
        "app.services.conversation_service.prepare_rag_question",
        return_value={
            "prompt": (
                "According to the documents, "
                "what framework is used?"
            ),
            "sources": [
                {
                    "content": "The project uses FastAPI.",
                    "document": "project.md",
                }
            ],
        },
    ):

        answer, sources = service.chat(
            conversation_id=conversation.id,
            message="What framework is used?",
        )

    assert answer == "The document says FastAPI."
    assert sources


def test_memory_context_preserves_tool_calling(
    db,
):
    provider = MagicMock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                {
                    "id": "call-1",
                    "name": "calculator",
                    "arguments": {
                        "expression": "10 + 20"
                    },
                }
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

    conversation = service.conversation_repository.create()

    with patch.object(
        service.memory_retriever,
        "retrieve",
        return_value=[
            {
                "memory_id": "memory-1",
                "content": (
                    "User prefers concise explanations."
                ),
                "memory_type": "semantic",
                "importance": 4,
                "distance": 0.2,
            }
        ],
    ), patch(
        "app.services.conversation_service.prepare_rag_question",
        return_value={
            "prompt": "Calculate 10 + 20.",
            "sources": [],
        },
    ):

        answer, sources = service.chat(
            conversation_id=conversation.id,
            message="Calculate 10 + 20.",
        )

    assert answer == "The answer is 30."
    assert sources == []

    assert (
        provider.generate_with_tools.call_count
        == 2
    )

    first_call = (
        provider.generate_with_tools.call_args_list[0]
    )

    messages = first_call.kwargs["messages"]

    assert any(
        message.role == "system"
        and "User prefers concise explanations."
        in message.content
        for message in messages
    )