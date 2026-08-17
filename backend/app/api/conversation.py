from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import ConversationResponse

router = APIRouter()


@router.post(
    "/conversation",
    response_model=ConversationResponse,
)
def create_conversation(
    db: Session = Depends(get_db),
):
    repo = ConversationRepository(db)

    conversation = repo.create()

    return ConversationResponse(
        conversation_id=conversation.id
    )