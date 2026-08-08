from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.llm import (
    generate_response,
    stream_response,
)

router = APIRouter()

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    response = generate_response(
        request.messages
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