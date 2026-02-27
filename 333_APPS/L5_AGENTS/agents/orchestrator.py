"""
ORCHESTRATOR - The 4-Agent Coordinator

Coordinates the constitutional cycle:
ARCHITECT (Δ) → AUDITOR (👁) → ENGINEER (Ω) → VALIDATOR (Ψ)

With continuous AUDITOR oversight.
"""

import asyncio
import inspect
from importlib import import_module
from typing import Any

from .architect import ARCHITECT
from .auditor import AUDITOR
from .engineer import ENGINEER
from .validator import VALIDATOR


class Orchestrator:
    """
    Coordinates 4 agents through 000-999 loop.
    Enforces the Metabolic Pipeline.
    """

    AGENTS = ["ARCHITECT", "AUDITOR", "ENGINEER", "VALIDATOR"]

    async def _anchor(self, query: str, actor_id: str = "L5_ORCHESTRATOR") -> dict[str, Any]:
        try:
            tool = getattr(import_module("aaa_mcp.server"), "anchor_session")
            fn = getattr(tool, "fn", tool)
            result = fn(query=query, actor_id=actor_id)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, dict):
                return result
            return {"verdict": "VOID", "error": "Invalid anchor_session response"}
        except Exception as exc:
            return {"verdict": "VOID", "error": str(exc)}

    async def run(self, query: str, user_token: str | None = None) -> dict[str, Any]:
        """
        Execute full constitutional cycle (The Pipeline).
        Fails fast if any Agent returns VOID.
        """
        normalized_query = str(query).strip()
        if not normalized_query:
            return {
                "verdict": "SABAR",
                "cycle_complete": False,
                "source": "ORCHESTRATOR",
                "reason": "Missing query input",
            }

        anchor = await self._anchor(normalized_query)
        if anchor.get("verdict") == "VOID":
            return {
                "verdict": "VOID",
                "cycle_complete": False,
                "source": "ANCHOR_SESSION",
                "reason": anchor.get("error", "Failed to initialize session"),
                "data": anchor,
            }
        session_id = str(anchor.get("session_id", "")).strip()
        if not session_id:
            return {
                "verdict": "VOID",
                "cycle_complete": False,
                "source": "ANCHOR_SESSION",
                "reason": "Missing session_id from anchor_session",
                "data": anchor,
            }

        # 1. ARCHITECT (Δ) - MIND
        # -----------------------
        architect = ARCHITECT()
        delta_res = await architect.execute(
            {"query": normalized_query, "session_id": session_id, "user_token": user_token}
        )

        if delta_res.verdict == "VOID":
            return self._fail("ARCHITECT (Mind)", delta_res)

        delta_bundle = delta_res.data  # {sense, think, atlas}

        # 2. AUDITOR (👁) - WITNESS 1 (Pre-Build)
        # --------------------------------------
        # Verify the Architect's Plan
        auditor = AUDITOR()
        # We verify the 'atlas' (map) produced by the Architect
        plan_str = str(delta_bundle.get("atlas", ""))
        audit_res = await auditor.execute({"claim": plan_str, "input": normalized_query})

        if audit_res.verdict == "VOID":
            return self._fail("AUDITOR (Injection/Truth)", audit_res)

        # 3. ENGINEER (Ω) - HEART
        # -----------------------
        engineer = ENGINEER()
        # Engineer takes the User Query + Architect's Plan (DeltaBundle)
        # For simplicity in this wiring, we pass the query, but contextually it should know the plan.
        # Ideally: engineer.execute({"query": query, "plan": delta_bundle})
        omega_res = await engineer.execute(
            {"query": normalized_query, "session_id": session_id, "plan": delta_bundle}
        )

        if omega_res.verdict == "VOID":
            return self._fail("ENGINEER (Safety)", omega_res)

        omega_bundle = omega_res.data  # {empathy, align, act}

        # 4. VALIDATOR (Ψ) - SOUL
        # -----------------------
        validator = VALIDATOR()
        # Validator judges the alignment of Mind (Delta) and Heart (Omega)
        judgment_context = (
            f"Query: {normalized_query}\n"
            f"Mind Plan: {delta_bundle}\n"
            f"Heart Build: {omega_bundle}\n"
            f"Audit: {audit_res.data}"
        )

        # In a real system, we pass structured objects, but stringifying for the 'judge' tool
        psi_res = await validator.execute({"query": judgment_context, "session_id": session_id})

        if psi_res.verdict == "VOID":
            return self._fail("VALIDATOR (Judgment)", psi_res)

        # Success!
        return {
            "verdict": "SEAL",
            "cycle_complete": True,
            "session_id": session_id,
            "artifacts": {
                "anchor": anchor,
                "delta": delta_bundle,
                "omega": omega_bundle,
                "judgment": psi_res.data,
            },
        }

    def _fail(self, source: str, result: Any) -> dict[str, Any]:
        """Circuit breaker helper."""
        return {
            "verdict": "VOID",
            "source": source,
            "reason": result.error or "Unknown failure",
            "data": result.data,
        }

    async def run_parallel(self, tasks: list[str]) -> dict[str, Any]:
        """Execute multiple tasks with 4-agent swarm."""
        if not tasks:
            return {"verdict": "SABAR", "results": [], "reason": "No tasks provided"}

        results = await asyncio.gather(*(self.run(task) for task in tasks), return_exceptions=True)
        normalized_results: list[dict[str, Any]] = []
        for result in results:
            if isinstance(result, BaseException):
                normalized_results.append(
                    {
                        "verdict": "VOID",
                        "cycle_complete": False,
                        "source": "ORCHESTRATOR",
                        "reason": str(result),
                    }
                )
            elif isinstance(result, dict):
                normalized_results.append(result)
            else:
                normalized_results.append(
                    {
                        "verdict": "VOID",
                        "cycle_complete": False,
                        "source": "ORCHESTRATOR",
                        "reason": "Invalid result type",
                    }
                )

        top_verdict = "SEAL" if all(r.get("verdict") == "SEAL" for r in normalized_results) else "PARTIAL"
        return {"verdict": top_verdict, "results": normalized_results}
