import pytest

from shelloracle.providers.openai import OpenAI


class TestOpenAI:
    @pytest.fixture
    def openai_config(self, set_config):
        config = {'shelloracle': {'provider': 'OpenAI'}, 'provider': {
            'OpenAI': {'api_key': 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'model': 'gpt-3.5-turbo'}}}
        return set_config(config)

    @pytest.fixture
    def openai_instance(self, openai_config):
        return OpenAI()

    def test_name(self):
        assert OpenAI.name == "OpenAI"
