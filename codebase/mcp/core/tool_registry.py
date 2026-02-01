"""
arifOS MCP Tool Registry
Single Source of Truth for all 7 Constitutional Tools.
"""

from typing import Dict, Any, Optional, Callable, Awaitable
from dataclasses import dataclass
import logging

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
        self._register_compatibility_aliases()

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
            mcp_init,
            mcp_agi,
            mcp_asi,
            mcp_apex,
            mcp_vault,
            mcp_trinity,
            mcp_reality,
        )

        # 1. init_reboot (was: _init_)
        self.register(
            ToolDefinition(
                name="init_reboot",
                title="Session Initialization Gate",
                description="Initialize a governed session. Verify caller authority, scan for prompt injection (F12), and open a session ledger entry. Use this before running other tools when starting a new workflow.",
                handler=mcp_init,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Initial user request"},
                        "user_token": {"type": "string", "description": "Optional Ed25519 signature token"},
                        "lane": {"type": "string", "enum": ["HARD", "SOFT"], "default": "SOFT"},
                        "session_id": {"type": "string", "description": "Optional session ID to resume"}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "session_id": {"type": "string"},
                        "authority_level": {"type": "string"},
                        "injection_check_passed": {"type": "boolean"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string"},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "required": ["verdict", "session_id"]
                },
                annotations={
                    "title": "Session Gate",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 2. agi_sense (split from _agi_ action="sense")
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
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        }
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "intent": {"type": "string"},
                        "lane": {"type": "string", "enum": ["HARD", "SOFT", "PHATIC"]},
                        "complexity": {"type": "number"},
                        "error": {"type": "object"}
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Intent Detection",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 3. agi_think (split from _agi_ action="think")
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
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "num_hypotheses": {"type": "integer", "default": 3}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "hypotheses": {"type": "array"},
                        "error": {"type": "object"}
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Hypothesis Generation",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 4. agi_reason (split from _agi_ action="reason")
        self.register(
            ToolDefinition(
                name="agi_reason",
                title="Deep Logical Reasoning",
                description="Perform deep logical reasoning over the user's question and context. Builds a step-by-step reasoning chain and enforces Truth (F2) and Clarity (F4). Returns SEAL if logic is sound, VOID if truth/clarity floors fail.",
                handler=lambda **kw: mcp_agi(action="reason", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Question or problem to reason about"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["default", "atlas", "physics", "forge"],
                            "description": "Reasoning mode:\n- default: Standard step-by-step reasoning\n- atlas: Build a map of concepts and dependencies\n- physics: Emphasize physical constraints and thermodynamics\n- forge: Deep synthesis, high-effort reasoning",
                            "default": "default"
                        },
                        "context": {"type": "object"}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {
                            "type": "string",
                            "enum": ["SEAL", "VOID", "SABAR"],
                            "description": "SEAL = approved under all required floors.\nVOID = rejected due to a hard floor violation (see error.code).\nSABAR = uncertain; requires human review."
                        },
                        "reasoning": {"type": "string", "description": "Natural language explanation of the reasoning"},
                        "floors": {"type": "object", "description": "Scores and checks for relevant constitutional floors"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "enum": ["F2_TRUTH", "F4_CLARITY", "F7_HUMILITY", "F10_ONTOLOGY", "INTERNAL_ERROR"]},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "required": ["verdict"]
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
                        "scenario": {"type": "string", "description": "Description of the situation or plan to assess for human impact"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "actors": {"type": "array", "items": {"type": "string"}, "description": "Optional list of affected parties or stakeholders"}
                    },
                    "required": ["scenario"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "stakeholders": {"type": "array"},
                        "weakest_stakeholder": {"type": "object"},
                        "empathy_kappa_r": {"type": "number", "description": "Empathy score (F6), must be >= 0.95"},
                        "peace_squared": {"type": "number", "description": "Peace² score (F5), must be >= 1.0"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "enum": ["F5_PEACE", "F6_EMPATHY", "F9_ANTI_HANTU", "INTERNAL_ERROR"]},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Stakeholder Analysis",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 6. asi_align (split from _asi_ action="align")
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
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        }
                    },
                    "required": ["proposal"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "alignment_score": {"type": "number"},
                        "concerns": {"type": "array"},
                        "error": {"type": "object"}
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Ethical Alignment",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 7. asi_insight (split from _asi_ action="act")
        self.register(
            ToolDefinition(
                name="asi_insight",
                title="Risk & Trade-off Analysis",
                description="Surface key risks, trade-offs, and safety considerations. Provides actionable insights about potential harms and benefits.",
                handler=lambda **kw: mcp_asi(action="act", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        }
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "insights": {"type": "array"},
                        "risks": {"type": "array"},
                        "error": {"type": "object"}
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Risk Analysis",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 8. apex_verdict (was: _apex_)
        self.register(
            ToolDefinition(
                name="apex_verdict",
                title="Final Constitutional Verdict",
                description="Synthesize AGI reasoning and ASI safety analysis into a final constitutional verdict. Enforces Tri-Witness consensus (F3) and returns SEAL, VOID, or SABAR.",
                handler=lambda **kw: mcp_apex(action="judge", **kw),
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The query or decision to render final verdict on"},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context. Required when chaining tools.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "agi_result": {"type": "object", "description": "Result from agi_reason"},
                        "asi_result": {"type": "object", "description": "Result from asi_empathize"}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"], "description": "Final constitutional verdict"},
                        "trinity_score": {"type": "number", "description": "Tri-Witness consensus score (F3), must be >= 0.95"},
                        "proof": {"type": "object"},
                        "error": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "enum": ["F3_TRI_WITNESS", "F8_GENIUS", "F11_AUTHORITY", "INTERNAL_ERROR"]},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Final Verdict",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": False,
                },
            )
        )

        # 9. reality_search (was: _reality_)
        self.register(
            ToolDefinition(
                name="reality_search",
                title="External Fact-Checking",
                description="Query external sources (Brave Search API) for real-time fact-checking and verification. Enforces Humility (F7) by citing all sources and stating uncertainty. Use when you need current information beyond training data.",
                handler=mcp_reality,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for fact-checking", "maxLength": 500},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "freshness": {"type": "string", "enum": ["24h", "7d", "30d", "any"], "default": "7d"}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
                        "verified": {"type": "boolean"},
                        "confidence": {"type": "number"},
                        "sources": {"type": "array"},
                        "error": {"type": "object"}
                    },
                    "required": ["verdict"]
                },
                annotations={
                    "title": "Reality Check",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # Keep _trinity_ and _vault_ as-is (per directive - these are not split)
        # 10. _trinity_ (Loop)
        self.register(
            ToolDefinition(
                name="_trinity_",
                title="Full Constitutional Pipeline",
                description="Complete metabolic loop: AGI→ASI→APEX→VAULT. Single-call constitutional evaluation.",
                handler=mcp_trinity,
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "maxLength": 10000},
                        "session_id": {
                            "type": "string",
                            "description": "Optional session identifier to link this call to prior context.",
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
                        },
                        "auto_seal": {"type": "boolean", "default": True},
                        "context": {"type": "object"},
                    },
                    "required": ["query"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string"},
                        "agi_result": {"type": "object"},
                        "asi_result": {"type": "object"},
                        "apex_result": {"type": "object"},
                        "vault_result": {"type": "object"},
                        "final_verdict": {"type": "string"},
                        "execution_time_ms": {"type": "number"},
                    },
                    "required": ["session_id", "final_verdict"],
                },
                annotations={
                    "title": "Full Trinity",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "openWorldHint": True,
                },
            )
        )

        # 11. _vault_ (Seal)
        self.register(
            ToolDefinition(
                name="_vault_",
                title="Immutable Ledger (Seal)",
                description="Tamper-proof storage using Merkle-tree sealing. Implements F1 Amanah (Trust).",
                handler=mcp_vault,
                input_schema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["seal", "list", "read", "write", "propose"],
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
                            "pattern": "^sess_[a-zA-Z0-9]{8,}$"
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

    def _register_compatibility_aliases(self):
        """Backward compatibility: map old names to new tools with deprecation warnings."""
        import warnings

        # _init_ → init_reboot
        if "_init_" not in self._tools and "init_reboot" in self._tools:
            old_handler = self._tools["init_reboot"].handler

            async def deprecated_init(**kwargs):
                warnings.warn(
                    "_init_ is deprecated, use init_reboot instead. "
                    "Old name will be removed in v56.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return await old_handler(**kwargs)

            tool_def = self._tools["init_reboot"]
            self._tools["_init_"] = ToolDefinition(
                name="_init_",
                handler=deprecated_init,
                title=tool_def.title,
                description=tool_def.description + " [DEPRECATED: use init_reboot]",
                input_schema=tool_def.input_schema,
                output_schema=tool_def.output_schema,
                annotations=tool_def.annotations,
            )

        # _agi_ → agi_reason (default action)
        if "_agi_" not in self._tools and "agi_reason" in self._tools:
            # Import the original handler
            from ..tools.canonical_trinity import mcp_agi

            async def deprecated_agi(**kwargs):
                warnings.warn(
                    "_agi_ is deprecated, use agi_sense, agi_think, or agi_reason instead. "
                    "Old name will be removed in v56.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return await mcp_agi(**kwargs)

            # Create a combined schema that accepts all old actions
            self._tools["_agi_"] = ToolDefinition(
                name="_agi_",
                handler=deprecated_agi,
                title="Mind Engine (Delta) [DEPRECATED]",
                description="Deep reasoning, pattern recognition. DEPRECATED: use agi_sense, agi_think, or agi_reason.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["sense", "think", "reason", "full"],
                            "default": "full",
                        },
                        "query": {"type": "string"},
                        "session_id": {"type": "string"},
                    },
                    "required": ["query"],
                },
                output_schema=self._tools["agi_reason"].output_schema,
                annotations={"title": "Mind Engine [DEPRECATED]", "readOnlyHint": True},
            )

        # _asi_ → asi_empathize (default action)
        if "_asi_" not in self._tools and "asi_empathize" in self._tools:
            from ..tools.canonical_trinity import mcp_asi

            async def deprecated_asi(**kwargs):
                warnings.warn(
                    "_asi_ is deprecated, use asi_empathize, asi_align, or asi_insight instead. "
                    "Old name will be removed in v56.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return await mcp_asi(**kwargs)

            self._tools["_asi_"] = ToolDefinition(
                name="_asi_",
                handler=deprecated_asi,
                title="Heart Engine (Omega) [DEPRECATED]",
                description="Safety evaluation. DEPRECATED: use asi_empathize, asi_align, or asi_insight.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["empathize", "align", "act", "full"],
                            "default": "full",
                        },
                        "query": {"type": "string"},
                        "session_id": {"type": "string"},
                    },
                    "required": ["query"],
                },
                output_schema=self._tools["asi_empathize"].output_schema,
                annotations={"title": "Heart Engine [DEPRECATED]", "readOnlyHint": True},
            )

        # _apex_ → apex_verdict
        if "_apex_" not in self._tools and "apex_verdict" in self._tools:
            old_handler = self._tools["apex_verdict"].handler

            async def deprecated_apex(**kwargs):
                warnings.warn(
                    "_apex_ is deprecated, use apex_verdict instead. "
                    "Old name will be removed in v56.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return await old_handler(**kwargs)

            tool_def = self._tools["apex_verdict"]
            self._tools["_apex_"] = ToolDefinition(
                name="_apex_",
                handler=deprecated_apex,
                title=tool_def.title + " [DEPRECATED]",
                description=tool_def.description + " [DEPRECATED: use apex_verdict]",
                input_schema=tool_def.input_schema,
                output_schema=tool_def.output_schema,
                annotations=tool_def.annotations,
            )

        # _reality_ → reality_search
        if "_reality_" not in self._tools and "reality_search" in self._tools:
            old_handler = self._tools["reality_search"].handler

            async def deprecated_reality(**kwargs):
                warnings.warn(
                    "_reality_ is deprecated, use reality_search instead. "
                    "Old name will be removed in v56.0.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return await old_handler(**kwargs)

            tool_def = self._tools["reality_search"]
            self._tools["_reality_"] = ToolDefinition(
                name="_reality_",
                handler=deprecated_reality,
                title=tool_def.title + " [DEPRECATED]",
                description=tool_def.description + " [DEPRECATED: use reality_search]",
                input_schema=tool_def.input_schema,
                output_schema=tool_def.output_schema,
                annotations=tool_def.annotations,
            )
