from app.schemas.agent import (
    AgentAction,
    AgentActionType,
    AgentResult,
    AgentStatus,
    AgentStep,
)

from evaluation.agent.evaluator import AgentEvaluator
from evaluation.agent.models import (
    AgentEvaluationExpectation,
    AgentEvaluationTask,
)


def make_task(
    *,
    task_id="task-1",
    category="tool",
    action_types=("tool", "answer"),
    tool_names=("calculator",),
    keywords=("5250",),
    min_tool_calls=1,
    max_tool_calls=1,
    max_steps=3,
    requires_rag=False,
    requires_memory=False,
):
    return AgentEvaluationTask(
        id=task_id,
        category=category,
        conversation_id=f"conversation-{task_id}",
        message="test task",
        expected=AgentEvaluationExpectation(
            action_types=action_types,
            tool_names=tool_names,
            required_keywords=keywords,
            min_tool_calls=min_tool_calls,
            max_tool_calls=max_tool_calls,
            max_steps=max_steps,
            requires_rag=requires_rag,
            requires_memory=requires_memory,
        ),
    )


def make_result(
    *,
    status=AgentStatus.COMPLETED,
    steps=None,
    response="The answer is 5250.",
    tool_call_count=1,
    retrieved_documents=None,
    retrieved_memories=None,
):
    return AgentResult(
        execution_id="execution-1",
        conversation_id="conversation-task-1",
        status=status,
        response=response,
        steps=steps or [],
        step_count=len(steps or []),
        tool_call_count=tool_call_count,
        retrieved_documents=retrieved_documents or [],
        retrieved_memories=retrieved_memories or [],
    )


def test_successful_calculator_task():
    task = make_task()

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
                arguments={"expression": "125 * 42"},
            ),
            observation="5250",
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="The answer is 5250.",
            ),
            success=True,
        ),
    ]

    result = make_result(steps=steps)

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.passed is True
    assert evaluation.tool_selection_correct is True
    assert evaluation.tool_execution_success is True
    assert evaluation.answer_relevance == 1.0
    assert evaluation.unnecessary_tool_calls == 0


def test_wrong_tool_selection_fails():
    task = make_task()

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="time",
            ),
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="The answer is 5250.",
            ),
            success=True,
        ),
    ]

    result = make_result(steps=steps)

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.passed is False
    assert evaluation.tool_selection_correct is False


def test_failed_tool_execution_fails_task():
    task = make_task()

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
            ),
            success=False,
            error="calculator failed",
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="Unable to calculate.",
            ),
            success=True,
        ),
    ]

    result = make_result(
        steps=steps,
        response="Unable to calculate.",
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.passed is False
    assert evaluation.tool_execution_success is False


def test_unnecessary_tool_call_is_counted():
    task = make_task(
        max_tool_calls=2,
    )

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
            ),
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
            ),
            success=True,
        ),
        AgentStep(
            step_number=3,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="The answer is 5250.",
            ),
            success=True,
        ),
    ]

    result = make_result(
        steps=steps,
        tool_call_count=2,
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.unnecessary_tool_calls == 1
    assert evaluation.passed is False


def test_max_step_failure_is_detected():
    task = make_task()

    result = make_result(
        status=AgentStatus.MAX_STEPS_REACHED,
        steps=[],
        response=None,
        tool_call_count=0,
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.passed is False
    assert evaluation.max_step_failure is True


def test_missing_required_keyword_reduces_relevance():
    task = make_task(
        keywords=("5250", "calculator"),
    )

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
            ),
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="The answer is 5250.",
            ),
            success=True,
        ),
    ]

    result = make_result(steps=steps)

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.answer_relevance == 0.5
    assert evaluation.passed is False


def test_rag_groundedness_requires_documents():
    task = make_task(
        category="rag",
        action_types=("rag", "answer"),
        tool_names=(),
        keywords=(),
        min_tool_calls=0,
        max_tool_calls=0,
        requires_rag=True,
    )

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.RAG,
                query="provider architecture",
            ),
            observation="retrieved context",
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="FastAPI provider architecture.",
            ),
            success=True,
        ),
    ]

    result = make_result(
        steps=steps,
        tool_call_count=0,
        retrieved_documents=[],
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.groundedness == 0.0
    assert evaluation.passed is False


def test_rag_task_passes_with_documents():
    task = make_task(
        category="rag",
        action_types=("rag", "answer"),
        tool_names=(),
        keywords=(),
        min_tool_calls=0,
        max_tool_calls=0,
        requires_rag=True,
    )

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.RAG,
                query="provider architecture",
            ),
            observation="retrieved context",
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="FastAPI provider architecture.",
            ),
            success=True,
        ),
    ]

    result = make_result(
        steps=steps,
        tool_call_count=0,
        retrieved_documents=[
            {
                "document": "nexus.md",
                "chunk_id": "chunk-1",
            }
        ],
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.groundedness == 1.0
    assert evaluation.passed is True


def test_memory_requirement_is_enforced():
    task = make_task(
        category="memory",
        action_types=("memory", "answer"),
        tool_names=(),
        keywords=(),
        min_tool_calls=0,
        max_tool_calls=0,
        requires_memory=True,
    )

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.MEMORY,
                query="backend preference",
            ),
            observation="memory result",
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="FastAPI.",
            ),
            success=True,
        ),
    ]

    result = make_result(
        steps=steps,
        tool_call_count=0,
        retrieved_memories=[],
        response="FastAPI.",
    )

    evaluation = AgentEvaluator().evaluate_task(
        task,
        result,
    )

    assert evaluation.passed is False


def test_evaluate_generates_aggregate_metrics():
    evaluator = AgentEvaluator()

    task = make_task()

    steps = [
        AgentStep(
            step_number=1,
            action=AgentAction(
                type=AgentActionType.TOOL,
                tool_name="calculator",
            ),
            success=True,
        ),
        AgentStep(
            step_number=2,
            action=AgentAction(
                type=AgentActionType.ANSWER,
                response="The answer is 5250.",
            ),
            success=True,
        ),
    ]

    result = make_result(steps=steps)

    report = evaluator.evaluate(
        tasks=[task],
        results={task.id: result},
    )

    assert report.version == "1.0"
    assert report.metrics.total_tasks == 1
    assert report.metrics.successful_tasks == 1
    assert report.metrics.task_success_rate == 1.0
    assert report.metrics.tool_selection_accuracy == 1.0
    assert report.metrics.tool_execution_success_rate == 1.0
    assert report.metrics.average_steps == 2.0


def test_missing_result_is_failed():
    evaluator = AgentEvaluator()

    task = make_task()

    report = evaluator.evaluate(
        tasks=[task],
        results={},
    )

    assert report.metrics.total_tasks == 1
    assert report.metrics.successful_tasks == 0
    assert report.metrics.task_success_rate == 0.0

    assert report.task_results[0].passed is False
    assert report.task_results[0].errors == [
        "No AgentResult produced for task."
    ]


def test_empty_evaluation_is_safe():
    report = AgentEvaluator().evaluate(
        tasks=[],
        results={},
    )

    assert report.metrics.total_tasks == 0
    assert report.metrics.successful_tasks == 0
    assert report.metrics.task_success_rate == 0.0


import json
from pathlib import Path

from evaluation.agent.runner import AgentEvaluationRunner


def test_agent_evaluation_dataset_is_valid():
    path = Path("evaluation/agent/tasks.json")

    tasks = AgentEvaluationRunner.load_tasks(path)

    assert tasks
    assert len(tasks) >= 10

    ids = [task.id for task in tasks]

    assert len(ids) == len(set(ids))

    for task in tasks:
        assert task.id
        assert task.category
        assert task.conversation_id
        assert task.message
        assert task.expected.status


def test_agent_evaluation_dataset_is_valid_json():
    path = Path("evaluation/agent/tasks.json")

    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    assert isinstance(payload, dict)
    assert payload["version"] == "1.0"
    assert isinstance(payload["tasks"], list)