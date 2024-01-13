from shelloracle.providers.ollama import Ollama


def test_name():
    assert Ollama.name == "Ollama"
