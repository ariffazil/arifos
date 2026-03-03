from __future__ import annotations

from ..base_agent import Agent, AgentResult


class AUDITOR(Agent):
    role_id = "A-AUDITOR"

    async def _execute(self, context: dict) -> AgentResult:
        claim = str(context.get("claim", context.get("query", ""))).strip()
        if not claim:
            return AgentResult(verdict="SABAR", error="Missing claim")
        objections = []
        if "source:" not in claim.lower():
            objections.append("Missing evidence source")
        verdict = "SABAR" if objections else "SEAL"
        return AgentResult(verdict=verdict, data={"objections": objections, "claim": claim})
