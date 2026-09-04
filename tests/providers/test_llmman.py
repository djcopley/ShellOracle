import pytest
from pytest_httpx import IteratorStream

from shelloracle.config import Configuration
from shelloracle.providers.llmman import Llmman


class TestLlmman:
    @pytest.fixture
    def llmman_config(self):
        config = {
            "shelloracle": {"provider": "llmman"},
            "provider": {"llmman": {"host": "localhost", "port": 17434, "model": "gemma4"}},
        }
        return Configuration(config)

    @pytest.fixture
    def llmman_instance(self, llmman_config):
        return Llmman(llmman_config)

    def test_name(self):
        assert Llmman.name == "llmman"

    def test_host(self, llmman_instance):
        assert llmman_instance.host == "localhost"

    def test_port(self, llmman_instance):
        assert llmman_instance.port == 17434

    def test_model(self, llmman_instance):
        assert llmman_instance.model == "gemma4"

    def test_endpoint(self, llmman_instance):
        assert llmman_instance.endpoint == "http://localhost:17434/api/generate"

    def test_defaults(self):
        instance = Llmman(Configuration({"shelloracle": {"provider": "llmman"}, "provider": {}}))
        assert instance.endpoint == "http://localhost:17434/api/generate"
        assert instance.model == "gemma4"

    @pytest.mark.asyncio
    async def test_generate(self, llmman_instance, httpx_mock):
        responses = [
            b'{"response": "cat"}\n',
            b'{"response": " test"}\n',
            b'{"response": "."}\n',
            b'{"response": "py"}\n',
            b'{"response": ""}\n',
        ]
        httpx_mock.add_response(stream=IteratorStream(responses))
        result = ""
        async for response in llmman_instance.generate(""):
            result += response
        assert result == "cat test.py"
