from app.prompts.base import SYSTEM_PROMPT
from app.schemas.chat import ChatMessage


def prepare_chat_messages(
    messages: list[ChatMessage],
) -> list[ChatMessage]:

    system_message = ChatMessage(
        role="system",
        content=SYSTEM_PROMPT,
    )

    return [
        system_message,
        *messages,
    ]