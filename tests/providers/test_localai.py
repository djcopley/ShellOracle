import pytest

from shelloracle.providers.localai import LocalAI


class TestOpenAI:
    @pytest.fixture
    def localai_config(self, set_config):
        config = {
            "shelloracle": {"provider": "LocalAI"},
            "provider": {"LocalAI": {"host": "localhost", "port": 8080, "model": "mistral-openorca"}},
        }
        set_config(config)

    @pytest.fixture
    def localai_instance(self, localai_config):
        return LocalAI()

    def test_name(self):
        assert LocalAI.name == "LocalAI"

    def test_model(self, localai_instance):
        assert localai_instance.model == "mistral-openorca"

    @pytest.mark.asyncio
    async def test_generate(self, mock_asyncopenai, localai_instance):
        result = ""
        async for response in localai_instance.generate(""):
            result += response
        assert result == "head -c 100 /dev/urandom | hexdump -C"
