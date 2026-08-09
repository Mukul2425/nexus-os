from pydantic import BaseModel
from typing import Literal

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
class ChatRequest(BaseModel):

    conversation_id: str

    message: str
class ChatResponse(BaseModel):

    response: str