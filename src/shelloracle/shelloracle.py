from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from prompt_toolkit import PromptSession
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from yaspin import yaspin
from yaspin.spinners import Spinners

from shelloracle.config import get_config
from shelloracle.providers import get_provider

if TYPE_CHECKING:
    from yaspin.core import Yaspin

logger = logging.getLogger(__name__)


async def prompt_user(default_prompt: str | None = None) -> str:
    # stdin doesn't exist when running as a zle widget
    with create_app_session_from_tty(), patch_stdout():
        history_file = Path.home() / ".shelloracle_history"
        prompt_session: PromptSession = PromptSession(history=FileHistory(str(history_file)))
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
        msg = "Multi-line input is not supported"
        raise ValueError(msg)
    logger.debug("using query from stdin: %s", lines)
    return lines[0].rstrip()


def spinner() -> Yaspin:
    """Get the correct spinner based on the user's configuration

    :returns: yaspin object
    """
    config = get_config()
    if not config.spinner_style:
        return yaspin()
    style = getattr(Spinners, config.spinner_style)
    return yaspin(style)


async def shelloracle() -> None:
    """ShellOracle program entrypoint

    If there is a query from the input pipe, it processes the query to generate a response.
    If there isn't a query from the input pipe, it prompts the user for input.

    Environment variables:
        - SHOR_DEFAULT_PROMPT: This is the initial user prompt that can be configured via this environment variable.

    :returns: None
    :raises KeyboardInterrupt: if the user presses CTRL+C
    """
    if not (prompt := get_query_from_pipe()):
        default_prompt = os.environ.get("SHOR_DEFAULT_PROMPT")
        prompt = await prompt_user(default_prompt)
    logger.info("user prompt: %s", prompt)

    config = get_config()
    provider = get_provider(config.provider)()

    shell_command = ""
    with create_app_session_from_tty(), patch_stdout(raw=True), spinner() as sp:
        async for token in provider.generate(prompt):
            # some models may erroneously return a newline, which causes issues with the status spinner
            shell_command += token.replace("\n", "")
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
    except Exception:
        logger.exception("An error occurred")
