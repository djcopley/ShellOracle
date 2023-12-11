import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass

import httpx

from . import Provider

host = "localhost"
port = 11434
endpoint = f"http://{host}:{port}/api/generate"

model = "codellama:13b"
system_prompt = """Based on the following user description, generate a corresponding Bash command. Focus solely on 
interpreting the requirements and translating them into a single, executable Bash command. Ensure accuracy and 
relevance to the user's description. The output should be a valid Bash command that directly aligns with the user's 
intent, ready for execution in a command-line environment. Output nothing except for the command. No code block, no 
English explanation, no start/end tags."""


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

    def to_json(self):
        request = {key: value for key, value in self.__dict__.items() if value is not None}
        return json.dumps(request)


class Ollama(Provider):

    async def generate(self, prompt: str) -> AsyncGenerator[str, None, None]:
        request = GenerateRequest(model, prompt, system=system_prompt, stream=True).to_json()
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", endpoint, content=request) as stream:
                async for line in stream.aiter_lines():
                    yield json.loads(line)["response"]


if __name__ == '__main__':
    ollama = Ollama()
