"""
aclip_cai/core/federation.py — Multi-Agent Health Coordination

Aggregates health signals from registered arifOS agents (aaa_mcp,
aclip_cai sensors, external services) and produces a consolidated
federation health report for the 9-panel dashboard and for use by
the Tri-Witness earth-witness scoring channel.

Authority: ARIF FAZIL (Sovereign)
Version: 2026.02.22-FORGE-KERNEL-SEAL
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

# ---------------------------------------------------------------------------
# AgentStatus
# ---------------------------------------------------------------------------


class AgentStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


@dataclass
class AgentHealth:
    agent_id: str
    status: AgentStatus
    last_check: str  # ISO-8601
    latency_ms: float | None = None
    details: str | None = None
    floor_pass_rate: float | None = None  # Last known constitutional pass rate


# ---------------------------------------------------------------------------
# FederationCoordinator
# ---------------------------------------------------------------------------


class FederationCoordinator:
    """
    Lightweight multi-agent coordination layer.

    Registered agents supply a `health_fn` callable that returns
    an AgentHealth dict. The coordinator polls all agents and
    produces an aggregated earth-witness score (E) for F3 Tri-Witness.
    """

    def __init__(self) -> None:
        self._agents: dict[str, Callable[[], AgentHealth]] = {}
        self._last_results: dict[str, AgentHealth] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, agent_id: str, health_fn: Callable[[], AgentHealth]) -> None:
        """Register an agent with its health polling function."""
        self._agents[agent_id] = health_fn

    def deregister(self, agent_id: str) -> None:
        """Remove an agent from the federation."""
        self._agents.pop(agent_id, None)
        self._last_results.pop(agent_id, None)

    # ------------------------------------------------------------------
    # Health polling
    # ------------------------------------------------------------------

    def poll_all(self) -> dict[str, AgentHealth]:
        """Poll all registered agents and cache results."""
        results: dict[str, AgentHealth] = {}
        for agent_id, fn in self._agents.items():
            try:
                result = fn()
                results[agent_id] = result
            except Exception as exc:
                results[agent_id] = AgentHealth(
                    agent_id=agent_id,
                    status=AgentStatus.OFFLINE,
                    last_check=datetime.now(tz=timezone.utc).isoformat(),
                    details=f"Poll error: {exc}",
                )
        self._last_results = results
        return results

    def poll_agent(self, agent_id: str) -> AgentHealth | None:
        """Poll a single registered agent."""
        fn = self._agents.get(agent_id)
        if not fn:
            return None
        try:
            result = fn()
            self._last_results[agent_id] = result
            return result
        except Exception as exc:
            offine = AgentHealth(
                agent_id=agent_id,
                status=AgentStatus.OFFLINE,
                last_check=datetime.now(tz=timezone.utc).isoformat(),
                details=str(exc),
            )
            self._last_results[agent_id] = offine
            return offine

    # ------------------------------------------------------------------
    # Earth-witness score (F3 Tri-Witness — E channel)
    # ------------------------------------------------------------------

    def earth_witness_score(self) -> float:
        """
        Compute earth-witness (E) score for F3 Tri-Witness.

        E = fraction of registered agents that are HEALTHY.
        If no agents registered, E = 0.5 (neutral/unknown).
        """
        if not self._last_results:
            self.poll_all()
        if not self._last_results:
            return 0.5

        healthy = sum(1 for h in self._last_results.values() if h.status == AgentStatus.HEALTHY)
        return healthy / len(self._last_results)

    # ------------------------------------------------------------------
    # Summary report
    # ------------------------------------------------------------------

    def federation_report(self) -> dict:
        """Return a telemetry-friendly federation summary."""
        results = self._last_results or self.poll_all()
        statuses = {aid: h.status.value for aid, h in results.items()}
        healthy_count = sum(1 for h in results.values() if h.status == AgentStatus.HEALTHY)
        return {
            "total_agents": len(results),
            "healthy": healthy_count,
            "degraded": sum(1 for h in results.values() if h.status == AgentStatus.DEGRADED),
            "offline": sum(1 for h in results.values() if h.status == AgentStatus.OFFLINE),
            "earth_witness": round(self.earth_witness_score(), 3),
            "agents": statuses,
            "polled_at": datetime.now(tz=timezone.utc).isoformat(),
        }
