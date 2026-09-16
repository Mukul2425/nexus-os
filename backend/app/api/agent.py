from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.agent import AgentResult
from app.schemas.agent_api import (
    AgentRunRequest,
    AgentRunResponse,
)
from app.services.agent.service import AgentService
from app.services.llm.factory import create_llm_provider


router = APIRouter()


def get_agent_service(
    db: Session = Depends(get_db),
) -> AgentService:
    """
    Construct the agent service for the current request.

    Keeping construction in a dependency makes the endpoint
    easy to test and keeps infrastructure concerns outside
    the route handler.
    """

    return AgentService(
        db=db,
        llm_provider=create_llm_provider(),
    )


def _resolve_agent_service(
    db: Session = Depends(get_db),
) -> AgentService:
    """
    Resolve the agent service for the API route.

    This small wrapper intentionally calls get_agent_service()
    at request time rather than binding it directly to the route.
    That keeps dependency overrides/patching predictable in tests.
    """

    return get_agent_service(db)


@router.post(
    "/agent/run",
    response_model=AgentRunResponse,
)
def run_agent(
    request: AgentRunRequest,
    agent_service: AgentService = Depends(
        _resolve_agent_service
    ),
) -> AgentRunResponse:
    """
    Execute a Nexus agent task.

    The endpoint is intentionally thin:
    validation and orchestration remain inside AgentService.
    """

    result: AgentResult = agent_service.run(
        conversation_id=request.conversation_id,
        task=request.message,
    )

    return AgentRunResponse(
        execution_id=result.execution_id,
        conversation_id=result.conversation_id,
        status=result.status,
        response=result.response,
        steps=result.steps,
        plan=result.plan,
        plan_progress=[
            progress
            if isinstance(progress, dict)
            else {
                "step": index + 1,
                "status": progress,
            }
            for index, progress in enumerate(result.plan_progress)
        ],
        step_count=result.step_count,
        tool_call_count=result.tool_call_count,
        error=result.error,
    )