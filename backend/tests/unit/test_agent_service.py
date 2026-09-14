from unittest.mock import Mock

import pytest

from app.schemas.agent import AgentStatus
from app.schemas.llm import LLMResponse, ToolCall
from app.services.agent.service import AgentService


class FakeRegistry:
    def __init__(self):
        self.tools = {
            "calculator": {
                "name": "calculator",
            },
            "time": {
                "name": "time",
            },
        }

    def get_definitions(self):
        return []

    def has(self, name):
        return name in self.tools


class FakeExecutor:
    def __init__(self):
        self.calls = []

    def execute(self, tool_name, arguments):
        self.calls.append(
            {
                "tool_name": tool_name,
                "arguments": arguments,
            }
        )

        if tool_name == "calculator":
            return {
                "success": True,
                "tool_name": tool_name,
                "result": 42,
            }

        if tool_name == "time":
            return {
                "success": True,
                "tool_name": tool_name,
                "result": "10:30 London",
            }

        raise RuntimeError("unknown tool")


def build_service(provider):
    registry = FakeRegistry()
    executor = FakeExecutor()

    service = AgentService(
        llm_provider=provider,
        tool_registry=registry,
        tool_executor=executor,
    )

    return service, executor


def test_direct_answer_completes_agent():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        text="FastAPI is a Python web framework."
    )

    service, executor = build_service(provider)

    result = service.run(
        conversation_id="conversation-1",
        task="What is FastAPI?",
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.response == "FastAPI is a Python web framework."
    assert result.step_count == 1
    assert result.tool_call_count == 0
    assert executor.calls == []


def test_single_tool_action_then_answer():
    provider = Mock()

    provider.generate_with_tools.side_effect = [
        LLMResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="calculator",
                    arguments={"expression": "25 * 18"},
                )
            ]
        ),
        LLMResponse(
            text="The result is 450."
        ),
    ]

    service, executor = build_service(provider)

    result = service.run(
        conversation_id="conversation-1",
        task="Calculate 25 * 18.",
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.response == "The result is 450."
    assert result.step_count == 2
    assert result.tool_call_count == 1

    assert executor.calls == [
        {
            "tool_name": "calculator",
            "arguments": {"expression": "25 * 18"},
        }
    ]


def test_two_sequential_tool_actions():
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

    service, executor = build_service(provider)

    result = service.run(
        conversation_id="conversation-1",
        task=(
            "Get the time in London and calculate "
            "how many hours remain until midnight."
        ),
    )

    assert result.status == AgentStatus.COMPLETED
    assert result.response == "14 hours remain."

    assert result.step_count == 3
    assert result.tool_call_count == 2

    assert executor.calls == [
        {
            "tool_name": "time",
            "arguments": {"timezone": "Europe/London"},
        },
        {
            "tool_name": "calculator",
            "arguments": {"expression": "24 - 10"},
        },
    ]


def test_unknown_tool_fails_safely():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                id="call-1",
                name="does_not_exist",
                arguments={},
            )
        ]
    )

    service, executor = build_service(provider)

    result = service.run(
        conversation_id="conversation-1",
        task="Use the unknown tool.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Unknown tool: does_not_exist"
    assert executor.calls == []


def test_empty_task_is_rejected():
    provider = Mock()

    service, _ = build_service(provider)

    with pytest.raises(ValueError, match="Agent task cannot be empty"):
        service.run(
            conversation_id="conversation-1",
            task="   ",
        )


def test_max_agent_steps_is_enforced():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                id="call",
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    service, executor = build_service(provider)

    service.max_agent_steps = 2

    result = service.run(
        conversation_id="conversation-1",
        task="Keep calculating.",
    )

    assert result.status == AgentStatus.MAX_STEPS_REACHED
    assert result.step_count == 2
    assert result.tool_call_count == 2


def test_max_tool_calls_is_enforced():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                id="call",
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    service, executor = build_service(provider)

    service.max_tool_calls = 2

    result = service.run(
        conversation_id="conversation-1",
        task="Keep calculating.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == (
        "The maximum number of tool calls was reached."
    )

    assert len(executor.calls) == 2


def test_repeated_action_protection():
    provider = Mock()

    provider.generate_with_tools.return_value = LLMResponse(
        tool_calls=[
            ToolCall(
                id="call",
                name="calculator",
                arguments={"expression": "1 + 1"},
            )
        ]
    )

    service, executor = build_service(provider)

    result = service.run(
        conversation_id="conversation-1",
        task="Keep calculating the same thing.",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Repeated agent action detected."



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
