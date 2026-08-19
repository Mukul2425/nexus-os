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