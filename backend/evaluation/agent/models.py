from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentEvaluationExpectation:
    status: str = "completed"
    action_types: tuple[str, ...] = ()
    tool_names: tuple[str, ...] = ()
    required_keywords: tuple[str, ...] = ()

    min_tool_calls: int = 0
    max_tool_calls: int | None = None
    max_steps: int | None = None

    requires_rag: bool = False
    requires_memory: bool = False


@dataclass(frozen=True)
class AgentEvaluationTask:
    id: str
    category: str
    conversation_id: str
    message: str
    expected: AgentEvaluationExpectation


@dataclass
class TaskEvaluation:
    task_id: str
    category: str

    passed: bool

    status_correct: bool
    action_sequence_correct: bool
    tool_selection_correct: bool
    tool_execution_success: bool

    unnecessary_tool_calls: int
    step_count: int
    tool_call_count: int

    max_step_failure: bool

    answer_relevance: float
    groundedness: float

    errors: list[str] = field(default_factory=list)


@dataclass
class EvaluationMetrics:
    total_tasks: int
    successful_tasks: int

    task_success_rate: float
    tool_selection_accuracy: float
    tool_execution_success_rate: float

    average_steps: float
    average_unnecessary_tool_calls: float

    maximum_step_failures: int

    average_answer_relevance: float
    average_groundedness: float


@dataclass
class EvaluationReport:
    version: str
    task_results: list[TaskEvaluation]
    metrics: EvaluationMetrics

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "metrics": {
                "total_tasks": self.metrics.total_tasks,
                "successful_tasks": self.metrics.successful_tasks,
                "task_success_rate": self.metrics.task_success_rate,
                "tool_selection_accuracy": self.metrics.tool_selection_accuracy,
                "tool_execution_success_rate": (
                    self.metrics.tool_execution_success_rate
                ),
                "average_steps": self.metrics.average_steps,
                "average_unnecessary_tool_calls": (
                    self.metrics.average_unnecessary_tool_calls
                ),
                "maximum_step_failures": self.metrics.maximum_step_failures,
                "average_answer_relevance": (
                    self.metrics.average_answer_relevance
                ),
                "average_groundedness": (
                    self.metrics.average_groundedness
                ),
            },
            "tasks": [
                {
                    "task_id": result.task_id,
                    "category": result.category,
                    "passed": result.passed,
                    "status_correct": result.status_correct,
                    "action_sequence_correct": result.action_sequence_correct,
                    "tool_selection_correct": result.tool_selection_correct,
                    "tool_execution_success": result.tool_execution_success,
                    "unnecessary_tool_calls": result.unnecessary_tool_calls,
                    "step_count": result.step_count,
                    "tool_call_count": result.tool_call_count,
                    "max_step_failure": result.max_step_failure,
                    "answer_relevance": result.answer_relevance,
                    "groundedness": result.groundedness,
                    "errors": result.errors,
                }
                for result in self.task_results
            ],
        }