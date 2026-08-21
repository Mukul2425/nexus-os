from unittest.mock import patch

import pytest

from app.services.llm.factory import create_llm_provider
from app.services.llm.gemini import GeminiProvider
from app.core.exceptions import LLMProviderError


def test_factory_returns_gemini_provider():

    with patch(
        "app.services.llm.factory.settings.LLM_PROVIDER",
        "gemini",
    ):

        provider = create_llm_provider()

    assert isinstance(
        provider,
        GeminiProvider,
    )


def test_factory_rejects_unknown_provider():

    with patch(
        "app.services.llm.factory.settings.LLM_PROVIDER",
        "unknown",
    ):

        with pytest.raises(LLMProviderError):

            create_llm_provider()