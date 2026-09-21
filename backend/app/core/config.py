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
        default="1.0.0"
    )

    LLM_PROVIDER: str = Field(
        default="gemini"
    )

    GEMINI_API_KEY: str

    DATABASE_URL: str = Field(
        default="sqlite:///./nexus.db"
    )

    # ---------------------------------------------------------
    # Gemini request safety
    # ---------------------------------------------------------

    GEMINI_TIMEOUT_SECONDS: float = Field(
        default=20.0,
        gt=0,
    )

    GEMINI_MAX_RETRIES: int = Field(
        default=1,
        ge=1,
    )

    GEMINI_RETRY_INITIAL_DELAY_SECONDS: float = Field(
        default=1.0,
        ge=0,
    )

    GEMINI_RETRY_MAX_DELAY_SECONDS: float = Field(
        default=3.0,
        ge=0,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()