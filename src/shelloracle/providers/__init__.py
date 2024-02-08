from __future__ import annotations

from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol, TypeVar, Generic, runtime_checkable

from ..config import get_config

system_prompt = (
    "Based on the following user description, generate a corresponding Bash command. Focus solely "
    "on interpreting the requirements and translating them into a single, executable Bash command. "
    "Ensure accuracy and relevance to the user's description. The output should be a valid Bash "
    "command that directly aligns with the user's intent, ready for execution in a command-line "
    "environment. Output nothing except for the command. No code block, no English explanation, "
    "no start/end tags."
)


class ProviderError(Exception):
    """LLM providers raise this error to gracefully indicate something has gone wrong."""


@runtime_checkable
class Provider(Protocol):
    """
    LLM Provider Protocol

    All LLM backends must implement this interface.
    """
    name: str

    @abstractmethod
    def generate(self, prompt: str) -> AsyncIterator[str]:
        """
        This is an asynchronous generator method which defines the protocol that a provider implementation
        should adhere to. The method takes a prompt as an argument and produces an asynchronous stream
        of string results.

        :param prompt: A string value which serves as input to the provider's process of generating results.
        :return: An asynchronous generator yielding string results.
        """
        # If you are wondering why the 'generate' signature doesn't include 'async', see
        # https://mypy.readthedocs.io/en/stable/more_types.html#asynchronous-iterators


T = TypeVar("T")


class Setting(Generic[T]):
    def __init__(self, *, name: str | None = None, default: T | None = None) -> None:
        self.name = name
        self.default = default

    def __set_name__(self, owner: type[Provider], name: str) -> None:
        if not self.name:
            self.name = name

    def __get__(self, instance: Provider, owner: type[Provider]) -> T:
        if instance is None:
            # Accessing settings as a class attribute is not supported because it prevents
            # inspect.get_members from determining the object type
            raise AttributeError("Settings must be accessed through a provider instance.")
        config = get_config()
        return config["provider"][owner.name][self.name]


def _providers() -> dict[str, type[Provider]]:
    from .ollama import Ollama
    from .openai import OpenAI
    from .localai import LocalAI
    providers = {
        Ollama.name: Ollama,
        OpenAI.name: OpenAI,
        LocalAI.name: LocalAI
    }
    return providers


def get_provider(name: str) -> type[Provider]:
    """Imports and loads a requested provider

    :param name: the provider name
    :return: the requested provider
    """

    return _providers()[name]


def list_providers() -> list[str]:
    return list(_providers())
