from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _contract_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "CONTRACT"


def load_runtime_env(profile: str = "dev") -> dict[str, Any]:
    file_name = "env.prod.json" if profile == "prod" else "env.dev.json"
    return json.loads((_contract_dir() / file_name).read_text(encoding="utf-8"))


def load_role_profiles() -> dict[str, dict[str, Any]]:
    return json.loads(
        (_contract_dir() / "role_profiles.json").read_text(encoding="utf-8")
    )["roles"]
