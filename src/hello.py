#!/usr/bin/env python3
"""A simple hello world script."""

import argparse


def main():
    parser = argparse.ArgumentParser(description="A simple hello script")
    parser.add_argument("--name", type=str, default="World", help="Name to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()