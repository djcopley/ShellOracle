from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.history import FileHistory

from .config import config
from .provider import get_provider


async def prompt_user(default_prompt: str | None = None) -> str:
    with create_app_session_from_tty():
        history_file = Path.home() / ".shelloracle_history"
        prompt_session: PromptSession = PromptSession(history=FileHistory(str(history_file)))
        # Can I do this with one of the builtin methods?
        # I tried a few (including cursor_down) with limited success
        prompt_session.output.write_raw("\033[E")
        return await prompt_session.prompt_async("> ", default=default_prompt or "")


def get_query_from_pipe() -> str | None:
    """Get a query from stdin pipe.

    :raises ValueError: If the input is more than one line
    :return: The query from the stdin pipe
    """
    if os.isatty(0) or not (lines := sys.stdin.readlines()):  # Return 'None' if fd 0 is a tty (no pipe)
        return None
    if len(lines) > 1:
        raise ValueError("Multi-line input not supported")
    return lines[0].rstrip()


async def shell_oracle() -> None:
    """
    If there is a query from the input pipe, it processes the query to generate a response.
    If there isn't a query from the input pipe, it prompts the user for input.

    Environment variables:
        - SHOR_DEFAULT_PROMPT: This is the initial user prompt that can be configured via this environment variable.

    :returns: None
    """
    provider = get_provider(config.global_config.provider)()

    if not (prompt := get_query_from_pipe()):
        default_prompt = os.environ.get("SHOR_DEFAULT_PROMPT")
        prompt = await prompt_user(default_prompt)

    async for token in provider.generate(prompt):
        sys.stdout.write(token)


def cli() -> None:
    """
    Run shell oracle.

    Handles KeyboardInterrupt and EOFError.
    """
    try:
        asyncio.run(shell_oracle())
    except (EOFError, KeyboardInterrupt):
        exit(0)
