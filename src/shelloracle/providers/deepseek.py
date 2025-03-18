from __future__ import annotations

from typing import TYPE_CHECKING

from openai import APIError, AsyncOpenAI

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class Deepseek(Provider):
    name = "Deepseek"

    api_key = Setting(default="")
    model = Setting(default="deepseek-chat")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        self.client = AsyncOpenAI(base_url="https://api.deepseek.com/v1", api_key=self.api_key)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except APIError as e:
            msg = f"Something went wrong while querying Deepseek: {e}"
            raise ProviderError(msg) from e
