import argparse

from doku.core import run_puzzle


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="fuzzy",
        description="Makes images fuzzy.",
    )
    parser.add_argument("image", help="path to the image to blur")
    parser.add_argument(
        "-r",
        "--radius",
        type=float,
        default=2.0,
        help="blur radius (default: 2.0)",
    )
    args = parser.parse_args(argv)
    run_puzzle(args.image, radius=args.radius)
