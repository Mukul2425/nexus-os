from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.memory import (
    MemoryCreate,
    MemoryListResponse,
    MemoryResponse,
    MemoryUpdate,
)
from app.services.memory.service import MemoryService


router = APIRouter(
    prefix="/memories",
    tags=["memories"],
)


def _to_response(memory) -> MemoryResponse:
    return MemoryResponse(
        id=memory.id,
        content=memory.content,
        memory_type=memory.memory_type,
        importance=memory.importance,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=201,
)
def create_memory(
    request: MemoryCreate,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memory = service.create(
        content=request.content,
        memory_type=request.memory_type,
        importance=request.importance,
    )

    return _to_response(memory)


@router.get(
    "",
    response_model=MemoryListResponse,
)
def list_memories(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memories = service.list(
        limit=limit,
        offset=offset,
    )

    return MemoryListResponse(
        memories=[
            _to_response(memory)
            for memory in memories
        ],
        total=service.repository.count(),
    )


@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
)
def get_memory(
    memory_id: str,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    return _to_response(
        service.get(memory_id)
    )


@router.patch(
    "/{memory_id}",
    response_model=MemoryResponse,
)
def update_memory(
    memory_id: str,
    request: MemoryUpdate,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memory = service.update(
        memory_id,
        content=request.content,
        memory_type=request.memory_type,
        importance=request.importance,
    )

    return _to_response(memory)


@router.delete(
    "/{memory_id}",
    status_code=204,
)
def delete_memory(
    memory_id: str,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    service.delete(memory_id)

    return None