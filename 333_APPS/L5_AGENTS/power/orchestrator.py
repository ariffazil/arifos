"""POWER orchestrator with no-bypass gate enforcement."""

from __future__ import annotations

from .base_agent import AgentResult
from .enforcement.gates import should_halt_on_auditor
from .roles.architect import ARCHITECT
from .roles.auditor import AUDITOR
from .roles.engineer import ENGINEER
from .roles.validator import VALIDATOR


class Orchestrator:
    async def run(self, query: str) -> dict:
        q = str(query).strip()
        if not q:
            return {"verdict": "SABAR", "reason": "Missing query input", "cycle_complete": False}

        architect = ARCHITECT()
        auditor = AUDITOR()
        engineer = ENGINEER()
        validator = VALIDATOR()

        a: AgentResult = await architect.execute({"query": q})
        if a.verdict in ("VOID", "888_HOLD"):
            return {"verdict": a.verdict, "source": "A-ARCHITECT", "data": a.data, "error": a.error}

        u: AgentResult = await auditor.execute({"query": q, "claim": str(a.data)})
        if should_halt_on_auditor(u.verdict):
            return {
                "verdict": u.verdict,
                "source": "A-AUDITOR",
                "cycle_complete": False,
                "data": u.data,
                "error": u.error,
            }

        e: AgentResult = await engineer.execute({"query": q, "draft": str(a.data)})
        if e.verdict in ("VOID", "888_HOLD"):
            return {"verdict": e.verdict, "source": "A-ENGINEER", "data": e.data, "error": e.error}

        v: AgentResult = await validator.execute({"query": q, "audit": u.data, "build": e.data})
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


__all__ = ["Orchestrator"]
