"""
L1 Cognition — Intelligence Layer Re-exports.

This sub-package re-exports the ACLIP intelligence layer (aclip_cai).
Import from here or from ``aclip_cai.*`` directly — both paths work.

Example::

    from core.l1_cognition import MCPResponse, register_aclip_tools
    # equivalent to:
    from aclip_cai.mcp_bridge import MCPResponse, register_aclip_tools
"""

from __future__ import annotations

# MCP bridge
try:
    from aclip_cai.mcp_bridge import MCPResponse, register_aclip_tools  # noqa: F401
except ImportError:
    pass

# Triad operations
try:
    from aclip_cai import triad  # noqa: F401
except ImportError:
    pass

# Core lifecycle
try:
    from aclip_cai.core.lifecycle import SessionLifecycle  # noqa: F401
    from aclip_cai.core.floor_audit import run_floor_audit  # noqa: F401
except ImportError:
    pass

__all__ = [
    "MCPResponse",
    "register_aclip_tools",
    "SessionLifecycle",
    "run_floor_audit",
]
