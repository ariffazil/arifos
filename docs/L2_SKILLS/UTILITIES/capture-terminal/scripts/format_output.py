#!/usr/bin/env python3
"""Format terminal output for clean copy-paste.

Usage:
  python format_output.py --style box --text "line1\nline2"
  cat output.txt | python format_output.py --style block
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BOX = {
    "top": "┌",
    "bottom": "└",
    "h": "─",
    "v": "│",
}
BLOCK = {
    "top": "═",
    "bottom": "═",
}


def read_input(text: str | None, file_path: str | None) -> str:
    if text is not None:
        return text
    if file_path is not None:
        return Path(file_path).read_text(encoding="utf-8")
    return sys.stdin.read()


def with_line_numbers(lines: list[str]) -> list[str]:
    width = len(str(len(lines)))
    return [f"{str(i + 1).rjust(width)} | {line}" for i, line in enumerate(lines)]


def format_box(lines: list[str]) -> str:
    width = max((len(line) for line in lines), default=0)
    top = BOX["top"] + (BOX["h"] * (width + 2)) + "┐"
    bottom = BOX["bottom"] + (BOX["h"] * (width + 2)) + "┘"
    body = "\n".join(f"{BOX['v']} {line.ljust(width)} {BOX['v']}" for line in lines)
    return "\n".join([top, body, bottom])


def format_block(lines: list[str]) -> str:
    width = max((len(line) for line in lines), default=0)
    border = BLOCK["top"] * (width + 2)
    body = "\n".join(f" {line.ljust(width)}" for line in lines)
    return "\n".join([border, body, border])


def format_minimal(lines: list[str]) -> str:
    return "\n".join(lines)


def format_code(lines: list[str]) -> str:
    return "\n".join(["```", *lines, "```"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Format terminal output")
    parser.add_argument("--style", choices=["box", "block", "minimal", "code"], default="box")
    parser.add_argument("--text", help="Inline text to format")
    parser.add_argument("--file", help="Read text from a file path")
    parser.add_argument("--line-numbers", action="store_true", help="Add line numbers")
    args = parser.parse_args()

    raw = read_input(args.text, args.file)
    lines = raw.rstrip("\n").split("\n") if raw else []

    if args.line_numbers:
        lines = with_line_numbers(lines)

    if args.style == "box":
        out = format_box(lines)
    elif args.style == "block":
        out = format_block(lines)
    elif args.style == "code":
        out = format_code(lines)
    else:
        out = format_minimal(lines)

    sys.stdout.write(out)
    if out and not out.endswith("\n"):
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
