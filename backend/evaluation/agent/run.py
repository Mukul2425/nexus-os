from __future__ import annotations

import json
from pathlib import Path

from evaluation.agent.app_runner import execute_agent_task
from evaluation.agent.evaluator import AgentEvaluator
from evaluation.agent.runner import AgentEvaluationRunner


def main() -> None:
    tasks_path = Path("evaluation/agent/tasks.json")
    output_path = Path("evaluation/agent/report.json")

    tasks = AgentEvaluationRunner.load_tasks(
        tasks_path
    )

    runner = AgentEvaluationRunner(
        execute=execute_agent_task,
        evaluator=AgentEvaluator(),
    )

    report = runner.run(tasks)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report.to_dict(),
            file,
            indent=2,
            ensure_ascii=False,
        )

    metrics = report.metrics

    print("\nNexus Agent Evaluation")
    print("=" * 32)

    print(
        f"Tasks:                 {metrics.total_tasks}"
    )
    print(
        f"Successful:            {metrics.successful_tasks}"
    )
    print(
        f"Task success rate:     {metrics.task_success_rate:.2%}"
    )
    print(
        f"Tool selection:        {metrics.tool_selection_accuracy:.2%}"
    )
    print(
        f"Tool execution:        {metrics.tool_execution_success_rate:.2%}"
    )
    print(
        f"Average steps:         {metrics.average_steps:.2f}"
    )
    print(
        "Avg unnecessary tools: "
        f"{metrics.average_unnecessary_tool_calls:.2f}"
    )
    print(
        f"Max-step failures:     {metrics.maximum_step_failures}"
    )
    print(
        f"Answer relevance:      {metrics.average_answer_relevance:.2%}"
    )
    print(
        f"Groundedness:          {metrics.average_groundedness:.2%}"
    )

    print(
        f"\nReport written to: {output_path}"
    )


if __name__ == "__main__":
    main()