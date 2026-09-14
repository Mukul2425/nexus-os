from pytest import raises

from app.services.agent.planner import AgentPlanner


def test_direct_task_creates_single_step_plan():
    planner = AgentPlanner()

    plan = planner.create_plan("What is FastAPI?")

    assert plan == ["What is FastAPI?"]


def test_then_task_is_decomposed():
    planner = AgentPlanner()

    plan = planner.create_plan(
        "Get the time in London and then calculate "
        "how many hours remain until midnight."
    )

    assert len(plan) == 2
    assert "Get the time in London" in plan[0]
    assert "calculate" in plan[1].lower()


def test_sequential_plan_preserves_order():
    planner = AgentPlanner()

    plan = planner.create_plan(
        "First get the time. Next calculate the difference. "
        "Finally answer the user."
    )

    assert len(plan) == 3
    assert "get the time" in plan[0].lower()
    assert "calculate" in plan[1].lower()
    assert "answer" in plan[2].lower()


def test_plan_is_limited():
    planner = AgentPlanner(max_steps=2)

    plan = planner.create_plan(
        "First inspect memory. "
        "Next inspect RAG. "
        "Then calculate. "
        "Finally answer."
    )

    assert len(plan) <= 2


def test_empty_task_is_rejected():
    planner = AgentPlanner()

    with raises(ValueError):
        planner.create_plan("")


def test_whitespace_task_is_rejected():
    planner = AgentPlanner()

    with raises(ValueError):
        planner.create_plan("   ")


def test_plan_never_exceeds_configured_limit():
    planner = AgentPlanner(max_steps=1)

    plan = planner.create_plan(
        "Get the time and then calculate the difference."
    )

    assert len(plan) == 1

def test_planner_limits_plan_length():
    planner = AgentPlanner(max_steps=2)

    plan = planner.create_plan(
        "first inspect the system "
        "then inspect memory "
        "then inspect RAG "
        "then calculate "
        "finally answer"
    )

    assert len(plan) <= 2

    