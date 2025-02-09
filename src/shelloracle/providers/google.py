from collections.abc import AsyncIterator

import google.generativeai as genai

from shelloracle.providers import Provider, ProviderError, Setting, system_prompt


class Google(Provider):
    name = "Google"

    api_key = Setting(default="")
    model = Setting(default="gemini-pro")  # Assuming a default model name

    def __init__(self):
        if not self.api_key:
            msg = "No API key provided"
            raise ProviderError(msg)
        genai.configure(api_key=self.api_key)
        self.model_instance = genai.GenerativeModel(self.model)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            response = await self.model_instance.generate_content_async(
                [
                    {"role": "user", "parts": [system_prompt]},
                    {"role": "model", "parts": ["Okay."]},  # Gemini requires a model response before user input
                    {"role": "user", "parts": [prompt]},
                ],
                stream=True,
            )

            async for chunk in response:
                yield chunk.text
        except Exception as e:
            msg = f"Something went wrong while querying Google Gemini: {e}"
            raise ProviderError(msg) from e
