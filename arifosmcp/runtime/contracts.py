"""Phase 3 contracts for arifOS AAA MCP.

Provides lightweight input guards and session continuity checks
without changing transport/runtime dependencies.
"""

from __future__ import annotations

REQUIRES_SESSION: set[str] = {
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
}
