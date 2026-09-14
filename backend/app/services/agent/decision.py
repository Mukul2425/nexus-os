from app.schemas.agent import (
    AgentAction,
    AgentActionType,
)
from app.schemas.llm import LLMResponse

from app.services.agent.capabilities import (
    MEMORY_TOOL_NAME,
    RAG_TOOL_NAME,
)


class AgentDecisionError(Exception):
    """Raised when the LLM response cannot be converted to an agent action."""


def decide_action(response: LLMResponse) -> AgentAction:
    """
    Convert the provider-neutral LLM response into exactly one
    agent action.

    v1.0 intentionally executes one action at a time.
    """

    if response.tool_calls:

        if len(response.tool_calls) != 1:
            raise AgentDecisionError(
                "Agent must select exactly one action at a time."
            )

        tool_call = response.tool_calls[0]

        if not tool_call.name:
            raise AgentDecisionError(
                "Agent selected a tool without a name."
            )

        arguments = tool_call.arguments or {}

        if tool_call.name == MEMORY_TOOL_NAME:
            query = arguments.get("query")

            if not isinstance(query, str) or not query.strip():
                raise AgentDecisionError(
                    "Memory retrieval requires a non-empty query."
                )

            return AgentAction(
                type=AgentActionType.MEMORY,
                query=query.strip(),
                arguments=arguments,
            )

        if tool_call.name == RAG_TOOL_NAME:
            query = arguments.get("query")

            if not isinstance(query, str) or not query.strip():
                raise AgentDecisionError(
                    "RAG retrieval requires a non-empty query."
                )

            return AgentAction(
                type=AgentActionType.RAG,
                query=query.strip(),
                arguments=arguments,
            )

        return AgentAction(
            type=AgentActionType.TOOL,
            tool_name=tool_call.name,
            arguments=arguments,
        )

    if response.text and response.text.strip():
        return AgentAction(
            type=AgentActionType.ANSWER,
            response=response.text,
        )

    raise AgentDecisionError(
        "Agent produced no actionable response."
    )