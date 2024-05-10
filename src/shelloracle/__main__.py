import argparse
import logging
from importlib.metadata import version

from shelloracle.config import initialize_config
from . import shelloracle
from .settings import Settings


def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler = logging.FileHandler(Settings.shelloracle_home / "shelloracle.log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)


def configure():
    # nest this import in a function to avoid expensive module loads
    from .bootstrap import bootstrap_shelloracle
    bootstrap_shelloracle()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'{__package__} {version(__package__)}')

    subparsers = parser.add_subparsers()
    configure_subparser = subparsers.add_parser("configure", help=f"install {__package__} keybindings")
    configure_subparser.set_defaults(action=configure)

    return parser.parse_args()


def main() -> None:
    configure_logging()

    args = parse_args()
    if action := getattr(args, "action", None):
        action()
        exit(0)
    initialize_config()

    shelloracle.cli()


if __name__ == "__main__":
    main()
