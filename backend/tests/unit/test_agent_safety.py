from unittest.mock import Mock

import pytest

from app.schemas.agent import AgentStatus
from app.schemas.llm import LLMResponse, ToolCall
from app.services.agent.errors import (
    AgentMaxToolCallsError,
    AgentTimeoutError,
    MalformedAgentResponseError,
)
from app.services.agent.service import AgentService
from tests.unit.test_agent_service import build_service

def test_agent_timeout_is_enforced():
    provider = Mock()

    service = build_service(
        provider,
        timeout_seconds=0.001,
    )

    result = service.run(
        conversation_id="c1",
        task="What is FastAPI?",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent execution timed out."


import time


def test_agent_timeout_during_provider_call():
    provider = Mock()

    def slow_generate(*args, **kwargs):
        time.sleep(0.05)
        return LLMResponse(text="done")

    provider.generate_with_tools.side_effect = slow_generate

    service = build_service(
        provider,
        timeout_seconds=0.01,
    )

    result = service.run(
        conversation_id="c1",
        task="What is FastAPI?",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent execution timed out."

def test_malformed_llm_response_fails_safely():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse()

    service = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task="Do something.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent produced an invalid response."

def test_multiple_tool_calls_are_rejected():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"expression": "1 + 1"},
            ),
            ToolCall(
                name="calculator",
                arguments={"expression": "2 + 2"},
            ),
        ]
    )

    service = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task="Calculate both.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent produced an invalid response."

def test_tool_action_without_name_is_rejected():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="",
                arguments={},
            )
        ]
    )

    service = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task="Use a tool.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent produced an invalid response."

def test_unknown_tool_is_controlled():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="not_registered",
                arguments={},
            )
        ]
    )

    service = build_service(provider)

    result = service.run(
        conversation_id="c1",
        task="Use the unknown tool.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Unknown tool requested."

def test_tool_failure_isolated():
    provider = Mock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name="calculator",
                    arguments={"expression": "1 / 0"},
                )
            ]
        ),
        LLMResponse(
            text="I could not complete the calculation."
        ),
    ]

    service, executor = build_service(provider)

    executor.execute.side_effect = ValueError(
        "division by zero"
    )

    result = service.run(
        conversation_id="c1",
        task="Calculate 1 / 0.",
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.error is None

def test_max_tool_calls_is_enforced_before_loop_detection():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    service, _ = build_service(
        provider,
        max_tool_calls=1,
        max_repeated_actions=10,
    )

    result = service.run(
        conversation_id="c1",
        task="Keep calculating.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Maximum tool calls exceeded."

def test_repeated_action_is_detected():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    service, _ = build_service(
        provider,
        max_tool_calls=10,
        max_repeated_actions=2,
    )

    result = service.run(
        conversation_id="c1",
        task="Keep repeating this calculation.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Repeated agent action detected."

def test_memory_failure_does_not_crash_agent(
    db,
):
    provider = Mock()
    memory = Mock()

    memory.retrieve.side_effect = RuntimeError(
        "memory unavailable"
    )

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name="memory",
                    arguments={"query": "preferred language"},
                )
            ]
        ),
        LLMResponse(
            text="I don't have enough memory information."
        ),
    ]

    service = AgentService(
        db=db,
        llm_provider=provider,
        memory_retriever=memory,
    )

    result = service.run(
        conversation_id="c1",
        task="What language do I prefer?",
    )

    assert result.status == AgentStatus.COMPLETED

def test_rag_failure_does_not_crash_agent(
    monkeypatch,
    db,
):
    provider = Mock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name="rag",
                    arguments={"query": "provider architecture"},
                )
            ]
        ),
        LLMResponse(
            text="I could not retrieve the documentation."
        ),
    ]

    def failing_rag(*args, **kwargs):
        raise RuntimeError("RAG unavailable")
    

    monkeypatch.setattr(
        "app.services.agent.service.prepare_rag_question",
        failing_rag,
    )

    service = AgentService(
        db=db,
        llm_provider=provider,
    )

    result = service.run(
        conversation_id="c1",
        task="Explain provider architecture.",
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.error is None