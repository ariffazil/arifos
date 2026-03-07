"""
aclip_cai/core/lifecycle.py — Compatibility shim for session lifecycle.

The canonical implementation now lives in `aaa_mcp.sessions.lifecycle`.
This module re-exports the public lifecycle surface so existing imports under
`aclip_cai.core.lifecycle` continue to work without forking state logic.
"""

from aaa_mcp.sessions.lifecycle import KernelState, LifecycleManager, Session

__all__ = ["KernelState", "LifecycleManager", "Session"]
