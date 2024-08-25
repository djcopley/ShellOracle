import argparse
import logging
import sys
from importlib.metadata import version

from shelloracle import shelloracle
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


def configure():
    # nest this import in a function to avoid expensive module loads
    from shelloracle.bootstrap import bootstrap_shelloracle

    bootstrap_shelloracle()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"{__package__} {version(__package__)}")

    subparsers = parser.add_subparsers()
    configure_subparser = subparsers.add_parser("configure", help=f"install {__package__} keybindings")
    configure_subparser.set_defaults(action=configure)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging()

    if action := getattr(args, "action", None):
        action()
        sys.exit(0)

    try:
        initialize_config()
    except FileNotFoundError:
        logger.warning("ShellOracle configuration not found. Run `shor configure` to initialize.")
        sys.exit(1)

    shelloracle.cli()


if __name__ == "__main__":
    main()
