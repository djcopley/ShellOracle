import argparse
from importlib.metadata import version

from . import shelloracle
from .bootstrap import bootstrap_shelloracle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'%(prog)s {version(__package__)}')

    subparsers = parser.add_subparsers()
    configure_subparser = subparsers.add_parser("configure", help="install %(prog)s keybindings")
    configure_subparser.set_defaults(subparser=configure_subparser, action=bootstrap_shelloracle)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if action := getattr(args, "action", None):
        action()
        exit(0)

    shelloracle.cli()


if __name__ == "__main__":
    main()
