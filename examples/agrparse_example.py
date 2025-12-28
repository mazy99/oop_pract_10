#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import ArgumentParser, Namespace


def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("square", type=int, help="Display the square of a given number")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Increase output verbosity"
    )

    args: Namespace = parser.parse_args()
    result: int = args.square**2
    if args.verbose:
        print(f"The square of {args.square} is {result}")
    else:
        print(result)


if __name__ == "__main__":
    main()
