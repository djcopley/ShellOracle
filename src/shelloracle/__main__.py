import argparse

from . import shelloracle
from .bootstrap import bootstrap


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="initialize shelloracle with scripts",
                        action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.init:
        bootstrap()
        exit(0)

    shelloracle.cli()


if __name__ == "__main__":
    main()
