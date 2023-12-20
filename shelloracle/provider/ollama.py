import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass, asdict
from typing import Any

import httpx

from . import Provider, ProviderError
from ..config import Setting


def dataclass_to_json(obj: Any) -> dict[str, Any]:
    """Convert dataclass to a json dict

    This function filters out 'None' values.

    :param obj: the dataclass to serialize
    :return: serialized dataclass
    :raises TypeError: if obj is not a dataclass
    """
    return {k: v for k, v in asdict(obj).items() if v is not None}


@dataclass
class GenerateRequest:
    model: str
    """(required) the model name"""
    prompt: str | None = None
    """the prompt to generate a response for"""
    images: list[str] | None = None
    """a list of base64-encoded images (for multimodal models such as llava)"""
    format: str | None = None
    """the format to return a response in. Currently the only accepted value is json"""
    options: dict | None = None
    """additional model parameters listed in the documentation for the Modelfile such as temperature"""
    system: str | None = None
    """system prompt to (overrides what is defined in the Modelfile)"""
    template: str | None = None
    """the full prompt or prompt template (overrides what is defined in the Modelfile)"""
    context: str | None = None
    """the context parameter returned from a previous request to /generate, this can be used to keep a short 
    conversational memory"""
    stream: bool | None = None
    """if false the response will be returned as a single response object, rather than a stream of objects"""
    raw: bool | None = None
    """if true no formatting will be applied to the prompt and no context will be returned. You may choose to use 
    the raw parameter if you are specifying a full templated prompt in your request to the API, and are managing 
    history yourself. JSON mode"""


class Ollama(Provider):
    name = "Ollama"

    host = Setting(default="localhost")
    port = Setting(default=11434)
    model = Setting(default="codellama:13b")
    system_prompt = Setting(
        default=(
            "Based on the following user description, generate a corresponding Bash command. Focus solely "
            "on interpreting the requirements and translating them into a single, executable Bash command. "
            "Ensure accuracy and relevance to the user's description. The output should be a valid Bash "
            "command that directly aligns with the user's intent, ready for execution in a command-line "
            "environment. Output nothing except for the command. No code block, no English explanation, "
            "no start/end tags."
        )
    )

    @property
    def endpoint(self):
        # computed property because python descriptors need to be bound to an instance before access
        return f"http://{self.host}:{self.port}/api/generate"

    async def generate(self, prompt: str) -> AsyncGenerator[str, None, None]:
        request = GenerateRequest(self.model, prompt, system=self.system_prompt, stream=True)
        data = dataclass_to_json(request)
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", self.endpoint, json=data, timeout=20.0) as stream:
                    async for line in stream.aiter_lines():
                        yield json.loads(line)["response"]
        except (httpx.HTTPError, httpx.StreamError) as e:
            raise ProviderError(f"Something went wrong while querying Ollama: {e}") from e
