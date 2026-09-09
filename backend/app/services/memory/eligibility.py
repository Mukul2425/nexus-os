from app.schemas.memory_extraction import MemoryCandidate


MIN_CONFIDENCE = 0.70


class MemoryEligibilityService:

    def is_eligible(
        self,
        candidate: MemoryCandidate,
    ) -> bool:
        content = candidate.content.strip()

        if not content:
            return False

        if candidate.confidence < MIN_CONFIDENCE:
            return False

        if candidate.memory_type not in {
            "semantic",
            "episodic",
        }:
            return False

        # Questions are generally not memories.
        if content.endswith("?"):
            return False

        # Reject obvious transient conversational content.
        transient_prefixes = (
            "what is ",
            "what's ",
            "how do i ",
            "how can i ",
            "can you ",
            "could you ",
            "please ",
            "tell me ",
        )

        normalized = content.lower()

        if normalized.startswith(transient_prefixes):
            return False

        return True

    def filter(
        self,
        candidates: list[MemoryCandidate],
    ) -> list[MemoryCandidate]:
        return [
            candidate
            for candidate in candidates
            if self.is_eligible(candidate)
        ]