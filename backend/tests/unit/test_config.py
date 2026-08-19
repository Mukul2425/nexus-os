from app.core.config import settings


def test_settings():

    assert settings.VERSION == "0.4.0"

    assert settings.LLM_PROVIDER == "gemini"

    assert settings.DATABASE_URL


def test_settings_have_required_values():

    assert settings.VERSION
    assert settings.ENVIRONMENT
    assert settings.LLM_PROVIDER
    assert settings.GEMINI_API_KEY
    assert settings.DATABASE_URL