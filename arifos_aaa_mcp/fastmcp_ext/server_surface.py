"""Server surface helpers for FastMCP registration."""

from __future__ import annotations

from fastmcp import FastMCP


def build_server(name: str, instructions: str) -> FastMCP:
    """Create canonical FastMCP server instance."""
    return FastMCP(name, instructions=instructions)
