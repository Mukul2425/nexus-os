from unittest.mock import MagicMock, patch

from app.schemas.agent import (
    AgentResult,
    AgentStatus,
)


def test_agent_run_success(client):
    conversation_response = client.post(
        "/conversation"
    )

    assert conversation_response.status_code == 200

    conversation_id = (
        conversation_response.json()["conversation_id"]
    )

    mock_result = AgentResult(
        execution_id="execution-123",
        conversation_id=conversation_id,
        status=AgentStatus.COMPLETED,
        response="125 * 42 = 5250.",
        steps=[],
        plan=[
            "Calculate 125 * 42.",
            "Return the result.",
        ],
        plan_progress=[
            {
                "step": 1,
                "status": "completed",
            },
            {
                "step": 2,
                "status": "completed",
            },
        ],
        step_count=2,
        tool_call_count=1,
        error=None,
    )

    mock_service = MagicMock()
    mock_service.run.return_value = mock_result

    with patch(
        "app.api.agent.get_agent_service",
        return_value=mock_service,
    ):
        response = client.post(
            "/agent/run",
            json={
                "conversation_id": conversation_id,
                "message": "Calculate 125 * 42.",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["execution_id"] == "execution-123"
    assert body["conversation_id"] == conversation_id
    assert body["status"] == "completed"
    assert body["response"] == "125 * 42 = 5250."
    assert body["step_count"] == 2
    assert body["tool_call_count"] == 1

def test_agent_run_passes_request_to_service(client):
    conversation_id = "conversation-123"

    mock_result = AgentResult(
        execution_id="execution-123",
        conversation_id=conversation_id,
        status=AgentStatus.COMPLETED,
        response="Done.",
        steps=[],
        plan=[],
        plan_progress=[],
        step_count=1,
        tool_call_count=0,
    )

    mock_service = MagicMock()
    mock_service.run.return_value = mock_result

    with patch(
        "app.api.agent.get_agent_service",
        return_value=mock_service,
    ):
        response = client.post(
            "/agent/run",
            json={
                "conversation_id": conversation_id,
                "message": "Do something.",
            },
        )

    assert response.status_code == 200

    mock_service.run.assert_called_once_with(
        conversation_id=conversation_id,
        task="Do something.",
    )

def test_agent_run_missing_message(client):
    response = client.post(
        "/agent/run",
        json={
            "conversation_id": "c1",
        },
    )

    assert response.status_code == 422

def test_agent_run_missing_conversation_id(client):
    response = client.post(
        "/agent/run",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 422

def test_agent_run_empty_message(client):
    response = client.post(
        "/agent/run",
        json={
            "conversation_id": "c1",
            "message": "",
        },
    )

    assert response.status_code == 422

def test_agent_run_empty_conversation_id(client):
    response = client.post(
        "/agent/run",
        json={
            "conversation_id": "",
            "message": "Hello",
        },
    )

    assert response.status_code == 422

def test_agent_run_missing_body(client):
    response = client.post(
        "/agent/run"
    )

    assert response.status_code == 422

def test_agent_run_returns_controlled_failure(client):
    mock_result = AgentResult(
        execution_id="execution-failed",
        conversation_id="c1",
        status=AgentStatus.FAILED,
        response=None,
        steps=[],
        plan=[],
        plan_progress=[],
        step_count=1,
        tool_call_count=0,
        error="Agent produced an invalid response.",
    )

    mock_service = MagicMock()
    mock_service.run.return_value = mock_result

    with patch(
        "app.api.agent.get_agent_service",
        return_value=mock_service,
    ):
        response = client.post(
            "/agent/run",
            json={
                "conversation_id": "c1",
                "message": "Do something.",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "failed"
    assert body["error"] == (
        "Agent produced an invalid response."
    )

def test_agent_run_returns_max_steps_status(client):
    mock_result = AgentResult(
        execution_id="execution-max-steps",
        conversation_id="c1",
        status=AgentStatus.MAX_STEPS_REACHED,
        response=None,
        steps=[],
        plan=[],
        plan_progress=[],
        step_count=10,
        tool_call_count=3,
        error="Maximum agent steps reached.",
    )

    mock_service = MagicMock()
    mock_service.run.return_value = mock_result

    with patch(
        "app.api.agent.get_agent_service",
        return_value=mock_service,
    ):
        response = client.post(
            "/agent/run",
            json={
                "conversation_id": "c1",
                "message": "Keep working forever.",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "max_steps_reached"
    assert body["step_count"] == 10
    assert body["error"] == (
        "Maximum agent steps reached."
    )


