from __future__ import annotations

from typing import TYPE_CHECKING

from google import genai

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class Google(Provider):
    name = "Google"

    api_key = Setting(default="")
    model = Setting(default="gemini-2.5-flash-lite")  # Assuming a default model name

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        self.client = genai.Client(api_key=self.api_key)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=genai.GenerateContentConfig(system_instruction=system_prompt),
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            msg = f"Something went wrong while querying Google Gemini: {e}"
            raise ProviderError(msg) from e
