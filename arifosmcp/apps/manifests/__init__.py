"""
arifosmcp/apps/manifests/__init__.py
Canonical MCP App manifests for the 5 core arifOS governance apps.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

_MANIFEST_DIR = pathlib.Path(__file__).parent


def load_manifest(app_id: str) -> dict[str, Any] | None:
    """Load an app manifest by app_id."""
    path = _MANIFEST_DIR / f"{app_id}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def list_manifests() -> list[str]:
    """List all available manifest app_ids."""
    return sorted([p.stem for p in _MANIFEST_DIR.glob("*.json")])


__all__ = ["load_manifest", "list_manifests"]
