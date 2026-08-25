from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.conversation_service import (
    ConversationService,
)

from app.services.llm.factory import create_llm_provider


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    service = ConversationService(
        db,
        llm_provider=create_llm_provider(),
    )

    answer, sources = service.chat(
        request.conversation_id,
        request.message,
    )

    return ChatResponse(
        response=answer,
        sources=sources,
    )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    llm_provider = create_llm_provider()

    service = ConversationService(
        db,
        llm_provider,
    )

    return StreamingResponse(
        service.stream_chat(
            request.conversation_id,
            request.message,
        ),
        media_type="text/plain",
    )