"""
arifosmcp.intelligence/core/lifecycle.py — Compatibility shim for session lifecycle.

The canonical implementation now lives in `arifosmcp.transport.sessions.lifecycle`.
This module re-exports the public lifecycle surface so existing imports under
`arifosmcp.intelligence.core.lifecycle` continue to work without forking state logic.
"""

from arifosmcp.transport.sessions.lifecycle import KernelState, LifecycleManager, Session

__all__ = ["KernelState", "LifecycleManager", "Session"]
