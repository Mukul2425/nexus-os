from __future__ import annotations

from dataclasses import dataclass


MAX_PLAN_STEPS = 5


@dataclass(frozen=True)
class PlanStep:
    step_number: int
    description: str
    status: str = "pending"


class AgentPlanner:
    """
    Lightweight deterministic planner.

    The planner does not execute actions or make tool decisions.
    It creates a short task decomposition that the AgentService
    can use to track progress.
    """

    def __init__(self, max_steps: int = MAX_PLAN_STEPS):
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")

        self.max_steps = max_steps

    def create_plan(self, task: str) -> list[str]:
        if not task or not task.strip():
            raise ValueError("task cannot be empty")

        task = task.strip()

        # Keep simple/direct tasks lightweight.
        if self._looks_like_direct_task(task):
            return [task]

        steps = self._decompose(task)

        if not steps:
            return [task]

        return steps[: self.max_steps]

    def _looks_like_direct_task(self, task: str) -> bool:
        lowered = task.lower()

        multi_step_markers = (
            " and then ",
            " then ",
            "after that",
            "followed by",
            "first ",
            "next ",
            "finally ",
            "using ",
        )

        return not any(marker in lowered for marker in multi_step_markers)

    def _decompose(self, task: str) -> list[str]:
        normalized = task.strip()

        # Explicit sequential wording.
        for separator in (
            " and then ",
            " then ",
            " after that ",
            " followed by ",
        ):
            if separator in normalized.lower():
                parts = self._split_case_insensitive(
                    normalized,
                    separator,
                )
                if len(parts) > 1:
                    return [
                        part.strip(" .")
                        for part in parts
                        if part.strip(" .")
                    ]

        # "First ..., next ..., finally ..." style.
        lowered = normalized.lower()

        if "first " in lowered and " next " in lowered:
            parts = self._split_ordered_task(normalized)
            if parts:
                return parts

        return [normalized]

    def _split_case_insensitive(
        self,
        text: str,
        separator: str,
    ) -> list[str]:
        lowered = text.lower()
        separator_lower = separator.lower()

        parts: list[str] = []
        start = 0

        while True:
            index = lowered.find(separator_lower, start)

            if index == -1:
                parts.append(text[start:])
                break

            parts.append(text[start:index])
            start = index + len(separator)

        return parts

    def _split_ordered_task(self, task: str) -> list[str]:
        markers = ("first ", " next ", " finally ")

        lowered = task.lower()
        positions: list[tuple[int, str]] = []

        for marker in markers:
            position = lowered.find(marker)

            if position != -1:
                positions.append((position, marker.strip()))

        if not positions:
            return []

        positions.sort()

        result: list[str] = []

        for index, (position, marker) in enumerate(positions):
            content_start = position + len(marker)

            if index + 1 < len(positions):
                content_end = positions[index + 1][0]
            else:
                content_end = len(task)

            content = task[content_start:content_end].strip(" .,")

            if content:
                result.append(content)

        return result