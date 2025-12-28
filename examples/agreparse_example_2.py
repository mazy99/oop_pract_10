#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from argparse import ArgumentParser, Namespace, _SubParsersAction


def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser()
    subparsers: _SubParsersAction = parser.add_subparsers(help="List of commands")

    list_parser: ArgumentParser = subparsers.add_parser("list", help="List contents")
    list_parser.add_argument("dirname", action="store", help="Directory to list")

    create_parser: ArgumentParser = subparsers.add_parser(
        "create", help="Create a directory"
    )
    create_parser.add_argument(
        "dirname", action="store", help="New directory to create"
    )
    create_parser.add_argument(
        "--read-only",
        default=False,
        action="store_true",
        help="Set permissions to prevent writing to the directory",
    )

    args: Namespace = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
