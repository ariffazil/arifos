"""
aaa_mcp — arifOS AAA MCP Transport Adapter (Compatibility Layer)

This module provides backward compatibility for systems expecting the `aaa_mcp`
namespace. It re-exports the canonical arifosmcp runtime surface.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

# Re-export canonical arifOS MCP runtime
from arifosmcp.runtime import (
    create_aaa_mcp_server,
    mcp,
)
from arifosmcp.runtime.bridge import call_kernel
from arifosmcp.runtime.models import (
    CallerContext,
    RuntimeEnvelope,
    Stage,
    Verdict,
)
from arifosmcp.runtime.public_registry import (
    build_mcp_manifest,
    build_server_json,
    public_tool_names,
    public_tool_specs,
)
from arifosmcp.runtime.server import (
    HTTP_PATH,
    PUBLIC_TOOL_PROFILE,
    VALID_TRANSPORT_MODES,
    app,
)

# Core organs for direct access
from core.organs import (
    agi,
    anchor,
    apex,
    asi,
    feel,
    forge,
    init,
    judge,
    seal,
    sense,
    think,
    vault,
)

__version__ = "2026.03.12-FORGED"
__all__ = [
    # Runtime
    "app",
    "call_kernel",
    "create_aaa_mcp_server",
    "HTTP_PATH",
    "mcp",
    "PUBLIC_TOOL_PROFILE",
    "VALID_TRANSPORT_MODES",
    # Models
    "CallerContext",
    "RuntimeEnvelope",
    "Stage",
    "Verdict",
    # Registry
    "build_mcp_manifest",
    "build_server_json",
    "public_tool_names",
    "public_tool_specs",
    # Organs (Canonical)
    "init",
    "anchor",
    "sense",
    "think",
    "agi",
    "feel",
    "empathize",
    "asi",
    "forge",
    "apex",
    "judge",
    "seal",
    "vault",
]
