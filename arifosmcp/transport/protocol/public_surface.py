"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""Compatibility re-exports for the AAA public surface."""

from __future__ import annotations

from .aaa_contract import (
    AAA_CANONICAL_TOOLS,
    AAA_PROMPT_NAMES,
    AAA_RESOURCE_URIS,
    AAA_TOOL_ALIASES,
)

PUBLIC_CANONICAL_TOOLS = AAA_CANONICAL_TOOLS
PUBLIC_TOOL_ALIASES = AAA_TOOL_ALIASES
PUBLIC_RESOURCE_URIS = AAA_RESOURCE_URIS
PUBLIC_PROMPT_NAMES = AAA_PROMPT_NAMES

__all__ = [
    "PUBLIC_CANONICAL_TOOLS",
    "PUBLIC_PROMPT_NAMES",
    "PUBLIC_RESOURCE_URIS",
    "PUBLIC_TOOL_ALIASES",
]
