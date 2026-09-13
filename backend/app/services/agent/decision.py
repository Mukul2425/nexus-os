from app.schemas.agent import AgentAction, AgentActionType
from app.schemas.llm import LLMResponse


class AgentDecisionError(Exception):
    """Raised when an LLM response cannot be converted into an agent action."""


def decide_action(response: LLMResponse) -> AgentAction:
    """
    Convert the provider-neutral LLM response into one agent action.

    The v1.0 agent executes exactly one action per step.
    """

    if response.tool_calls:
        if len(response.tool_calls) != 1:
            raise AgentDecisionError(
                "Agent returned multiple actions for a single execution step."
            )

        tool_call = response.tool_calls[0]

        if not tool_call.name:
            raise AgentDecisionError(
                "Agent returned a tool call without a tool name."
            )

        return AgentAction(
            type=AgentActionType.TOOL,
            tool_name=tool_call.name,
            arguments=tool_call.arguments,
        )

    if response.text:
        return AgentAction(
            type=AgentActionType.ANSWER,
            response=response.text,
        )

    raise AgentDecisionError(
        "Agent returned neither a final response nor a tool call."
    )