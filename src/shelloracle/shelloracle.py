from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from yaspin import yaspin

from .config import get_config
from .providers import get_provider

logger = logging.getLogger(__name__)


async def prompt_user(default_prompt: str | None = None) -> str:
    # stdin doesn't exist when running as a zle widget
    with create_app_session_from_tty(), patch_stdout():
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
        raise ValueError("Multi-line input is not supported")
    logger.debug("using query from stdin: %s", lines)
    return lines[0].rstrip()


async def shelloracle() -> None:
    """ShellOracle program entrypoint

    If there is a query from the input pipe, it processes the query to generate a response.
    If there isn't a query from the input pipe, it prompts the user for input.

    Environment variables:
        - SHOR_DEFAULT_PROMPT: This is the initial user prompt that can be configured via this environment variable.

    :returns: None
    :raises KeyboardInterrupt: if the user presses CTRL+C
    """
    config = get_config()
    provider = get_provider(config.provider)()

    if not (prompt := get_query_from_pipe()):
        default_prompt = os.environ.get("SHOR_DEFAULT_PROMPT")
        prompt = await prompt_user(default_prompt)
    logger.info("user prompt: %s", prompt)

    shell_command = ""
    with create_app_session_from_tty(), patch_stdout(raw=True), yaspin() as sp:
        async for token in provider.generate(prompt):
            # some models may erroneously return a newline, which causes issues with the status spinner
            token = token.replace("\n", "")
            shell_command += token
            sp.text = shell_command
    logger.info("generated shell command: %s", shell_command)
    sys.stdout.write(shell_command)


def cli() -> None:
    """Run the ShellOracle command line interface

    :returns: None
    """
    try:
        asyncio.run(shelloracle())
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        return
    except Exception as err:
        logger.exception("An unhandled exception occurred")
        with create_app_session_from_tty():
            print_formatted_text(FormattedText([("ansired", f"\n{err}")]))
