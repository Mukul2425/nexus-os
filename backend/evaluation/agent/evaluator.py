from __future__ import annotations

import re
from typing import Any

from app.schemas.agent import AgentResult

from evaluation.agent.models import (
    AgentEvaluationExpectation,
    AgentEvaluationTask,
    EvaluationMetrics,
    EvaluationReport,
    TaskEvaluation,
)


class AgentEvaluator:
    """
    Deterministic evaluator for Nexus AgentResult objects.

    The evaluator intentionally avoids an LLM-as-a-judge dependency.
    Evaluation is based on observable execution behavior and explicit
    task expectations.
    """

    VERSION = "1.0"

    def evaluate_task(
        self,
        task: AgentEvaluationTask,
        result: AgentResult,
    ) -> TaskEvaluation:
        expected = task.expected

        errors: list[str] = []

        status_correct = self._status_correct(
            result=result,
            expected=expected,
        )

        if not status_correct:
            errors.append(
                f"Expected status '{expected.status}', "
                f"got '{result.status.value}'."
            )

        action_sequence = self._action_sequence(result)
        action_sequence_correct = self._sequence_matches(
            actual=action_sequence,
            expected=expected.action_types,
        )

        if not action_sequence_correct:
            errors.append(
                "Action sequence mismatch: "
                f"expected={list(expected.action_types)}, "
                f"actual={action_sequence}."
            )

        actual_tools = self._tool_sequence(result)

        tool_selection_correct = self._tool_selection_correct(
            actual=actual_tools,
            expected=expected.tool_names,
        )

        if expected.tool_names and not tool_selection_correct:
            errors.append(
                "Tool selection mismatch: "
                f"expected={list(expected.tool_names)}, "
                f"actual={actual_tools}."
            )

        tool_execution_success = self._tool_execution_success(result)

        if not tool_execution_success:
            errors.append("At least one executed tool failed.")

        unnecessary_tool_calls = max(
            0,
            result.tool_call_count - len(expected.tool_names),
        )

        if expected.max_tool_calls is not None:
            if result.tool_call_count > expected.max_tool_calls:
                errors.append(
                    f"Tool-call limit exceeded: "
                    f"{result.tool_call_count} > "
                    f"{expected.max_tool_calls}."
                )

        if result.tool_call_count < expected.min_tool_calls:
            errors.append(
                f"Too few tool calls: "
                f"{result.tool_call_count} < "
                f"{expected.min_tool_calls}."
            )

        max_step_failure = (
            result.status.value == "max_steps_reached"
        )

        if expected.max_steps is not None:
            if result.step_count > expected.max_steps:
                errors.append(
                    f"Step limit exceeded: "
                    f"{result.step_count} > "
                    f"{expected.max_steps}."
                )

        answer_relevance = self._answer_relevance(
            result=result,
            expected=expected,
        )

        if expected.required_keywords and answer_relevance < 1.0:
            errors.append(
                "Final answer is missing one or more required keywords."
            )

        groundedness = self._groundedness(
            result=result,
            expected=expected,
        )

        if expected.requires_rag and groundedness < 1.0:
            errors.append(
                "RAG was required but no retrieved documents "
                "were available."
            )
        memory_requirement_satisfied = (
             not expected.requires_memory 
             or bool(result.retrieved_memories) 
             )

        if expected.requires_memory and not memory_requirement_satisfied: 
            errors.append( 
                "Memory retrieval was required but no memories " "were returned."
        )

        passed = (
            status_correct
            and action_sequence_correct
            and tool_selection_correct
            and tool_execution_success
            and not max_step_failure
            and answer_relevance == 1.0
            and groundedness == 1.0
            and memory_requirement_satisfied
            and result.tool_call_count >= expected.min_tool_calls
            and (
                expected.max_tool_calls is None
                or result.tool_call_count <= expected.max_tool_calls
            )
            and (
                expected.max_steps is None
                or result.step_count <= expected.max_steps
            )
        )

        return TaskEvaluation(
            task_id=task.id,
            category=task.category,
            passed=passed,
            status_correct=status_correct,
            action_sequence_correct=action_sequence_correct,
            tool_selection_correct=tool_selection_correct,
            tool_execution_success=tool_execution_success,
            unnecessary_tool_calls=unnecessary_tool_calls,
            step_count=result.step_count,
            tool_call_count=result.tool_call_count,
            max_step_failure=max_step_failure,
            answer_relevance=answer_relevance,
            groundedness=groundedness,
            errors=errors,
        )

    def evaluate(
        self,
        tasks: list[AgentEvaluationTask],
        results: dict[str, AgentResult],
    ) -> EvaluationReport:
        evaluations: list[TaskEvaluation] = []

        for task in tasks:
            result = results.get(task.id)

            if result is None:
                evaluations.append(
                    TaskEvaluation(
                        task_id=task.id,
                        category=task.category,
                        passed=False,
                        status_correct=False,
                        action_sequence_correct=False,
                        tool_selection_correct=False,
                        tool_execution_success=False,
                        unnecessary_tool_calls=0,
                        step_count=0,
                        tool_call_count=0,
                        max_step_failure=False,
                        answer_relevance=0.0,
                        groundedness=0.0,
                        errors=["No AgentResult produced for task."],
                    )
                )
                continue

            evaluations.append(
                self.evaluate_task(task, result)
            )

        return EvaluationReport(
            version=self.VERSION,
            task_results=evaluations,
            metrics=self._calculate_metrics(evaluations),
        )

    @staticmethod
    def _status_correct(
        result: AgentResult,
        expected: AgentEvaluationExpectation,
    ) -> bool:
        return result.status.value == expected.status

    @staticmethod
    def _action_sequence(
        result: AgentResult,
    ) -> list[str]:
        return [
            step.action.type.value
            for step in result.steps
        ]

    @staticmethod
    def _tool_sequence(
        result: AgentResult,
    ) -> list[str]:
        return [
            step.action.tool_name
            for step in result.steps
            if step.action.type.value == "tool"
            and step.action.tool_name
        ]

    @staticmethod
    def _sequence_matches(
        actual: list[str],
        expected: tuple[str, ...],
    ) -> bool:
        if not expected:
            return True

        if len(actual) != len(expected):
            return False

        return actual == list(expected)

    @staticmethod
    def _tool_selection_correct(
        actual: list[str],
        expected: tuple[str, ...],
    ) -> bool:
        if not expected:
            return len(actual) == 0

        return actual == list(expected)

    @staticmethod
    def _tool_execution_success(
        result: AgentResult,
    ) -> bool:
        tool_steps = [
            step
            for step in result.steps
            if step.action.type.value == "tool"
        ]

        return all(step.success for step in tool_steps)

    @classmethod
    def _answer_relevance(
        cls,
        result: AgentResult,
        expected: AgentEvaluationExpectation,
    ) -> float:
        if not expected.required_keywords:
            return 1.0 if result.response else 0.0

        if not result.response:
            return 0.0

        normalized_answer = cls._normalize(result.response)

        matches = sum(
            1
            for keyword in expected.required_keywords
            if cls._normalize(keyword) in normalized_answer
        )

        return matches / len(expected.required_keywords)

    @staticmethod
    def _groundedness(
        result: AgentResult,
        expected: AgentEvaluationExpectation,
    ) -> float:
        if not expected.requires_rag:
            return 1.0

        if not result.retrieved_documents:
            return 0.0

        return 1.0

    @staticmethod
    def _normalize(value: Any) -> str:
        return re.sub(
            r"\s+",
            " ",
            str(value).lower().strip(),
        ).replace(",", "")

    @staticmethod
    def _calculate_metrics(
        evaluations: list[TaskEvaluation],
    ) -> EvaluationMetrics:
        total = len(evaluations)

        if total == 0:
            return EvaluationMetrics(
                total_tasks=0,
                successful_tasks=0,
                task_success_rate=0.0,
                tool_selection_accuracy=0.0,
                tool_execution_success_rate=0.0,
                average_steps=0.0,
                average_unnecessary_tool_calls=0.0,
                maximum_step_failures=0,
                average_answer_relevance=0.0,
                average_groundedness=0.0,
            )

        successful = sum(
            evaluation.passed
            for evaluation in evaluations
        )

        tool_selection = sum(
            evaluation.tool_selection_correct
            for evaluation in evaluations
        )

        tool_execution = sum(
            evaluation.tool_execution_success
            for evaluation in evaluations
        )

        return EvaluationMetrics(
            total_tasks=total,
            successful_tasks=successful,
            task_success_rate=successful / total,
            tool_selection_accuracy=tool_selection / total,
            tool_execution_success_rate=tool_execution / total,
            average_steps=(
                sum(e.step_count for e in evaluations) / total
            ),
            average_unnecessary_tool_calls=(
                sum(
                    e.unnecessary_tool_calls
                    for e in evaluations
                )
                / total
            ),
            maximum_step_failures=sum(
                e.max_step_failure
                for e in evaluations
            ),
            average_answer_relevance=(
                sum(
                    e.answer_relevance
                    for e in evaluations
                )
                / total
            ),
            average_groundedness=(
                sum(
                    e.groundedness
                    for e in evaluations
                )
                / total
            ),
        )