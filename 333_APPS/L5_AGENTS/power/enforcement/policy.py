"""Runtime ENV contract loader for POWER plane."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_runtime_env(profile: str = "dev") -> dict[str, Any]:
    contract_dir = Path(__file__).resolve().parents[2] / "SPEC" / "CONTRACT"
    file_name = "env.prod.json" if profile == "prod" else "env.dev.json"
    return json.loads((contract_dir / file_name).read_text(encoding="utf-8"))
