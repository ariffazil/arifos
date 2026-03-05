from __future__ import annotations

from ..base_agent import Agent, AgentResult


class VALIDATOR(Agent):
    role_id = "A-VALIDATOR"

    async def _execute(self, context: dict) -> AgentResult:
        errors: list[str] = []

        audit = context.get("audit", {})
        objections: list[str] = []
        if isinstance(audit, dict):
            objections = list(audit.get("objections") or [])
        if objections:
            errors.append("Auditor objections unresolved")

        architect = context.get("architect")
        architect_query = ""
        architect_objective = ""
        if isinstance(architect, dict):
            architect_query = str(architect.get("query", "")).strip()
            plan = architect.get("plan")
            if isinstance(plan, dict):
                scope = plan.get("scope")
                if isinstance(scope, dict):
                    architect_objective = str(scope.get("objective", "")).strip()
        else:
            errors.append("Missing architect artifact")

        build_context = context.get("build")
        build_payload = {}
        if isinstance(build_context, dict):
            candidate = build_context.get("build")
            if isinstance(candidate, dict):
                build_payload = candidate

        if not build_payload:
            errors.append("Missing engineer build artifact")
        else:
            objective = str(build_payload.get("objective", "")).strip()
            trace = build_payload.get("trace")
            build_query = ""
            if isinstance(trace, dict):
                build_query = str(trace.get("architect_query", "")).strip()

            if architect_query and build_query != architect_query:
                errors.append("Engineer build trace does not match architect query")
            if architect_objective and objective != architect_objective:
                errors.append("Engineer build objective does not match architect objective")

        if errors:
            return AgentResult(
                verdict="SABAR",
                error="; ".join(errors),
                data={"errors": errors, "objections": objections},
            )

        return AgentResult(verdict="SEAL", data={"validated": True, "objections": []})
