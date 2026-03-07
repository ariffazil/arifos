from __future__ import annotations

from ..base_agent import Agent, AgentResult


class ENGINEER(Agent):
    role_id = "A-ENGINEER"

    async def _execute(self, context: dict) -> AgentResult:
        query = str(context.get("query", "")).strip()
        if not query:
            return AgentResult(verdict="SABAR", error="Missing query")

        architect = context.get("architect")
        if not isinstance(architect, dict):
            return AgentResult(verdict="SABAR", error="Missing architect artifact")

        plan = architect.get("plan")
        architect_query = str(architect.get("query", "")).strip()
        source = architect.get("source")
        if not isinstance(plan, dict) or not architect_query or source != "user_query":
            return AgentResult(verdict="SABAR", error="Invalid architect draft")

        scope = plan.get("scope")
        handoff = plan.get("handoff")
        objective = ""
        if isinstance(scope, dict):
            objective = str(scope.get("objective", "")).strip()
        if not objective:
            return AgentResult(verdict="SABAR", error="Missing architect objective")

        next_steps: list[str] = []
        handoff_owner = ""
        if isinstance(handoff, dict):
            handoff_owner = str(handoff.get("owner", "")).strip()
            raw_steps = handoff.get("next_steps", [])
            if isinstance(raw_steps, list):
                next_steps = [str(step).strip() for step in raw_steps if str(step).strip()]

        build = {
            "mode": "safe-non-destructive",
            "objective": objective,
            "implementation": {
                "plan_type": plan.get("type", "bounded_plan"),
                "handoff_owner": handoff_owner,
                "steps": next_steps,
            },
            "trace": {
                "architect_query": architect_query,
                "architect_source": source,
            },
        }
        return AgentResult(
            verdict="SEAL",
            data={
                "query": query,
                "architect_handoff": {"owner": handoff_owner, "next_steps": next_steps},
                "build": build,
            },
        )
