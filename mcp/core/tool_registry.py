"""
arifOS MCP Tool Registry
Single source of truth for the 9 canonical constitutional tools (no aliases).
"""

import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class ToolDefinition:
    """MCP Tool Definition Schema"""

    name: str
    title: str
    description: str
    input_schema: Dict[str, Any]
    handler: Optional[Callable[..., Awaitable[Dict[str, Any]]]] = None
    output_schema: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "inputSchema": self.input_schema,
        }
        if self.output_schema:
            result["outputSchema"] = self.output_schema
        if self.annotations:
            result["annotations"] = self.annotations
        return result


class ToolRegistry:
    """
    Central registry for all MCP tools.
    All transports (stdio, SSE, HTTP) consume this registry.
    """

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._register_canonical_tools()

    def register(self, tool: ToolDefinition) -> None:
        """Register a new tool."""
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name."""
        return self._tools.get(name)

    def list_tools(self) -> Dict[str, ToolDefinition]:
        """Get all registered tools."""
        return self._tools

    def _register_canonical_tools(self):
        """Register the 9 canonical constitutional tools with explicit, LLM-friendly names."""
        # Import handlers inside method to break circular dependency
        from ..tools.canonical_trinity import (
            mcp_agi,
            mcp_apex,
            mcp_asi,
            mcp_init,
            mcp_reality,
            mcp_trinity,
            mcp_vault,
        )

        # 1. init_gate (session gate)
        self.register(
            ToolDefinition(
                name="init_gate",
                title="Session Initialization Gate",
                description="Initialize a governed session with arifOS constitutional framework. Verifies caller authority (F11), scans for prompt injection (F12), injects 13 constitutional floors, and collapses to APEX Genius score (G = A × P × X × E²). Returns motto 'DITEMPA BUKAN DIBERI 💎🔥🧠' and full APEX summary. Use this first before any other constitutional tools.",
                handler=mcp_init,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Initial user request"},
                        "user_token": {
                            "type": "string",
                            "description": "Optional Ed25519 signature token",
                        },
                        "lane": {"type": "string", "enum": ["HARD", "SOFT"], "default": "SOFT"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session ID to resume",
                        },
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR", "888_HOLD"]},
                        "session_id": {"type": "string"},
                        "authority_level": {"type": "string", "enum": ["guest", "user", "admin", "sovereign"]},
                        "authority_verified": {"type": "boolean"},
                        "injection_check_passed": {"type": "boolean"},
                        "injection_risk": {"type": "number"},
                        "lane": {"type": "string", "enum": ["HARD", "SOFT", "PHATIC"]},
                        "intent": {"type": "string"},
                        "motto": {"type": "string", "description": "DITEMPA BUKAN DIBERI 💎🔥🧠"},
                        "seal": {"type": "string", "enum": ["SEAL", "VOID", "SABAR", "888_HOLD"]},
                        "apex_summary": {
                            "type": "object",
                            "properties": {
                                "G": {"type": "number", "description": "Genius score (G = A × P × X × E²)"},
                                "verdict": {"type": "string"},
                                "A": {"type": "number", "description": "Akal/Clarity (AGI Mind)"},
                                "P": {"type": "number", "description": "Present/Regulation (APEX Soul)"},
                                "X": {"type": "number", "description": "Exploration/Trust (ASI Heart)"},
                                "E2": {"type": "number", "description": "Energy² (Earth)"},
                                "13_floors_injected": {"type": "boolean"},
                                "collapsed_to": {"type": "string"}
                            }
                        },
                        "floors_checked": {"type": "array", "items": {"type": "string"}},
                        "tri_witness": {"type": "object"},
                        "TW": {"type": "number", "description": "Tri-Witness score (F3)"},
                        "entropy_input": {"type": "number"},
                        "entropy_target": {"type": "number"},
                        "energy_budget": {"type": "number"},
                        "reason": {"type": "string"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string"},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"},
                            },
                        },
                    },
                    "required": ["verdict", "session_id", "motto", "seal"],
                },
                annotations={
                    "title": "Session Gate",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 2. agi_sense
        self.register(
            ToolDefinition(
                name="agi_sense",
                title="Input Parsing & Intent Detection",
                description="Parse the user input, detect intent, and classify the request into constitutional lanes (HARD/SOFT/PHATIC). Use this when you need to understand what kind of task the user is asking for.",
                handler=lambda **kw: mcp_agi(action="sense", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "User input to parse"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "intent": {"type": "string"},
                        "lane": {"type": "string", "enum": ["HARD", "SOFT", "PHATIC"]},
                        "complexity": {"type": "number"},
                        "error": {"type": "object"},
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Intent Detection",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 3. agi_think
        self.register(
            ToolDefinition(
                name="agi_think",
                title="Hypothesis Generation",
                description="Generate multiple possible hypotheses, options, or plans for how to respond to the user. Does not commit to a final verdict. Use this when you need to explore different approaches.",
                handler=lambda **kw: mcp_agi(action="think", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                        "num_hypotheses": {"type": "integer", "default": 3},
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "hypotheses": {"type": "array"},
                        "error": {"type": "object"},
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Hypothesis Generation",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 4. agi_reason
        self.register(
            ToolDefinition(
                name="agi_reason",
                title="Deep Logical Reasoning",
                description="Perform deep logical reasoning over the user's question and context. Builds a step-by-step reasoning chain and enforces Truth (F2) and Clarity (F4). Returns SEAL if logic is sound, VOID if truth/clarity floors fail.",
                handler=lambda **kw: mcp_agi(action="reason", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Question or problem to reason about",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["default", "atlas", "physics", "forge", "reflect"],
                            "description": "Reasoning mode:\n- default: Standard step-by-step reasoning\n- atlas: Build a map of concepts and dependencies\n- physics: Emphasize physical constraints and thermodynamics\n- forge: Deep synthesis, high-effort reasoning\n- reflect: Constitutional critique of the reasoning itself",
                            "default": "default",
                        },
                        "context": {"type": "object"},
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "stage": {"type": "string"},
                        # sense output
                        "intent_lane": {
                            "type": "string",
                            "enum": ["HARD", "SOFT", "PHATIC", "UNKNOWN"],
                        },
                        "task_type": {"type": "string"},
                        "risk_flags": {"type": "array", "items": {"type": "string"}},
                        "ambiguities": {"type": "array", "items": {"type": "string"}},
                        # think output
                        "options": {"type": "array"},
                        "assumptions": {"type": "array", "items": {"type": "string"}},
                        "unknowns": {"type": "array", "items": {"type": "string"}},
                        # reason/full output
                        "entropy_delta": {"type": "number"},
                        "omega_0": {"type": "number"},
                        "precision": {"type": "object"},
                        "hierarchical_beliefs": {"type": "object"},
                        "action_policy": {"type": "object"},
                        "vote": {"type": "string", "enum": ["SEAL", "VOID", "SABAR", "UNCERTAIN"]},
                        "floor_scores": {"type": "object"},
                        "conclusion": {"type": "string"},
                        "confidence": {"type": "number"},
                        "premises": {"type": "array", "items": {"type": "string"}},
                        "counterarguments": {"type": "array", "items": {"type": "string"}},
                        "reflection": {"type": "object"},
                        "verdict": {
                            "type": "string",
                            "enum": ["SEAL", "VOID", "SABAR"],
                            "description": "SEAL = approved under all required floors.\nVOID = rejected due to a hard floor violation (see error.code).\nSABAR = uncertain; requires human review.",
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Natural language explanation of the reasoning",
                        },
                        "floors": {
                            "type": "object",
                            "description": "Scores and checks for relevant constitutional floors",
                        },
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "enum": [
                                        "F2_TRUTH",
                                        "F4_CLARITY",
                                        "F7_HUMILITY",
                                        "F10_ONTOLOGY",
                                        "INTERNAL_ERROR",
                                    ],
                                },
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"},
                            },
                        },
                    },
                    "required": ["session_id", "verdict"],
                },
                annotations={
                    "title": "Deep Reasoning",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 5. asi_empathize (split from _asi_ action="empathize")
        self.register(
            ToolDefinition(
                name="asi_empathize",
                title="Stakeholder Impact Analysis",
                description="Model human impact and emotional/safety context. Identifies all stakeholders, calculates vulnerability scores, and finds the weakest stakeholder. Enforces Empathy (F6) and Peace² (F5).",
                handler=lambda **kw: mcp_asi(action="empathize", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "scenario": {
                            "type": "string",
                            "description": "Description of the situation or plan to assess for human impact",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                        "actors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional list of affected parties or stakeholders",
                        },
                    },
                    "required": ["scenario"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "stakeholders": {"type": "array"},
                        "weakest_stakeholder": {"type": "object"},
                        "empathy_kappa_r": {
                            "type": "number",
                            "description": "Empathy score (F6), must be >= 0.95",
                        },
                        "peace_squared": {
                            "type": "number",
                            "description": "Peace² score (F5), must be >= 1.0",
                        },
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "enum": [
                                        "F5_PEACE",
                                        "F6_EMPATHY",
                                        "F9_ANTI_HANTU",
                                        "INTERNAL_ERROR",
                                    ],
                                },
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"},
                            },
                        },
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Stakeholder Analysis",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 6. asi_align
        self.register(
            ToolDefinition(
                name="asi_align",
                title="Ethical Alignment Check",
                description="Reconcile user request with ethics, law, and policy. Checks if the proposed action aligns with constitutional floors and societal norms.",
                handler=lambda **kw: mcp_asi(action="align", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "proposal": {"type": "string"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                    },
                    "required": ["proposal"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "alignment_score": {"type": "number"},
                        "concerns": {"type": "array"},
                        "error": {"type": "object"},
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Ethical Alignment",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 7. apex_verdict
        self.register(
            ToolDefinition(
                name="apex_verdict",
                title="Final Constitutional Verdict",
                description="Synthesize AGI reasoning and ASI safety analysis into a final constitutional verdict. Enforces Tri-Witness consensus (F3) and returns SEAL, VOID, or SABAR.",
                handler=lambda **kw: mcp_apex(action="judge", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query or decision to render final verdict on",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                        "agi_result": {"type": "object", "description": "Result from agi_reason"},
                        "asi_result": {
                            "type": "object",
                            "description": "Result from asi_empathize",
                        },
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {
                            "type": "string",
                            "enum": ["SEAL", "VOID", "SABAR"],
                            "description": "Final constitutional verdict",
                        },
                        "trinity_score": {
                            "type": "number",
                            "description": "Tri-Witness consensus score (F3), must be >= 0.95",
                        },
                        "proof": {"type": "object"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "enum": [
                                        "F3_TRI_WITNESS",
                                        "F8_GENIUS",
                                        "F11_AUTHORITY",
                                        "INTERNAL_ERROR",
                                    ],
                                },
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"},
                            },
                        },
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Final Verdict",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 8. reality_search
        self.register(
            ToolDefinition(
                name="reality_search",
                title="External Fact-Checking",
                description="Query external sources (Brave Search API) for real-time fact-checking and verification. Enforces Humility (F7) by citing all sources and stating uncertainty. Use when you need current information beyond training data.",
                handler=mcp_reality,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for fact-checking",
                            "maxLength": 500,
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                        "freshness": {
                            "type": "string",
                            "enum": ["24h", "7d", "30d", "any"],
                            "default": "7d",
                        },
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "verified": {"type": "boolean"},
                        "confidence": {"type": "number"},
                        "sources": {"type": "array"},
                        "error": {"type": "object"},
                    },
                    "required": ["verdict"],
                },
                annotations={
                    "title": "Reality Check",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 9. vault_seal (seal & ledger)
        self.register(
            ToolDefinition(
                name="vault_seal",
                title="Immutable Ledger (Seal)",
                description="Tamper-proof storage using Merkle-tree sealing. Implements F1 Amanah (Trust).",
                # Vault999 records events regardless of approval; verdict is a field. VOID entries are still recorded for audit truth.
                handler=mcp_vault,
                input_schema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["seal", "list", "read", "query", "verify", "proof", "propose"],
                            "default": "seal",
                        },
                        "verdict": {"type": "string"},
                        "decision_data": {"type": "object"},
                        "target": {
                            "type": "string",
                            "enum": ["seal", "ledger", "canon", "fag", "tempa", "phoenix", "audit"],
                            "default": "seal",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                    },
                    "required": ["action"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "merkle_root": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "seal_id": {"type": "string"},
                        "target": {"type": "string"},
                        "integrity_hash": {"type": "string"},
                        "status": {"type": "string", "enum": ["SEALED", "PENDING", "ERROR"]},
                    },
                    "required": ["seal_id", "merkle_root", "status"],
                },
                annotations={
                    "title": "Vault Seal",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 10. _trinity_ (The Meta-Loop)
        self.register(
            ToolDefinition(
                name="_trinity_",
                title="Full Metabolic Cycle (The Loop)",
                description="Executes the complete AGI→ASI→APEX→VAULT constitutional loop in a single call. Use this for standard requests that require a final verified verdict.",
                handler=mcp_trinity,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The request to process through the full loop",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Optional session ID to link context",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$",
                        },
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "session_id": {"type": "string"},
                        "public_rationale": {"type": "string"},
                        "rule_hits": {"type": "array", "items": {"type": "string"}},
                        "error": {"type": "object"},
                    },
                    "required": ["verdict", "session_id"],
                },
                annotations={
                    "title": "Metabolic Loop",
                    "readOnlyHint": False,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )
