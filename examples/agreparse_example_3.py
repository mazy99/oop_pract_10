#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import ArgumentParser, Namespace


def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("square", type=int, help="display the square of a given number")
    parser.add_argument(
        "-v", "--verbosity", action="count", help="increase output verbosity"
    )

    args: Namespace = parser.parse_args()
    answer: int = args.square**2

    if args.verbosity == 2:
        print(f"the square of {args.square} equals {answer}")
    elif args.verbosity == 1:
        print(f"{args.square}*2 = {answer}")
    else:
        print(answer)


if __name__ == "__main__":
    main()
