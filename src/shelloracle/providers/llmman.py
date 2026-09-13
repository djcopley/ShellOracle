from __future__ import annotations

from shelloracle.providers import Setting
from shelloracle.providers.ollama import Ollama


class Llmman(Ollama):
    """llmman (https://github.com/llmmanorg/llmman) serves the Ollama API on port 17434."""

    name = "llmman"

    port = Setting(default=17434)
    model = Setting(default="gemma4")
