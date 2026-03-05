"""OpenAI Apps adapter resource bindings for arifOS.

This module is adapter-scoped (host profile). It does not change core tool
contracts or governance logic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

UI_RESOURCE_URI = "ui://constitutional-visualizer/mcp-app.html"
UI_RESOURCE_NAME = "constitutional_visualizer"
UI_RESOURCE_MIME = "text/html;profile=mcp-app"

# Adapter-only alias map (host-facing -> canonical).
TOOL_ALIAS_MAP: dict[str, str] = {
    "search": "search_reality",
    "fetch": "fetch_content",
    "health_check": "check_vital",
}

# Optional reverse view for registration/reporting.
CANONICAL_TO_OPENAI_ALIAS: dict[str, str] = {
    "search_reality": "search",
    "fetch_content": "fetch",
    "check_vital": "health_check",
}


def _visualizer_dist_path() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "333_APPS"
        / "constitutional-visualizer"
        / "dist"
        / "mcp-app.html"
    )


def load_constitutional_visualizer_html() -> str:
    """Load bundled constitutional visualizer HTML for MCP app resource."""
    path = _visualizer_dist_path()
    if path.exists():
        return path.read_text(encoding="utf-8")
    return (
        "<html><body><h1>Constitutional visualizer not built.</h1>"
        "<p>Run npm build for 333_APPS/constitutional-visualizer.</p></body></html>"
    )


def register_constitutional_visualizer_resource(mcp: Any) -> None:
    """Bind constitutional visualizer as MCP resource for OpenAI Apps profile."""

    @mcp.resource(
        UI_RESOURCE_URI,
        name=UI_RESOURCE_NAME,
        mime_type=UI_RESOURCE_MIME,
        description="Constitutional visualizer MCP app bundle.",
    )
    def constitutional_visualizer_resource() -> str:
        return load_constitutional_visualizer_html()


def resolve_canonical_tool_name(host_tool_name: str) -> str:
    """Translate host-facing alias names to canonical core tool names."""
    return TOOL_ALIAS_MAP.get(host_tool_name, host_tool_name)


def build_visualize_governance_meta() -> dict[str, Any]:
    """Return UI metadata payload for visualize_governance tool responses."""
    return {
        "ui": {
            "resourceUri": UI_RESOURCE_URI,
            "title": "Constitutional Decision Visualizer",
            "description": "Real-time governance metrics dashboard",
        },
        "openai/outputTemplate": UI_RESOURCE_URI,
    }
