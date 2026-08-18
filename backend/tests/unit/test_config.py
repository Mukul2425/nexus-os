from app.core.config import settings


def test_settings():

    assert settings.VERSION == "0.4.0"

    assert settings.LLM_PROVIDER == "gemini"

    assert settings.DATABASE_URL