from __future__ import annotations

from ..base_agent import Agent, AgentResult


class ARCHITECT(Agent):
    role_id = "A-ARCHITECT"

    async def _execute(self, context: dict) -> AgentResult:
        query = str(context.get("query", "")).strip()
        if not query:
            return AgentResult(verdict="SABAR", error="Missing query")
        return AgentResult(verdict="SEAL", data={"plan": "bounded", "query": query})
