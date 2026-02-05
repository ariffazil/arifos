import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTE_SCRIPT = REPO_ROOT / "skills" / "route-tasks-by-policy" / "scripts" / "route_task.py"
ROUTING_JSON = REPO_ROOT / "routing.json"


def run_route(prompt: str) -> str:
    result = subprocess.check_output(
        [sys.executable, str(ROUTE_SCRIPT), "--prompt", prompt],
        text=True,
    )
    return result.strip()


def test_route_matches_keyword() -> None:
    policy = json.loads(ROUTING_JSON.read_text(encoding="utf-8"))
    expected_model = None
    for route in policy["routes"]:
        if route.get("task_type") == "constitutional_audit":
            expected_model = route.get("primary")
            break

    assert expected_model is not None

    output = run_route("please audit and verify floors")
    assert "TASK: constitutional_audit" in output
    assert f"MODEL: {expected_model}" in output


def test_route_default_model() -> None:
    policy = json.loads(ROUTING_JSON.read_text(encoding="utf-8"))
    default_model = policy["default_model"]

    output = run_route("this prompt has no keywords")
    assert "TASK: unknown_default" in output
    assert f"MODEL: {default_model}" in output
    assert re.search(r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\]", output)
