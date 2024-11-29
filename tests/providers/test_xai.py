import pytest

from shelloracle.providers.xai import XAI


class TestOpenAI:
    @pytest.fixture
    def xai_config(self, set_config):
        config = {
            "shelloracle": {"provider": "XAI"},
            "provider": {
                "XAI": {
                    "api_key": "xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "model": "grok-beta",
                }
            },
        }
        set_config(config)

    @pytest.fixture
    def xai_instance(self, xai_config):
        return XAI()

    def test_name(self):
        assert XAI.name == "XAI"

    def test_api_key(self, xai_instance):
        assert (
            xai_instance.api_key
            == "xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )

    def test_model(self, xai_instance):
        assert xai_instance.model == "grok-beta"

    @pytest.mark.asyncio
    async def test_generate(self, mock_asyncopenai, xai_instance):
        result = ""
        async for response in xai_instance.generate(""):
            result += response
        assert result == "head -c 100 /dev/urandom | hexdump -C"
