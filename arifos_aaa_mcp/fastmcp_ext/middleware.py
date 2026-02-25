"""Middleware-style helpers for normalized tool responses."""

from __future__ import annotations

from typing import Any


def normalize_error(stage: str, error: Exception) -> dict[str, Any]:
    """Canonical MCP-facing error payload."""
    return {
        "verdict": "VOID",
        "stage": stage,
        "error": str(error),
    }


def attach_runtime_meta(payload: dict[str, Any], transport: str) -> dict[str, Any]:
    """Attach non-sensitive runtime metadata to payload."""
    merged = dict(payload)
    meta = dict(merged.get("runtime", {}))
    meta["transport"] = transport
    merged["runtime"] = meta
    return merged
