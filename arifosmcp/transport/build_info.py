"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.

Runtime/build metadata helpers for HTTP surfaces.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version


def _package_version() -> str:
    try:
        return package_version("arifos")
    except PackageNotFoundError:
        return "unknown"


def get_build_info() -> dict[str, str]:
    """Return stable build metadata for health/version endpoints."""
    resolved_version = os.environ.get("ARIFOS_VERSION") or _package_version()
    build_time = os.environ.get("BUILD_TIME") or datetime.now(timezone.utc).isoformat()

    return {
        "version": resolved_version,
        "schema_version": resolved_version,
        "git_sha": os.environ.get("GIT_SHA", "unknown"),
        "build_time": build_time,
    }


__all__ = ["get_build_info"]
