from __future__ import annotations

from ..base_agent import Agent, AgentResult


class ARCHITECT(Agent):
    role_id = "A-ARCHITECT"

    async def _execute(self, context: dict) -> AgentResult:
        query = str(context.get("query", "")).strip()
        if not query:
            return AgentResult(verdict="SABAR", error="Missing query")
        plan = {
            "type": "bounded_plan",
            "scope": {
                "objective": query,
                "constraints": ["minimal change", "no extra dependencies"],
                "out_of_scope": ["new infrastructure", "broad refactors"],
            },
            "invariants": [
                "Return SABAR when query is missing",
                "Return SEAL when query is present",
                "Keep implementation transport-agnostic",
            ],
            "rollback_notes": {
                "strategy": "single-file revert",
                "signals": ["schema mismatch", "auditor evidence failure"],
            },
            "unknowns": [
                "downstream consumers that parse plan keys",
                "future auditor evidence schema changes",
            ],
            "handoff": {
                "owner": "implementation_agent",
                "next_steps": [
                    "execute minimal scoped changes",
                    "validate verdict and evidence fields",
                ],
            },
            "evidence": [
                "source: user_query",
                f"query: {query}",
            ],
        }
        return AgentResult(
            verdict="SEAL", data={"plan": plan, "query": query, "source": "user_query"}
        )
