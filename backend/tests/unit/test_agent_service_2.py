from unittest.mock import Mock

import pytest

from app.schemas.agent import AgentStatus
from app.schemas.llm import LLMResponse, ToolCall
from app.services.agent.service import AgentService

from unittest.mock import Mock

from app.services.agent.capabilities import (
    MEMORY_TOOL_NAME,
    RAG_TOOL_NAME,
    get_agent_capability_definitions,
)
from app.services.agent.service import AgentService
from app.services.agent.decision import AgentDecisionError, decide_action
from app.schemas.agent import (
    AgentActionType,
)
from app.schemas.llm import (
    LLMResponse,
    ToolCall,
)
from tests.unit.test_agent_service import build_service


def test_agent_retrieves_memory(
    db,
):
    fake_provider = Mock()
    fake_memory_retriever = Mock()
    fake_memory_retriever.retrieve.return_value = [
        {
            "memory_id": "m1",
            "content": "User prefers Python.",
            "memory_type": "preference",
            "importance": 5,
            "distance": 0.2,
        }
    ]

    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name=MEMORY_TOOL_NAME,
                    arguments={
                        "query": "backend language preference"
                    },
                )
            ]
        ),
        LLMResponse(
            text="You should use Python for the backend."
        ),
    ]

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
        memory_retriever=fake_memory_retriever,
    )

    result = service.run(
        conversation_id="c1",
        task="Which backend language should I use?",
    )

    assert result.status.value == "completed"
    assert result.response == (
        "You should use Python for the backend."
    )

    assert len(result.retrieved_memories) == 1

    fake_memory_retriever.retrieve.assert_called_once_with(
        "backend language preference"
    )



def test_memory_observation_is_fed_back_to_agent(
    db,
):
    fake_provider = Mock()
    fake_memory_retriever = Mock()
    fake_memory_retriever.retrieve.return_value = [
        {
            "memory_id": "m1",
            "content": "User prefers Python.",
            "memory_type": "preference",
            "importance": 5,
            "distance": 0.1,
        }
    ]

    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=MEMORY_TOOL_NAME,
                    arguments={
                        "query": "programming preference"
                    },
                )
            ]
        ),
        LLMResponse(
            text="Python is the best fit for you."
        ),
    ]

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
        memory_retriever=fake_memory_retriever,
    )

    result = service.run(
        conversation_id="c1",
        task="What language should I use?",
    )

    assert result.status.value == "completed"

    second_call = (
        fake_provider
        .generate_with_tools
        .call_args_list[1]
    )

    messages = second_call.args[0]

    assert any(
        "User prefers Python."
        in message.content
        for message in messages
    )

def test_memory_failure_does_not_fail_agent(
    db,
):
    fake_provider = Mock()
    fake_memory_retriever = Mock()
    fake_memory_retriever.retrieve.side_effect = (
        RuntimeError("memory unavailable")
    )

    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=MEMORY_TOOL_NAME,
                    arguments={
                        "query": "user preference"
                    },
                )
            ]
        ),
        LLMResponse(
            text="I can answer without memory."
        ),
    ]

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
        memory_retriever=fake_memory_retriever,
    )

    result = service.run(
        conversation_id="c1",
        task="What should I use?",
    )

    assert result.status.value == "completed"
    assert result.response == (
        "I can answer without memory."
    )

    assert result.retrieved_memories == []

    assert (
        result.steps[0].success is False
    )


def test_agent_retrieves_rag(
    monkeypatch,
    db,
):
    fake_provider = Mock()
    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=RAG_TOOL_NAME,
                    arguments={
                        "query": (
                            "Nexus provider architecture"
                        )
                    },
                )
            ]
        ),
        LLMResponse(
            text=(
                "Nexus uses a provider abstraction "
                "with concrete LLM providers."
            )
        ),
    ]

    monkeypatch.setattr(
        "app.services.agent.service.prepare_rag_question",
        lambda question, top_k: {
    "prompt": "Relevant context...",
    "sources": [
        {
            "document": "architecture.md",
            "document_id": "doc-1",
            "chunk_id": "chunk-1",
        }
    ],
}
    )

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
    )

    result = service.run(
        conversation_id="c1",
        task=(
            "According to Nexus documentation, "
            "what is provider architecture?"
        ),
    )

    assert result.status.value == "completed"

    assert result.retrieved_documents == [
        {
            "document": "architecture.md",
            "document_id": "doc-1",
            "chunk_id": "chunk-1",
        }
    ]

def test_rag_observation_is_fed_back_to_agent(
    monkeypatch,
    db,
):
    fake_provider = Mock()
    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=RAG_TOOL_NAME,
                    arguments={
                        "query": "provider architecture"
                    },
                )
            ]
        ),
        LLMResponse(
            text="The provider abstraction isolates LLM vendors."
        ),
    ]

    monkeypatch.setattr(
        "app.services.agent.service.prepare_rag_question",
        lambda question, top_k: {
    "prompt": "Relevant context...",
    "sources": [
        {
            "document": "architecture.md",
            "document_id": "doc-1",
            "chunk_id": "chunk-1",
        }
    ],
}
    )

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
    )

    result = service.run(
        conversation_id="c1",
        task="Explain provider architecture.",
    )

    assert result.status.value == "completed"

    second_call = (
        fake_provider
        .generate_with_tools
        .call_args_list[1]
    )

    messages = second_call.args[0]

    assert any(
        "Relevant context..."
        in message.content
        for message in messages
    )


def test_rag_failure_does_not_fail_agent(
    monkeypatch,
    db,
):
    fake_provider = Mock()
    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=RAG_TOOL_NAME,
                    arguments={
                        "query": "Nexus architecture"
                    },
                )
            ]
        ),
        LLMResponse(
            text="I can answer without retrieved documents."
        ),
    ]

    def failing_rag(
        question,
        top_k,
    ):
        raise RuntimeError(
            "vector store unavailable"
        )

    monkeypatch.setattr(
        "app.services.agent.service.prepare_rag_question",
        failing_rag,
    )

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
    )

    result = service.run(
        conversation_id="c1",
        task="Explain Nexus architecture.",
    )

    assert result.status.value == "completed"

    assert result.response == (
        "I can answer without retrieved documents."
    )

    assert result.retrieved_documents == []

    assert result.steps[0].success is False



def test_agent_can_combine_memory_and_rag(
    monkeypatch,
    db,
):
    fake_provider = Mock()
    fake_memory_retriever = Mock()
    fake_memory_retriever.retrieve.return_value = [
        {
            "memory_id": "m1",
            "content": "User prefers Python and FastAPI.",
            "memory_type": "preference",
            "importance": 5,
            "distance": 0.1,
        }
    ]

    monkeypatch.setattr(
        "app.services.agent.service.prepare_rag_question",
        lambda question, top_k: {
    "prompt": "Relevant context...",
    "sources": [
        {
            "document": "architecture.md",
            "document_id": "doc-1",
            "chunk_id": "chunk-1",
        }
    ],
}
    )

    fake_provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=MEMORY_TOOL_NAME,
                    arguments={
                        "query": "preferred backend stack"
                    },
                )
            ]
        ),
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=RAG_TOOL_NAME,
                    arguments={
                        "query": (
                            "Nexus recommended backend stack"
                        )
                    },
                )
            ]
        ),
        LLMResponse(
            text=(
                "Given your preference for Python and "
                "FastAPI and the Nexus documentation, "
                "FastAPI is the appropriate backend choice."
            )
        ),
    ]

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
        memory_retriever=fake_memory_retriever,
    )

    result = service.run(
        conversation_id="c1",
        task=(
            "Using my preferences and Nexus documentation, "
            "which backend stack should I use?"
        ),
    )

    assert result.status.value == "completed"

    assert result.step_count == 3

    assert len(result.retrieved_memories) == 1

    assert len(result.retrieved_documents) == 1

    assert (
        "FastAPI"
        in result.response
    )


def test_agent_capability_definitions():
    from app.services.agent.capabilities import (
        get_agent_capability_definitions,
    )

    definitions = (
        get_agent_capability_definitions()
    )

    names = {
        definition.name
        for definition in definitions
    }

    assert names == {
        "memory_retrieval",
        "rag_retrieval",
    }


def test_memory_capability_requires_query():
    response = LLMResponse(
        tool_calls=[
            ToolCall(
                name=MEMORY_TOOL_NAME,
                arguments={},
            )
        ]
    )

    try:
        decide_action(response)
        assert False
    except AgentDecisionError:
        assert True


def test_rag_capability_requires_query():
    response = LLMResponse(
        tool_calls=[
            ToolCall(
                name=RAG_TOOL_NAME,
                arguments={},
            )
        ]
    )

    try:
        decide_action(response)
        assert False
    except AgentDecisionError:
        assert True



def test_normal_tool_definitions_are_still_available(
    db,
):
    fake_provider = Mock()
    fake_provider.generate_with_tools.return_value = (
        LLMResponse(
            text="done"
        )
    )

    service = AgentService(
        db=db,
        llm_provider=fake_provider,
    )

    definitions = (
        service.tool_registry.get_definitions()
    )

    names = {
        definition.name
        for definition in definitions
    }

    assert "calculator" in names
    assert "time" in names

    capability_definitions = (
        get_agent_capability_definitions()
    )

    capability_names = {
        definition.name
        for definition in capability_definitions
    }

    assert "memory_retrieval" in capability_names
    assert "rag_retrieval" in capability_names


def test_agent_creates_plan():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="FastAPI is a Python web framework."
    )

    service, _ = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task="What is FastAPI?",
    )

    assert result.status.value == "completed"
    assert result.plan == ["What is FastAPI?"]
    assert result.plan_progress == ["completed"]


def test_agent_tracks_multi_step_plan():
    provider = Mock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="time",
                    arguments={"timezone": "Europe/London"},
                )
            ]
        ),
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-2",
                    name="calculator",
                    arguments={"expression": "24 - 10"},
                )
            ]
        ),
        LLMResponse(
            text="14 hours remain."
        ),
    ]

    service, _ = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task=(
            "Get the time in London and then calculate "
            "how many hours remain until midnight."
        ),
    )

    assert result.status.value == "completed"
    assert len(result.plan) == 2
    assert all(
        status == "completed"
        for status in result.plan_progress
    )