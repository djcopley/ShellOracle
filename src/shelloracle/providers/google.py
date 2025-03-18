from __future__ import annotations

from typing import TYPE_CHECKING

import google.generativeai as genai

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class Google(Provider):
    name = "Google"

    api_key = Setting(default="")
    model = Setting(default="gemini-2.0-flash")  # Assuming a default model name

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        genai.configure(api_key=self.api_key)
        self.model_instance = genai.GenerativeModel(self.model, system_instruction=system_prompt)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            response = await self.model_instance.generate_content_async(
                [prompt],
                stream=True,
            )

            async for chunk in response:
                yield chunk.text
        except Exception as e:
            msg = f"Something went wrong while querying Google Gemini: {e}"
            raise ProviderError(msg) from e
