import json

from app.schemas.chat import ChatMessage
from app.services.llm.provider import LLMProvider


CONFLICT_PROMPT = """
You are a memory conflict detector.

Compare a NEW memory against an EXISTING memory.

Determine whether the new memory contradicts the existing memory.

Examples:

Existing:
User prefers Python.

New:
User prefers TypeScript.

Result:
{
    "conflict": true
}

Existing:
User prefers Python.

New:
User uses FastAPI.

Result:
{
    "conflict": false
}

Existing:
User is building Nexus OS.

New:
User is building an AI chatbot.

Result:
{
    "conflict": false
}

Rules:
- Only mark conflict when the two memories cannot reasonably both be true.
- Similarity alone is NOT a conflict.
- Different preferences may be conflicting.
- Different projects are NOT conflicting.
- Return ONLY valid JSON.

Format:
{
    "conflict": true
}
"""


class MemoryConflictDetector:

    def __init__(
        self,
        llm_provider: LLMProvider,
    ):
        self.llm_provider = llm_provider

    def is_conflict(
        self,
        existing_memory: str,
        new_memory: str,
    ) -> bool:

        prompt = (
            f"{CONFLICT_PROMPT}\n\n"
            f"EXISTING MEMORY:\n{existing_memory}\n\n"
            f"NEW MEMORY:\n{new_memory}"
        )

        response = self.llm_provider.generate(
            [
                ChatMessage(
                    role="user",
                    content=prompt,
                )
            ]
        )

        try:
            payload = json.loads(response)
            return bool(payload.get("conflict", False))
        except Exception:
            # Conflict detection must never break memory creation.
            return False