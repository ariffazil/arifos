from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone


def _pick_route(prompt: str, config: dict) -> tuple[str, str]:
    text = prompt.lower()
    for route in config.get("routes", []):
        keywords = route.get("keywords", [])
        if any(str(keyword).lower() in text for keyword in keywords):
            return str(route.get("task_type", "unknown_default")), str(
                route.get("primary", config["default_model"])
            )
    return "unknown_default", str(config["default_model"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as handle:
        config = json.load(handle)

    task, model = _pick_route(args.prompt, config)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{now}] TASK: {task} | MODEL: {model}")


if __name__ == "__main__":
    main()
