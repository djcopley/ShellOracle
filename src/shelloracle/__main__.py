import argparse
from importlib.metadata import version

from . import shelloracle
from .bootstrap import bootstrap_shelloracle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'%(prog)s {version(__package__)}')

    subparsers = parser.add_subparsers()
    init_subparser = subparsers.add_parser("init", help="install %(prog)s keybindings")
    init_subparser.set_defaults(subparser=init_subparser, func=bootstrap_shelloracle)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if func := args.func:
        func()
        exit(0)

    shelloracle.cli()


if __name__ == "__main__":
    main()
