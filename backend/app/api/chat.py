from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from app.database.session import SessionLocal

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.conversation_service import (
    ConversationService,
)

from app.services.llm import (
    generate_response,
    stream_response,
)
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    service = ConversationService(db)

    response = service.chat(
        request.conversation_id,
        request.message,
    )


    return ChatResponse(
        response=response
    )

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):

    return StreamingResponse(
        stream_response(request.messages),
        media_type="text/event-stream",
    )