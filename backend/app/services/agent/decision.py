
from app.schemas.agent import (
    AgentAction,
    AgentActionType,
)
from app.schemas.llm import LLMResponse

from app.services.agent.capabilities import (
    MEMORY_TOOL_NAME,
    RAG_TOOL_NAME,
)
from app.services.agent.errors import MalformedAgentResponseError


def decide_action(response: LLMResponse) -> AgentAction:
    """
    Convert the provider-neutral LLM response into exactly one
    agent action.

    v1.0 intentionally executes one action at a time.
    """

    if response is None:
        raise MalformedAgentResponseError(
            "LLM returned no response."
        )

    tool_calls = response.tool_calls or []

    if len(tool_calls) > 1:
        raise MalformedAgentResponseError(
            "Agent returned multiple actions; exactly one action is allowed."
        )

    if tool_calls:
        tool_call = tool_calls[0]

        if not tool_call.name:
            raise MalformedAgentResponseError(
                "Agent tool action is missing a tool name."
            )

        arguments = tool_call.arguments or {}

        if tool_call.name == MEMORY_TOOL_NAME:
            query = arguments.get("query")

            if not isinstance(query, str) or not query.strip():
                raise MalformedAgentResponseError(
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
                raise MalformedAgentResponseError(
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

    if response.text is not None:
        text = response.text.strip()

        if text:
            return AgentAction(
                type=AgentActionType.ANSWER,
                response=text,
            )

    raise MalformedAgentResponseError(
        "LLM response did not contain a valid answer or action."
    )
