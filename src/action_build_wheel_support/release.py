#!/usr/bin/env python3
"""make a release"""
# /// script
# dependencies = [
# ]
# ///

import argparse
import logging
import re
import subprocess
from argparse import Namespace
from pathlib import Path

log = logging.getLogger(__name__)
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
GREY = "\033[90m"
RESET = "\033[0m"


def indent(txt: str, pre: str, first: str | None = None) -> str:
    return (pre if first is None else first) + txt.replace("\n", "\n" + pre)


def message(title: str, body: str | list[str]) -> str:
    text = body if isinstance(body, str) else "\n".join(str(b) for b in body)
    text = indent(text, "|  ")
    return f"> {YELLOW}{title}{RESET}\n{GREEN}{text}{RESET}"


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--commit", action="store_true")
    group.add_argument("--push", action="store_true")
    parser.add_argument("mode", choices=["major", "minor", "micro"])

    return parser.parse_args()


def raise_if_modified():
    out = [
        line
        for line in subprocess.check_output(["git", "status", "--porcelain"], text=True).split("\n")
        if line.strip()
    ]
    changed = [line for line in out if (not line.startswith("??"))]
    if changed:
        txt = " | " + "\n | ".join(changed)
        raise RuntimeError(f"found modifications:\n{txt}")


def get_pyproject(path: Path) -> tuple[list[tuple[int, str]], dict]:
    lines = []
    data = {}
    for index, line in enumerate(path.read_text().split("\n")):
        lines.append((index, line))
        if re.search(r"^version\s*=", line):
            data["version"] = (index, line.partition("=")[2].strip().replace('"', "").replace("'", ""))
    return lines, data


def bump(version: list[int], mode: str) -> list[int]:
    index = {
        "major": 0,
        "micro": len(version) - 1,
        "minor": 1,
    }[mode]
    result = version[:]
    result[index] += 1
    for i in range(index + 1, len(version)):
        result[i] = 0
    return result


def main(args: Namespace) -> None:
    raise_if_modified()

    # first we get the local version
    pyproject = Path("pyproject.toml")
    lines, data = get_pyproject(pyproject)

    lineno, sversion = data["version"]
    version = [int(v) for v in sversion.split(".")]

    nextversion = bump(version, args.mode)
    snextversion = ".".join(str(v) for v in nextversion)

    print(f"will release '{sversion}', and move onto '{snextversion}'")

    while (ask := input("Ok to proceed? y|N ")) or True:
        if ask.upper() in {"Y", "YES"}:
            break
        elif ask.upper() in {"", "N", "NO"}:
            return

    commit = args.commit or args.push

    def run(arguments: list[str | Path], capture: bool = False) -> str | None:
        cmdline = [str(a) for a in arguments]
        if commit:
            subprocess.check_call(cmdline)
        else:
            print(f"{GREY}dry run:", " ".join(cmdline), RESET)

    # get the current hash
    current = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True)[:7]

    # first tagging the code
    run(["git", "commit", "-m", f"release v{sversion}", "--allow-empty"])
    run(["git", "tag", "-m", "release", f"v{sversion}"])

    newline = lineno, f'version = "{snextversion}"'
    print(
        message(
            f"changing line @ {lineno}",
            [
                lines[lineno][1],
                newline[1],
            ],
        )
    )
    lines[lineno] = newline

    # updating pyproject
    if commit:
        pyproject.write_text("\n".join(line[1] for line in lines))
    run(["git", "commit", "-m", f"release bump {sversion} -> {snextversion}", pyproject])

    # pushing it out
    if args.push:
        run(["git", "push", "origin", f"v{sversion}"])
        run(["git", "push", "origin", "HEAD"])

    if args.commit:
        print(message("To reverse", [f'git tag -d "v{sversion}"', f"git reset --hard {current[:7]}"]))
        print(message("To push", [f"git push origin v{sversion}", "git push origin HEAD"]))


if __name__ == "__main__":
    main(parse_args())
