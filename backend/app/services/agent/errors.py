class AgentExecutionError(Exception):
    """Base class for controlled agent execution failures."""


class AgentTimeoutError(AgentExecutionError):
    """Agent execution exceeded its configured timeout."""


class AgentMaxStepsError(AgentExecutionError):
    """Agent exceeded its maximum execution steps."""


class AgentMaxToolCallsError(AgentExecutionError):
    """Agent exceeded its maximum tool calls."""


class AgentLoopDetectedError(AgentExecutionError):
    """Agent repeated the same action beyond the allowed limit."""


class InvalidAgentActionError(AgentExecutionError):
    """Agent selected an invalid or unsupported action."""


class UnknownAgentToolError(AgentExecutionError):
    """Agent selected a tool that is not registered."""


class MalformedAgentResponseError(AgentExecutionError):
    """LLM returned a response that cannot be interpreted safely."""

    