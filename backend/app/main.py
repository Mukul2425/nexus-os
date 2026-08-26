from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router

from app.core.config import settings

from app.database.base import Base
from app.database.session import engine

from app.logging.middleware import LoggingMiddleware
from app.core.exceptions import NexusException
from app.core.exception_handlers import nexus_exception_handler
from app.api.documents import router as documents_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Nexus Backend",
    version=settings.VERSION,
)

app.add_middleware(
    LoggingMiddleware
)

app.include_router(chat_router)
app.include_router(conversation_router)
app.add_exception_handler(
    NexusException,
    nexus_exception_handler,
)
app.include_router(
    documents_router
)