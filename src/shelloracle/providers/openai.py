from __future__ import annotations

from typing import TYPE_CHECKING

from openai import APIError, AsyncOpenAI

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class OpenAI(Provider):
    name = "OpenAI"

    api_key = Setting(default="")
    model = Setting(default="gpt-3.5-turbo")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except APIError as e:
            msg = f"Something went wrong while querying OpenAI: {e}"
            raise ProviderError(msg) from e
