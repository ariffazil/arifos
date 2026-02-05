#!/usr/bin/env python3
"""Route a task prompt using routing.json and optionally log the decision.

Usage:
  python route_task.py --prompt "fix this bug" [--log]
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ROUTING_PATH = REPO_ROOT / "routing.json"
LEDGER_PATH = REPO_ROOT / "routing_ledger.md"


def load_policy(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def select_route(policy: dict, prompt: str) -> dict:
    prompt_lc = prompt.lower()
    for route in policy.get("routes", []):
        keywords = route.get("keywords", [])
        if any(kw.lower() in prompt_lc for kw in keywords):
            return {
                "task_type": route.get("task_type", "unknown"),
                "model": route.get("primary", policy.get("default_model")),
                "reason": route.get("reason", "keyword match"),
            }

    return {
        "task_type": "unknown_default",
        "model": policy.get("default_model"),
        "reason": "No keyword match; using default_model.",
    }


def format_log_entry(task_type: str, model: str, reason: str) -> str:
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"[{ts}] | TASK: {task_type} | MODEL: {model} | REASON: {reason}"


def append_log(path: Path, entry: str) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a task prompt using routing.json")
    parser.add_argument("--prompt", required=True, help="Task prompt to classify")
    parser.add_argument("--log", action="store_true", help="Append decision to routing_ledger.md")
    args = parser.parse_args()

    policy = load_policy(ROUTING_PATH)
    selection = select_route(policy, args.prompt)

    entry = format_log_entry(selection["task_type"], selection["model"], selection["reason"])
    print(entry)

    if args.log:
        append_log(LEDGER_PATH, entry)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
