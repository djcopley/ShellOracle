from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol


class ProviderError(Exception):
    """LLM providers raise this error to gracefully indicate something has gone wrong."""


class Provider(Protocol):
    """
    LLM Provider Protocol

    All LLM backends must implement this interface.
    """
    name: str

    @abstractmethod
    async def generate(self, prompt: str) -> AsyncIterator[str]:
        """
        This is an asynchronous generator method which defines the protocol that a provider implementation
        should adhere to. The method takes a prompt as an argument and produces an asynchronous stream
        of string results.

        :param prompt: A string value which serves as input to the provider's process of generating results.
        :return: An asynchronous generator yielding string results.
        """


def get_provider(name: str) -> type[Provider]:
    """Imports and loads a requested provider

    :param name: the provider name
    :return: the requested provider
    """
    from .providers import Ollama
    providers = {
        Ollama.name: Ollama,
    }
    return providers[name]
