from app.core.config import settings
from app.core.exceptions import LLMProviderError

from app.services.llm.gemini import GeminiProvider
from app.services.llm.provider import LLMProvider


def create_llm_provider() -> LLMProvider:

    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        return GeminiProvider()

    raise LLMProviderError(
        f"Unsupported LLM provider: {provider}"
    )