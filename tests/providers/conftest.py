import textwrap

import pytest


@pytest.fixture
def ollama_config(set_config):
    config = textwrap.dedent("""\
    [shelloracle]
    provider = "Ollama"
    
    [provider.Ollama]
    host = "localhost"
    port = 11434
    model = "dolphin-mistral"
    """)
    set_config(config)
