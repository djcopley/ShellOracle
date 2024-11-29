from collections.abc import AsyncIterator

from openai import APIError, AsyncOpenAI

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt


class XAI(Provider):
    name = "XAI"

    api_key = Setting(default="")
    model = Setting(default="grok-beta")

    def __init__(self):
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1",
        )

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
            msg = f"Something went wrong while querying XAI: {e}"
            raise ProviderError(msg) from e
