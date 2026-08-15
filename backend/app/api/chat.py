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


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    service = ConversationService(db)

    response = service.chat(
        request.conversation_id,
        request.message,
    )

    return ChatResponse(
        response=response,
    )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    service = ConversationService(db)

    return StreamingResponse(
        service.stream_chat(
            request.conversation_id,
            request.message,
        ),
        media_type="text/plain",
    )