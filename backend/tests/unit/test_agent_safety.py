
from unittest.mock import Mock

from app.schemas.agent import AgentStatus
from app.schemas.llm import LLMResponse, ToolCall
from app.services.agent.capabilities import (
    MEMORY_TOOL_NAME,
    RAG_TOOL_NAME,
)
from app.services.agent.service import AgentService


def test_agent_timeout_is_enforced():
    provider = Mock()

    def slow_generate(*args, **kwargs):
        import time

        time.sleep(0.05)
        return LLMResponse(text="done")

    provider.generate_with_tools.side_effect = slow_generate

    service = AgentService(
        llm_provider=provider,
        timeout_seconds=0.01,
    )

    result = service.run(
        conversation_id="c1",
        task="What is FastAPI?",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Agent execution timed out."




def test_agent_timeout_during_provider_call():
    provider = Mock()

    def slow_generate(*args, **kwargs):
        import time

        time.sleep(0.05)
        return LLMResponse(text="done")

    provider.generate_with_tools.side_effect = slow_generate

    service = AgentService(
        llm_provider=provider,
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

    service = AgentService(
        llm_provider=provider,
    )

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

    service = AgentService(
        llm_provider=provider,
    )

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

    service = AgentService(
        llm_provider=provider,
    )

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

    service = AgentService(
        llm_provider=provider,
    )

    result = service.run(
        conversation_id="c1",
        task="Use the unknown tool.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Unknown tool: not_registered"


def test_tool_failure_isolated():
    provider = Mock()
    executor = Mock()

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

    executor.execute.side_effect = ValueError(
        "division by zero"
    )

    service = AgentService(
        llm_provider=provider,
        tool_executor=executor,
    )

    result = service.run(
        conversation_id="c1",
        task="Calculate 1 / 0.",
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.error is None


def test_max_tool_calls_is_enforced_before_loop_detection():
    provider = Mock()
    executor = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    executor.execute.return_value = {
        "success": True,
        "tool_name": "calculator",
        "result": 2,
        "error": None,
    }

    service = AgentService(
        llm_provider=provider,
        tool_executor=executor,
        max_tool_calls=1,
        max_repeated_actions=10,
    )

    result = service.run(
        conversation_id="c1",
        task="Keep calculating.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == (
        "The maximum number of tool calls was reached."
    )


def test_repeated_action_is_detected():
    provider = Mock()
    executor = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    executor.execute.return_value = {
        "success": True,
        "tool_name": "calculator",
        "result": 2,
        "error": None,
    }

    service = AgentService(
        llm_provider=provider,
        tool_executor=executor,
        max_tool_calls=10,
        max_repeated_actions=2,
    )

    result = service.run(
        conversation_id="c1",
        task="Keep repeating this calculation.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Repeated agent action detected."


def test_memory_failure_does_not_crash_agent(db):
    provider = Mock()
    memory = Mock()

    memory.retrieve.side_effect = RuntimeError(
        "memory unavailable"
    )

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=MEMORY_TOOL_NAME,
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
    assert result.error is None


def test_rag_failure_does_not_crash_agent(monkeypatch, db):
    provider = Mock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    name=RAG_TOOL_NAME,
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

