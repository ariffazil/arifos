"""
AGENT: VALIDATOR (APEX Ψ)
Symbol: Ψ
Stages: 888-999 (Judge → Seal)

The VALIDATOR is the Soul of the system.
It renders the final verdict and seals the ledger.

Responsibilities:
- 888_JUDGE: Tri-witness consensus, Genius check
- 999_SEAL: Cryptographic logging, closure

Constitutional Floors:
- F3: Tri-Witness (Consensus)
- F8: Genius (G ≥ 0.80)
- F11: Authority (Command verified)
"""

import inspect
from importlib import import_module
from typing import Any


def _resolve_apex_tool() -> Any:
    for module_name, attr in (("aaa_mcp.server", "apex_judge"), ("aaa_mcp.server", "seal_vault")):
        try:
            tool = getattr(import_module(module_name), attr)
            resolved = getattr(tool, "fn", tool)
            if attr == "apex_judge":
                judge = resolved
            else:
                seal = resolved
        except (ImportError, AttributeError):
            continue
    return {"judge": locals().get("judge"), "seal": locals().get("seal")}


APEX_TOOLS = _resolve_apex_tool()

from . import Agent, AgentResult


class VALIDATOR(Agent):
    """
    APEX Agent - The Judge.

    Final constitutional authority.
    Seals the outcome if floors are met.
    """

    name = "VALIDATOR"
    symbol = "Ψ"

    async def _execute_apex(self, action: str, **kwargs: Any) -> dict[str, Any]:
        tool = APEX_TOOLS.get(action)
        if tool is None:
            return {
                "verdict": "VOID",
                "error": f"AAA MCP {action} tool not available",
                "stage": "888-999",
            }
        try:
            result = tool(**kwargs)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, dict):
                return result
            return {
                "verdict": "VOID",
                "error": "Invalid AAA MCP response type",
                "stage": "888-999",
            }
        except Exception as exc:
            return {"verdict": "VOID", "error": str(exc), "stage": "888-999"}

    async def judge(self, query: str, session_id: str) -> dict[str, Any]:
        """888_JUDGE: Render verdict."""
        return await self._execute_apex("judge", session_id=session_id, query=query)

    async def seal(self, judge_result: dict[str, Any], session_id: str) -> dict[str, Any]:
        """999_SEAL: Cryptographic seal."""
        summary = f"L5 VALIDATOR summary: verdict={judge_result.get('verdict', 'UNKNOWN')}"
        return await self._execute_apex("seal", session_id=session_id, summary=summary)

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Run full APEX pipeline."""
        if not isinstance(context, dict):
            return AgentResult(verdict="VOID", agent=self.name, error="Context must be a dict")

        query = str(self._safe_get(context, "query", "")).strip()
        session_id = str(self._safe_get(context, "session_id", "")).strip()
        if not query:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing query for VALIDATOR execution"
            )
        if not session_id:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing session_id for VALIDATOR execution"
            )

        judge = await self.judge(query=query, session_id=session_id)
        if judge.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=judge, error=judge.get("error")
            )

        seal = await self.seal(judge_result=judge, session_id=session_id)

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"judge": judge, "seal": seal},
        )
