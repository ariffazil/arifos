"""
L2 Tools — Canonical 13-Tool Surface Re-exports.

This sub-package re-exports the 13 canonical arifOS MCP tools from
the ``arifos_aaa_mcp`` surface package.

Example::

    from core.l2_tools import anchor_session, apex_judge, seal_vault
"""

from __future__ import annotations

# Re-export the 13 canonical tools from the full server
try:
    from arifos_aaa_mcp.server import (  # noqa: F401
        anchor_session,
        reason_mind,
        vector_memory,
        simulate_heart,
        critique_thought,
        apex_judge,
        eureka_forge,
        seal_vault,
        search_reality,
        ingest_evidence,
        audit_rules,
        check_vital,
        metabolic_loop,
        create_aaa_mcp_server,
        mcp,
    )
except ImportError:
    pass

__all__ = [
    "anchor_session",
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "search_reality",
    "ingest_evidence",
    "audit_rules",
    "check_vital",
    "metabolic_loop",
    "create_aaa_mcp_server",
    "mcp",
]
