"""Build information for arifOS AAA MCP."""

from __future__ import annotations

from typing import Any

from .public_registry import release_version_label


def get_build_info() -> dict[str, Any]:
    """Return version and environment metadata."""
    return {
        "version": release_version_label(),
        "commit": "f16aa4c06",
        "timestamp": "2026-03-12T09:07:53+08:00",
        "status": "FORGED",
    }
