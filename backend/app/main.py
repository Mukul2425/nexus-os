from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router

from app.database.base import Base
from app.database.session import engine

from app.logging.middleware import LoggingMiddleware


Base.metadata.create_all(bind=engine)
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)
app.add_middleware(LoggingMiddleware)

app.include_router(chat_router)
app.include_router(conversation_router)