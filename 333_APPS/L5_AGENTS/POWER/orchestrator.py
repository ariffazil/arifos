from __future__ import annotations

from .base_agent import AgentResult
from .enforcement.gates import should_halt_on_auditor
from .roles.architect import ARCHITECT
from .roles.auditor import AUDITOR
from .roles.engineer import ENGINEER
from .roles.validator import VALIDATOR


class Orchestrator:
    async def run(self, query: str) -> dict:
        normalized = str(query).strip()
        if not normalized:
            return {
                "verdict": "SABAR",
                "cycle_complete": False,
                "reason": "Missing query input",
            }

        architect = ARCHITECT()
        auditor = AUDITOR()
        engineer = ENGINEER()
        validator = VALIDATOR()

        a: AgentResult = await architect.execute({"query": normalized})
        if a.verdict in ("VOID", "888_HOLD"):
            return {
                "verdict": a.verdict,
                "source": "A-ARCHITECT",
                "data": a.data,
                "error": a.error,
            }

        u: AgentResult = await auditor.execute(
            {"query": normalized, "claim": str(a.data)}
        )
        if should_halt_on_auditor(u.verdict):
            return {
                "verdict": u.verdict,
                "cycle_complete": False,
                "source": "A-AUDITOR",
                "data": u.data,
                "error": u.error,
            }

        e: AgentResult = await engineer.execute(
            {"query": normalized, "draft": str(a.data)}
        )
        if e.verdict in ("VOID", "888_HOLD"):
            return {
                "verdict": e.verdict,
                "source": "A-ENGINEER",
                "data": e.data,
                "error": e.error,
            }

        v: AgentResult = await validator.execute(
            {"query": normalized, "audit": u.data, "build": e.data}
        )
        return {
            "verdict": v.verdict,
            "cycle_complete": v.verdict == "SEAL",
            "artifacts": {
                "architect": a.data,
                "auditor": u.data,
                "engineer": e.data,
                "validator": v.data,
            },
            "error": v.error,
        }
