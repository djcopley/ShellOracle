import pytest
from pytest_httpx import IteratorStream

from shelloracle.providers.ollama import Ollama


class TestOllama:
    @pytest.fixture
    def ollama_config(self, set_config):
        config = {
            "shelloracle": {"provider": "Ollama"},
            "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
        }
        set_config(config)

    @pytest.fixture
    def ollama_instance(self, ollama_config):
        return Ollama()

    def test_name(self):
        assert Ollama.name == "Ollama"

    def test_host(self, ollama_instance):
        assert ollama_instance.host == "localhost"

    def test_port(self, ollama_instance):
        assert ollama_instance.port == 11434

    def test_model(self, ollama_instance):
        assert ollama_instance.model == "dolphin-mistral"

    def test_endpoint(self, ollama_instance):
        assert ollama_instance.endpoint == "http://localhost:11434/api/generate"

    @pytest.mark.asyncio
    async def test_generate(self, ollama_instance, httpx_mock):
        responses = [
            b'{"response": "cat"}\n',
            b'{"response": " test"}\n',
            b'{"response": "."}\n',
            b'{"response": "py"}\n',
            b'{"response": ""}\n',
        ]
        httpx_mock.add_response(stream=IteratorStream(responses))
        result = ""
        async for response in ollama_instance.generate(""):
            result += response
        assert result == "cat test.py"
