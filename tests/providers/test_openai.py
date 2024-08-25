import pytest

from shelloracle.providers.openai import OpenAI


class TestOpenAI:
    @pytest.fixture
    def openai_config(self, set_config):
        config = {
            "shelloracle": {"provider": "OpenAI"},
            "provider": {
                "OpenAI": {"api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "model": "gpt-3.5-turbo"}
            },
        }
        set_config(config)

    @pytest.fixture
    def openai_instance(self, openai_config):
        return OpenAI()

    def test_name(self):
        assert OpenAI.name == "OpenAI"

    def test_api_key(self, openai_instance):
        assert openai_instance.api_key == "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    def test_model(self, openai_instance):
        assert openai_instance.model == "gpt-3.5-turbo"

    @pytest.mark.asyncio
    async def test_generate(self, mock_asyncopenai, openai_instance):
        result = ""
        async for response in openai_instance.generate(""):
            result += response
        assert result == "head -c 100 /dev/urandom | hexdump -C"
