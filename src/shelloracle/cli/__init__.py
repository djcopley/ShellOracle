from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

import click

from shelloracle import shelloracle
from shelloracle.cli.application import Application
from shelloracle.cli.config import config
from shelloracle.config import Configuration
from shelloracle.tty_log_handler import TtyLogHandler

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def configure_logging(log_path: Path):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    tty_formatter = logging.Formatter("%(message)s")
    tty_handler = TtyLogHandler()
    tty_handler.setLevel(logging.WARNING)
    tty_handler.setFormatter(tty_formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(tty_handler)


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    """ShellOracle command line interface."""
    app = Application()
    configure_logging(app.log_path)
    ctx.obj = app

    if ctx.invoked_subcommand is not None:
        # If no subcommand is invoked, run the main CLI
        return

    try:
        app.configuration = Configuration.from_file(app.config_path)
    except FileNotFoundError:
        logger.warning("Configuration not found. Run `shor config init` to initialize.")
        sys.exit(1)

    shelloracle.cli(app)


cli.add_command(config)


def main():
    cli()
