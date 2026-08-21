import pytest

from app.services.llm.provider import LLMProvider


def test_llm_provider_is_abstract():

    with pytest.raises(TypeError):

        LLMProvider()