"""Executable base contract for the POWER plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enforcement.policy import load_role_profiles
from .enforcement.preflight import preflight


@dataclass
class AgentResult:
    verdict: str = "VOID"
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class Agent:
    role_id: str = "A-ORCHESTRATOR"

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        gate = self.run_preflight(context)
        if gate is not None:
            return gate
        return await self._execute(context)

    def run_preflight(self, context: dict[str, Any]) -> AgentResult | None:
        profile = load_role_profiles().get(self.role_id)
        if profile is None:
            return AgentResult(verdict="VOID", error=f"Missing role profile for {self.role_id}")
        gate = preflight(profile, context)
        context["preflight"] = {
            "verdict": gate.verdict,
            "omega_0": gate.omega_0,
            "reasons": list(gate.reasons),
        }
        if gate.verdict in ("VOID", "888_HOLD"):
            return AgentResult(
                verdict=gate.verdict, data=context["preflight"], error="; ".join(gate.reasons)
            )
        return None

    async def _execute(self, context: dict[str, Any]) -> AgentResult:
        raise NotImplementedError


__all__ = ["Agent", "AgentResult"]
