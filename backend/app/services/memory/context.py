from app.schemas.chat import ChatMessage


MEMORY_CONTEXT_HEADER = (
    "The following memories about the user may be relevant "
    "to the current conversation."
)


def build_memory_context(
    memories: list[dict],
) -> str | None:

    if not memories:
        return None

    lines = [
        MEMORY_CONTEXT_HEADER,
        "",
    ]

    for memory in memories:
        lines.append(
            f"- {memory['content']}"
        )

    return "\n".join(lines)


def build_memory_message(
    memories: list[dict],
) -> ChatMessage | None:

    context = build_memory_context(
        memories
    )

    if context is None:
        return None

    return ChatMessage(
        role="system",
        content=context,
    )