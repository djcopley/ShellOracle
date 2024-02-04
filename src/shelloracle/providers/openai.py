from collections.abc import AsyncIterator

from openai import APIError
from openai import AsyncOpenAI as OpenAIClient

from . import Provider, ProviderError, Setting, system_prompt


class OpenAI(Provider):
    name = "OpenAI"

    api_key = Setting(default="")
    model = Setting(default="gpt-3.5-turbo")

    def __init__(self):
        if not self.api_key:
            raise ProviderError("No API key provided")
        self.client = OpenAIClient(api_key=self.api_key)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except APIError as e:
            raise ProviderError(f"Something went wrong while querying OpenAI: {e}") from e
