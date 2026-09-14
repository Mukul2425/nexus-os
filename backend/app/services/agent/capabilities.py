from app.schemas.llm import ToolDefinition


MEMORY_TOOL_NAME = "memory_retrieval"
RAG_TOOL_NAME = "rag_retrieval"


def get_agent_capability_definitions() -> list[ToolDefinition]:
    """
    Return capabilities that belong to the agent orchestration layer.

    These are intentionally not registered in ToolRegistry because they
    are internal orchestration capabilities rather than user-facing tools.
    """

    return [
        ToolDefinition(
            name=MEMORY_TOOL_NAME,
            description=(
                "Retrieve relevant persistent memories about the user. "
                "Use this only when the task may depend on the user's "
                "preferences, prior decisions, background, or other "
                "stored personal context."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A concise query describing the information "
                            "needed from persistent memory."
                        ),
                    }
                },
                "required": ["query"],
            },
        ),
        ToolDefinition(
            name=RAG_TOOL_NAME,
            description=(
                "Retrieve relevant information from the Nexus knowledge "
                "base and project documentation. Use this when answering "
                "questions that require project-specific or documented "
                "knowledge."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The question to search for in the knowledge base."
                        ),
                    }
                },
                "required": ["query"],
            },
        ),
    ]