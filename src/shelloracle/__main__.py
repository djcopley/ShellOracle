import argparse
from importlib.metadata import version

from . import shelloracle
from .bootstrap import bootstrap


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="install %(prog)s keybindings", action="store_true")
    parser.add_argument('--version', action='version', version=f'%(prog)s {version(__package__)}')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.init:
        bootstrap()
        exit(0)

    shelloracle.cli()


if __name__ == "__main__":
    main()
