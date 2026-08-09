from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(chat_router)