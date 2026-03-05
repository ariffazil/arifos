from __future__ import annotations

from ..base_agent import Agent, AgentResult


class AUDITOR(Agent):
    role_id = "A-AUDITOR"

    async def _execute(self, context: dict) -> AgentResult:
        objections: list[str] = []
        architect = context.get("architect")
        if not isinstance(architect, dict):
            objections.append("Missing architect artifact")
            return AgentResult(
                verdict="SABAR",
                error="Invalid architect artifact",
                data={"objections": objections},
            )

        plan = architect.get("plan")
        query = architect.get("query")
        source = architect.get("source")

        if not isinstance(plan, dict):
            objections.append("Missing architect plan")
        if not isinstance(query, str) or not query.strip():
            objections.append("Missing architect query")
        if source != "user_query":
            objections.append("Missing or invalid architect source")

        if isinstance(plan, dict):
            for required_key in ("scope", "invariants", "handoff", "evidence"):
                if required_key not in plan:
                    objections.append(f"Missing plan section: {required_key}")

            scope = plan.get("scope")
            if not isinstance(scope, dict) or not str(scope.get("objective", "")).strip():
                objections.append("Missing plan scope objective")

            evidence = plan.get("evidence")
            if not isinstance(evidence, list) or "source: user_query" not in evidence:
                objections.append("Missing evidence marker: source: user_query")

        verdict = "SABAR" if objections else "SEAL"
        return AgentResult(
            verdict=verdict,
            error="; ".join(objections) if objections else None,
            data={
                "objections": objections,
                "architect": {
                    "query": query,
                    "source": source,
                    "plan_sections": list(plan.keys()) if isinstance(plan, dict) else [],
                },
            },
        )
