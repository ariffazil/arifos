from __future__ import annotations

from ..base_agent import Agent, AgentResult


class VALIDATOR(Agent):
    role_id = "A-VALIDATOR"

    async def _execute(self, context: dict) -> AgentResult:
        audit = context.get("audit", {})
        objections = []
        if isinstance(audit, dict):
            objections = list(audit.get("objections") or [])
        if objections:
            return AgentResult(
                verdict="SABAR",
                error="Auditor objections unresolved",
                data={"objections": objections},
            )
        return AgentResult(verdict="SEAL", data={"validated": True})
