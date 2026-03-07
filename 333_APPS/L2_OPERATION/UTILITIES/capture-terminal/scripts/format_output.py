from __future__ import annotations

import argparse


def _format_box(text: str) -> str:
    lines = text.splitlines() or [""]
    width = max(len(line) for line in lines)
    inner = width + 2
    out = [f"┌{'─' * inner}┐"]
    for line in lines:
        out.append(f"│ {line.ljust(width)} │")
    out.append(f"└{'─' * inner}┘")
    return "\n".join(out) + "\n"


def _format_minimal(text: str, line_numbers: bool) -> str:
    lines = text.splitlines() or [""]
    if line_numbers:
        return "\n".join(f"{i} | {line}" for i, line in enumerate(lines, start=1)) + "\n"
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=["box", "minimal"], required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--line-numbers", action="store_true")
    args = parser.parse_args()

    if args.style == "box":
        print(_format_box(args.text), end="")
        return
    print(_format_minimal(args.text, args.line_numbers), end="")


if __name__ == "__main__":
    main()
