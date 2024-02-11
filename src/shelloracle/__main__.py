import argparse
from importlib.metadata import version

from . import shelloracle


def configure():
    # nest this import in a function to avoid expensive module loads
    from .configure import configure_shelloracle
    configure_shelloracle()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'{__package__} {version(__package__)}')

    subparsers = parser.add_subparsers()
    configure_subparser = subparsers.add_parser("configure", help=f"install {__package__} keybindings")
    configure_subparser.set_defaults(action=configure)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if action := getattr(args, "action", None):
        action()
        exit(0)

    shelloracle.cli()


if __name__ == "__main__":
    main()
