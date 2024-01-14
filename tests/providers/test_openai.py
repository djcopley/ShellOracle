from shelloracle.providers.openai import OpenAI


def test_name():
    assert OpenAI.name == "OpenAI"
