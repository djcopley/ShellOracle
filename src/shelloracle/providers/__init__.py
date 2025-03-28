from __future__ import annotations

import abc
from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from shelloracle.config import Configuration

system_prompt = (
    "Based on the following user description, generate a corresponding shell command. Focus solely "
    "on interpreting the requirements and translating them into a single, executable Bash command. "
    "Ensure accuracy and relevance to the user's description. The output should be a valid shell "
    "command that directly aligns with the user's intent, ready for execution in a command-line "
    "environment. Do not output anything except for the command. No code block, no English explanation, "
    "no newlines, and no start/end tags."
)


class ProviderError(Exception):
    """LLM providers raise this error to gracefully indicate something has gone wrong."""


class Provider(abc.ABC):
    """
    LLM Provider Protocol

    All LLM backends must implement this interface.
    """

    name: str
    config: Configuration

    def __init__(self, config: Configuration) -> None:
        """Initialize the provider with the given configuration.

        :param config: the configuration object
        :return: none
        """
        self.config = config

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
            msg = "Settings must be accessed through a provider instance."
            raise AttributeError(msg)
        try:
            return instance.config["provider"][owner.name][self.name]
        except KeyError:
            if self.default is None:
                raise
            return self.default


def _providers() -> dict[str, type[Provider]]:
    from shelloracle.providers.deepseek import Deepseek
    from shelloracle.providers.google import Google
    from shelloracle.providers.localai import LocalAI
    from shelloracle.providers.ollama import Ollama
    from shelloracle.providers.openai import OpenAI
    from shelloracle.providers.openai_compat import OpenAICompat
    from shelloracle.providers.xai import XAI

    return {
        Ollama.name: Ollama,
        OpenAI.name: OpenAI,
        OpenAICompat.name: OpenAICompat,
        LocalAI.name: LocalAI,
        XAI.name: XAI,
        Deepseek.name: Deepseek,
        Google.name: Google,
    }


def get_provider(name: str) -> type[Provider]:
    """Imports and loads a requested provider

    :param name: the provider name
    :return: the requested provider
    """

    return _providers()[name]


def list_providers() -> list[str]:
    return list(_providers())
