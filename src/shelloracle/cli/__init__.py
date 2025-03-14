import logging
import sys
from importlib.metadata import version

import click

from shelloracle import shelloracle
from shelloracle.cli.config import config
from shelloracle.config import initialize_config
from shelloracle.settings import Settings
from shelloracle.tty_log_handler import TtyLogHandler

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    file_handler = logging.FileHandler(Settings.shelloracle_home / "shelloracle.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    tty_formatter = logging.Formatter("%(message)s")
    tty_handler = TtyLogHandler()
    tty_handler.setLevel(logging.WARNING)
    tty_handler.setFormatter(tty_formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(tty_handler)


@click.group(invoke_without_command=True)
@click.version_option(version=version("shelloracle"))
@click.pass_context
def cli(ctx):
    """ShellOracle command line interface."""
    configure_logging()

    # If no subcommand is invoked, run the main CLI
    if ctx.invoked_subcommand is None:
        try:
            initialize_config()
        except FileNotFoundError:
            logger.warning("ShellOracle configuration not found. Run `shor config init` to initialize.")
            sys.exit(1)

        shelloracle.cli()


cli.add_command(config)


def main():
    cli()
