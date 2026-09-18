from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from app.schemas.agent import AgentResult

from evaluation.agent.evaluator import AgentEvaluator
from evaluation.agent.models import (
    AgentEvaluationExpectation,
    AgentEvaluationTask,
)


class AgentEvaluationRunner:
    """
    Loads agent evaluation cases, executes them, and evaluates
    the resulting AgentResult objects.
    """

    def __init__(
        self,
        execute: Callable[[AgentEvaluationTask], AgentResult],
        evaluator: AgentEvaluator | None = None,
    ) -> None:
        self.execute = execute
        self.evaluator = evaluator or AgentEvaluator()

    @staticmethod
    def load_tasks(
        path: str | Path,
    ) -> list[AgentEvaluationTask]:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Evaluation dataset not found: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            payload = json.load(file)

        if not isinstance(payload, dict):
            raise ValueError(
                "Evaluation dataset must contain a JSON object."
            )

        raw_tasks = payload.get("tasks")

        if not isinstance(raw_tasks, list):
            raise ValueError(
                "Evaluation dataset must contain a 'tasks' list."
            )

        tasks: list[AgentEvaluationTask] = []

        for raw in raw_tasks:
            tasks.append(
                AgentEvaluationTask(
                    id=raw["id"],
                    category=raw["category"],
                    conversation_id=raw["conversation_id"],
                    message=raw["message"],
                    expected=AgentEvaluationExpectation(
                        status=raw["expected"].get(
                            "status",
                            "completed",
                        ),
                        action_types=tuple(
                            raw["expected"].get(
                                "action_types",
                                [],
                            )
                        ),
                        tool_names=tuple(
                            raw["expected"].get(
                                "tool_names",
                                [],
                            )
                        ),
                        required_keywords=tuple(
                            raw["expected"].get(
                                "required_keywords",
                                [],
                            )
                        ),
                        min_tool_calls=raw["expected"].get(
                            "min_tool_calls",
                            0,
                        ),
                        max_tool_calls=raw["expected"].get(
                            "max_tool_calls",
                        ),
                        max_steps=raw["expected"].get(
                            "max_steps",
                        ),
                        requires_rag=raw["expected"].get(
                            "requires_rag",
                            False,
                        ),
                        requires_memory=raw["expected"].get(
                            "requires_memory",
                            False,
                        ),
                    ),
                )
            )

        return tasks

    def run(
        self,
        tasks: list[AgentEvaluationTask],
    ):
        results: dict[str, AgentResult] = {}

        for task in tasks:
            results[task.id] = self.execute(task)

        return self.evaluator.evaluate(
            tasks=tasks,
            results=results,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Nexus OS agent evaluation.",
    )

    parser.add_argument(
        "--tasks",
        default="evaluation/agent/tasks.json",
        help="Path to the agent evaluation dataset.",
    )

    parser.add_argument(
        "--output",
        default="evaluation/agent/report.json",
        help="Path for the generated evaluation report.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    raise RuntimeError(
        "The CLI runner requires an application-specific "
        "AgentService adapter. Use AgentEvaluationRunner "
        "from Python and provide an execute(task) callback."
    )


if __name__ == "__main__":
    main()