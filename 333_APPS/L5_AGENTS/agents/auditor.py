"""
AGENT: AUDITOR (EYE)
Symbol: 👁
Stages: Cross-cutting (Verification)

The AUDITOR is the Witness.
It verifies facts, checks reality, and ensures truth.

Responsibilities:
- 444_EVIDENCE: Fact-checking, reality grounding
- Cross-stage verification
- Truth validation (F2)
- Injection detection (F12)

The AUDITOR sees all and speaks truth.
"""

import inspect
from importlib import import_module
from typing import Any


def _resolve_reality_tool() -> Any:
    for module_name, attr in (("aaa_mcp.server", "search_reality"), ("aaa_mcp.server", "audit_rules")):
        try:
            tool = getattr(import_module(module_name), attr)
            resolved = getattr(tool, "fn", tool)
            if attr == "search_reality":
                search = resolved
            else:
                audit = resolved
        except (ImportError, AttributeError):
            continue
    return {"search": locals().get("search"), "audit": locals().get("audit")}


REALITY_TOOLS = _resolve_reality_tool()

from . import Agent, AgentResult


class AUDITOR(Agent):
    """
    EYE Agent - The Witness.

    Verifies claims against external reality.
    Grounds the system in facts, not hallucinations.
    """

    name = "AUDITOR"
    symbol = "👁"

    async def _execute_reality(self, action: str, **kwargs: Any) -> dict[str, Any]:
        tool = REALITY_TOOLS.get(action)
        if tool is None:
            return {
                "verdict": "VOID",
                "error": f"AAA MCP {action} tool not available",
                "stage": "444_EVIDENCE",
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
                "stage": "444_EVIDENCE",
            }
        except Exception as exc:
            return {"verdict": "VOID", "error": str(exc), "stage": "444_EVIDENCE"}

    async def evidence(self, claim: str) -> dict[str, Any]:
        """444_EVIDENCE: Fact-check claim."""
        if not claim:
            return {"verdict": "SABAR", "stage": "444_EVIDENCE", "error": "No claim to verify"}
        return await self._execute_reality("search", query=claim, intent="verification")

    async def detect_injection(self, input_data: str) -> dict[str, Any]:
        """F12: Injection defense."""
        suspicious_markers = ("ignore previous", "override", "system prompt", "sudo rm -rf")
        lowered = input_data.lower()
        if any(marker in lowered for marker in suspicious_markers):
            return {
                "verdict": "VOID",
                "stage": "444_EVIDENCE",
                "error": "Potential prompt injection detected",
            }
        return await self._execute_reality("audit", audit_scope="quick", verify_floors=True)

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Run audit pipeline. Context is a dict with 'claim' and 'input' keys."""
        if not isinstance(context, dict):
            return AgentResult(verdict="VOID", agent=self.name, error="Context must be a dict")

        claim = str(self._safe_get(context, "claim", "")).strip()
        input_data = str(self._safe_get(context, "input", "")).strip()

        # 1. Check Injection (F12)
        injection = await self.detect_injection(input_data)
        if injection.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=injection, error=injection.get("error")
            )

        # 2. Check Truth (F2)
        evidence = await self.evidence(claim)
        truth_data = {
            "score": evidence.get("truth_score"),
            "sources": [r.get("url") for r in evidence.get("results", []) if isinstance(r, dict)],
        }

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"evidence": evidence, "truth": truth_data, "injection_safe": injection},
        )
