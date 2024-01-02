from collections.abc import AsyncIterator

from openai import APIError
from openai import AsyncOpenAI as OpenAIClient

from ..config import Setting
from ..provider import Provider, ProviderError


class OpenAI(Provider):
    name = "OpenAI"

    api_key = Setting(default="")
    model = Setting(default="gpt-3.5-turbo")
    system_prompt = Setting(
        default=(
            "Based on the following user description, generate a corresponding Bash command. Focus solely "
            "on interpreting the requirements and translating them into a single, executable Bash command. "
            "Ensure accuracy and relevance to the user's description. The output should be a valid Bash "
            "command that directly aligns with the user's intent, ready for execution in a command-line "
            "environment. Output nothing except for the command. No code block, no English explanation, "
            "no start/end tags."
        )
    )

    def __init__(self):
        if not self.api_key:
            raise ProviderError("No API key provided")
        self.client = OpenAIClient(api_key=self.api_key)

    async def generate(self, prompt: str) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except APIError as e:
            raise ProviderError(f"Something went wrong while querying OpenAI: {e}") from e
