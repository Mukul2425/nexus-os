from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = Field(
        default="development"
    )

    VERSION: str = Field(
        default="0.7.0"
    )

    LLM_PROVIDER: str = Field(
        default="gemini"
    )

    GEMINI_API_KEY: str

    DATABASE_URL: str = Field(
        default="sqlite:///./nexus.db"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()