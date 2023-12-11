import asyncio
import os
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.application import create_app_session_from_tty

from .provider import get_provider

ollama = get_provider("ollama")()


class ShitPluginException(Exception):
    ...


async def prompt_user(default_prompt: str | None) -> None:
    """
    Coroutine function to prompt the user for input, optionally preloading with a default value.

    :param default_prompt: The default text to preload into the prompt
    :return: None
    """
    with create_app_session_from_tty():
        prompt_session = PromptSession()
        prompt_session.output.write_raw("\033[E")  # Can I do this with one of the builtin methods
        query = await prompt_session.prompt_async("> ", default=default_prompt or "")
        async for item in ollama.generate(query):
            sys.stdout.write(item)


async def generate_response(query: str) -> None:
    """Generate a shell command based on the query.

    :param query: The query to generate a shell command for
    :return: None
    """
    try:
        ...
    except Exception as e:
        raise ShitPluginException("Uh oh! Shit plugin alert. The LLM plugin you are using shit the bed.") from e


def get_query_from_pipe() -> str | None:
    """Get a query from stdin pipe.

    :raises ValueError: If the input is more than one line
    :return: The query from the stdin pipe
    """
    if os.isatty(0):  # Return 'None' if nothing is in the pipe
        return None
    if not (lines := sys.stdin.readlines()):
        return None
    if len(lines) > 1:
        raise ValueError("Multi-line input not supported")
    return lines[0].rstrip()


async def shell_oracle() -> None:
    """
    This is the core function of the application.

    It accepts queries either through a standard input pipe or an interactive prompt.
    If there is a query from the input pipe, it processes the query to generate a response.
    If there isn't a query from the input pipe, it prompts the user for input.

    Environment variables:
        - SHOR_DEFAULT_PROMPT: This is the initial user prompt that can be configured via this environment variable.

    :returns: None
    """
    if query := get_query_from_pipe():
        await generate_response(query)
        return

    default_prompt = os.environ.get("SHOR_DEFAULT_PROMPT")
    await prompt_user(default_prompt)


def cli() -> None:
    """
    Run shell oracle.

    Handles KeyboardInterrupt and EOFError.
    """
    try:
        asyncio.run(shell_oracle())
    except (EOFError, KeyboardInterrupt):
        exit(0)
