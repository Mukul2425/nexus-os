from __future__ import annotations

from evaluation.agent.models import AgentEvaluationTask
from app.services.agent.service import AgentService
from app.services.llm.factory import create_llm_provider
from app.database.session import SessionLocal
from app.services.memory.retriever import MemoryRetriever

def execute_agent_task(
    task: AgentEvaluationTask,
):
    """
    Execute one evaluation task using the real Nexus AgentService.
    """

    db = SessionLocal()

    try:
        service = AgentService(
            db=db,
            llm_provider=create_llm_provider(),
            memory_retriever=MemoryRetriever(db),
        )

        return service.run(
            conversation_id=task.conversation_id,
            task=task.message,
        )

    finally:
        db.close()