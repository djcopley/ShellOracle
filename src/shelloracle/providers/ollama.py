from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

import httpx

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


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
    model = Setting(default="dolphin-mistral")

    @property
    def endpoint(self) -> str:
        # computed property because python descriptors need to be bound to an instance before access
        return f"http://{self.host}:{self.port}/api/generate"

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        request = GenerateRequest(self.model, prompt, system=system_prompt, stream=True)
        data = dataclass_to_json(request)
        try:
            async with (
                httpx.AsyncClient() as client,
                client.stream("POST", self.endpoint, json=data, timeout=20.0) as stream,
            ):
                async for line in stream.aiter_lines():
                    response = json.loads(line)
                    if "error" in response:
                        raise ProviderError(response["error"])
                    yield response["response"]
        except (httpx.HTTPError, httpx.StreamError) as e:
            msg = f"Something went wrong while querying Ollama: {e}"
            raise ProviderError(msg) from e
