class NexusException(Exception):
    """
    Base exception for application-level errors.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class LLMProviderError(NexusException):

    def __init__(
        self,
        message: str = "Unable to generate a response",
    ):
        super().__init__(
            code="LLM_PROVIDER_ERROR",
            message=message,
            status_code=502,
        )


class ConversationNotFoundError(NexusException):

    def __init__(self):
        super().__init__(
            code="CONVERSATION_NOT_FOUND",
            message="Conversation not found",
            status_code=404,
        )

class UnknownToolError(NexusException):

    def __init__(
        self,
        tool_name: str,
    ):
        super().__init__(
            code="UNKNOWN_TOOL",
            message=f"Unknown tool: {tool_name}",
            status_code=400,
        )


class InvalidToolArgumentsError(NexusException):

    def __init__(
        self,
        tool_name: str,
        message: str,
    ):
        super().__init__(
            code="INVALID_TOOL_ARGUMENTS",
            message=(
                f"Invalid arguments for tool "
                f"'{tool_name}': {message}"
            ),
            status_code=400,
        )


class ToolExecutionError(NexusException):

    def __init__(
        self,
        tool_name: str,
        message: str = "Tool execution failed",
    ):
        super().__init__(
            code="TOOL_EXECUTION_ERROR",
            message=(
                f"{tool_name}: {message}"
            ),
            status_code=500,
        )

class MemoryNotFoundError(NexusException):
    def __init__(self):
        super().__init__(
            code="MEMORY_NOT_FOUND",
            message="Memory not found.",
            status_code=404,
        )


class InvalidMemoryError(NexusException):
    def __init__(self, message: str = "Invalid memory."):
        super().__init__(
            code="INVALID_MEMORY",
            message=message,
            status_code=400,
        )