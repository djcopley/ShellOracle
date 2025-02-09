import logging
from collections.abc import AsyncIterator

from openai import APIError, AsyncOpenAI

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt


class OpenAICompat(Provider):
    name = "OpenAICompat"

    base_url = Setting(default="")
    api_key = Setting(default="")
    model = Setting(default="")

    def __init__(self):
        if not self.api_key:
            msg = "No API key provided. Use a dummy placeholder if no key is required"
            raise ProviderError(msg)
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                stream=True,
            )
            async for chunk in stream:
                logging.getLogger(__name__).info(chunk)
                try:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
                except:
                    logging.getLogger(__name__).exception("no choices")
        except APIError as e:
            msg = f"Something went wrong while querying OpenAI: {e}"
            raise ProviderError(msg) from e
