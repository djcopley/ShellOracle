import pytest

from shelloracle.config import Configuration
from shelloracle.providers.deepseek import Deepseek


class TestOpenAI:
    @pytest.fixture
    def deepseek_config(self):
        config = {
            "shelloracle": {"provider": "Deepseek"},
            "provider": {
                "Deepseek": {
                    "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "model": "grok-beta",
                }
            },
        }
        return Configuration(config)

    @pytest.fixture
    def deepseek_instance(self, deepseek_config):
        return Deepseek(deepseek_config)

    def test_name(self):
        assert Deepseek.name == "Deepseek"

    def test_api_key(self, deepseek_instance):
        assert (
            deepseek_instance.api_key
            == "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )

    def test_model(self, deepseek_instance):
        assert deepseek_instance.model == "grok-beta"

    @pytest.mark.asyncio
    async def test_generate(self, mock_asyncopenai, deepseek_instance):
        result = ""
        async for response in deepseek_instance.generate(""):
            result += response
        assert result == "head -c 100 /dev/urandom | hexdump -C"
