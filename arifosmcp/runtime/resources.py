"""
arifosmcp/runtime/resources.py — arifOS FastMCP Resource Layer

Read-only, structured views of the arifOS canon, governance floors,
metabolic workflows, tool schemas (input + output), vault, and telemetry.

Register via register_resources(mcp).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.apps import AppConfig, ResourceCSP

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VAULT_PATH = Path(__file__).resolve().parent.parent.parent / "core" / "vault"


def _read_vault_entries(n: int = 5) -> list[dict[str, Any]]:
    if not _VAULT_PATH.exists():
        return []
    entries: list[dict[str, Any]] = []
    for f in sorted(_VAULT_PATH.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:n]:
        try:
            raw = json.loads(f.read_text(encoding="utf-8"))
            entries.append(
                {
                    "ledger_id": raw.get("ledger_id"),
                    "session_id": raw.get("session_id"),
                    "verdict": raw.get("verdict"),
                    "timestamp": raw.get("timestamp"),
                    "hash": raw.get("hash"),
                }
            )
        except Exception:
            pass
    return entries


# ---------------------------------------------------------------------------
# Static data
# ---------------------------------------------------------------------------

_TOOLS = [
    {
        "stage": "000",
        "name": "init_anchor_state",
        "canonical": "anchor_session",
        "lane": "Delta",
        "label": "000 INIT - Session anchor",
        "role": "Governed session bootstrap",
    },
    {
        "stage": "111",
        "name": "integrate_analyze_reflect",
        "canonical": "reason_mind",
        "lane": "Delta",
        "label": "111 FRAME - Integrate, analyze, reflect",
        "role": "Problem framing & integrative analysis",
    },
    {
        "stage": "333",
        "name": "reason_mind_synthesis",
        "canonical": "reason_mind",
        "lane": "Delta",
        "label": "333 REASON - Mind synthesis",
        "role": "Multi-step reasoning + Eureka synthesis",
    },
    {
        "stage": "444",
        "name": "metabolic_loop_router",
        "canonical": "metabolic_loop",
        "lane": "ALL",
        "label": "444 ROUTE - Metabolic loop router",
        "role": "Full 000-999 pipeline orchestrator",
    },
    {
        "stage": "555",
        "name": "vector_memory_store",
        "canonical": "vector_memory",
        "lane": "Omega",
        "label": "555 MEMORY - Vector memory store",
        "role": "BBB associative vector memory",
    },
    {
        "stage": "666A",
        "name": "assess_heart_impact",
        "canonical": "simulate_heart",
        "lane": "Omega",
        "label": "666A HEART - Impact assessment",
        "role": "Empathy & ethical safety engine",
    },
    {
        "stage": "666B",
        "name": "critique_thought_audit",
        "canonical": "critique_thought",
        "lane": "Omega",
        "label": "666B CRITIQUE - Thought audit",
        "role": "Adversarial internal thought audit",
    },
    {
        "stage": "777",
        "name": "quantum_eureka_forge",
        "canonical": "eureka_forge",
        "lane": "Psi",
        "label": "777 FORGE - Eureka proposal",
        "role": "Sandboxed discovery actuator",
    },
    {
        "stage": "888",
        "name": "apex_judge_verdict",
        "canonical": "apex_judge",
        "lane": "Psi",
        "label": "888 JUDGE - APEX verdict",
        "role": "Constitutional judgment verdict",
    },
    {
        "stage": "999",
        "name": "seal_vault_commit",
        "canonical": "seal_vault",
        "lane": "Psi",
        "label": "999 SEAL - Vault commit",
        "role": "Immutable VAULT999 ledger sealing",
    },
]

APEX_CORE_TOOLS: tuple[dict[str, str], ...] = tuple(_TOOLS)


def apex_tools_html_rows() -> str:
    """Return HTML table rows for the canonical 10-tool APEX-G stack."""
    rows: list[str] = []
    for tool in APEX_CORE_TOOLS:
        rows.append(
            (
                f'<tr><td><span class="stage">{tool["stage"]}</span></td>'
                f'<td class="name">{tool["name"]}</td>'
                f'<td class="name">{tool["canonical"]}</td>'
                f'<td class="role">{tool["label"]}</td>'
                f'<td class="role">{tool["role"]}</td></tr>'
            )
        )
    return "\n".join(rows)


def apex_tools_markdown_table() -> str:
    """Return the canonical 10-tool APEX-G stack as a Markdown table."""
    header = (
        "| Stage | Runtime Tool | Canonical Handle | Label | Role |\n"
        "|-------|--------------|------------------|-------|------|"
    )
    rows = [
        (
            f'| {tool["stage"]} | {tool["name"]} | {tool["canonical"]} | '
            f'{tool["label"]} | {tool["role"]} |'
        )
        for tool in APEX_CORE_TOOLS
    ]
    return "\n".join([header, *rows])

_FLOORS = [
    {
        "id": "F1",
        "name": "Amanah",
        "type": "Hard",
        "engine": "ASI",
        "threshold": "LOCK",
        "check": "Reversible? Within mandate?",
    },
    {
        "id": "F2",
        "name": "Truth",
        "type": "Hard",
        "engine": "AGI",
        "threshold": "≥ 0.99",
        "check": "Factually accurate?",
    },
    {
        "id": "F3",
        "name": "Tri-Witness",
        "type": "Mirror",
        "engine": "—",
        "threshold": "≥ 0.95",
        "check": "Human·AI·Earth consensus",
    },
    {
        "id": "F4",
        "name": "ΔS Clarity",
        "type": "Hard",
        "engine": "AGI",
        "threshold": "≤ 0",
        "check": "Reduces confusion?",
    },
    {
        "id": "F5",
        "name": "Peace²",
        "type": "Soft",
        "engine": "ASI",
        "threshold": "≥ 1.0",
        "check": "Non-destructive?",
    },
    {
        "id": "F6",
        "name": "kr Empathy",
        "type": "Soft",
        "engine": "ASI",
        "threshold": "≥ 0.70",
        "check": "Serves weakest stakeholder?",
    },
    {
        "id": "F7",
        "name": "Omega Humility",
        "type": "Hard",
        "engine": "AGI",
        "threshold": "0.03-0.05",
        "check": "States uncertainty?",
    },
    {
        "id": "F8",
        "name": "G Genius",
        "type": "Mirror",
        "engine": "—",
        "threshold": "≥ 0.80",
        "check": "A×P×X×E² coherence",
    },
    {
        "id": "F9",
        "name": "C_dark",
        "type": "Hard",
        "engine": "ASI",
        "threshold": "< 0.30",
        "check": "Dark cleverness contained?",
    },
    {
        "id": "F10",
        "name": "Ontology",
        "type": "Wall",
        "engine": "—",
        "threshold": "LOCK",
        "check": "No consciousness/soul claims",
    },
    {
        "id": "F11",
        "name": "Command Auth",
        "type": "Hard",
        "engine": "ASI",
        "threshold": "LOCK",
        "check": "Nonce-verified identity?",
    },
    {
        "id": "F12",
        "name": "Injection",
        "type": "Wall",
        "engine": "—",
        "threshold": "< 0.85",
        "check": "Block adversarial control",
    },
    {
        "id": "F13",
        "name": "Sovereign",
        "type": "Veto",
        "engine": "APEX",
        "threshold": "HUMAN",
        "check": "Human final authority?",
    },
]

_WORKFLOWS = [
    {"name": "default_low_risk", "path": ["000", "111", "333", "666B", "888", "999"]},
    {
        "name": "high_risk",
        "path": ["000", "111", "333", "555", "666A", "666B", "777", "888", "999"],
    },
    {"name": "memory_recall", "path": ["000", "555", "333", "888", "999"]},
    {"name": "ethical_review", "path": ["000", "666A", "666B", "888", "999"]},
    {"name": "discovery_only", "path": ["000", "111", "333", "777", "888", "999"]},
]

# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def register_resources(mcp: FastMCP) -> None:
    """Wire all arifOS resources onto *mcp*."""

    # ------------------------------------------------------------------
    # Canon resources
    # ------------------------------------------------------------------

    @mcp.resource("canon://index")
    def canon_index() -> str:
        """High-level arifOS canon map: tools, floors, and resource index."""
        return json.dumps(
            {
                "version": "2026.03.08",
                "motto": "DITEMPA BUKAN DIBERI",
                "organs": ["AGI", "ASI", "APEX", "VAULT", "INIT", "UnifiedMemory"],
                "tool_count": len(_TOOLS),
                "floor_count": len(_FLOORS),
                "resources": [
                    "canon://index",
                    "canon://tools",
                    "canon://floors",
                    "canon://metabolic-loop",
                    "governance://law",
                    "eval://metabolic-workflows",
                    "eval://floors-thresholds",
                    "schema://tools/input",
                    "schema://tools/output",
                    "vault://latest",
                    "telemetry://summary",
                ],
            },
            ensure_ascii=False,
        )

    @mcp.resource("canon://tools")
    def canon_tools() -> str:
        """APEX-G 10-tool stack overview (stage, name, canonical name, role)."""
        return json.dumps({"tools": _TOOLS}, ensure_ascii=False)

    @mcp.resource("canon://floors")
    def canon_floors() -> str:
        """arifOS 13 constitutional floors (F1-F13) with types and thresholds."""
        return json.dumps({"floors": _FLOORS}, ensure_ascii=False)

    @mcp.resource("canon://metabolic-loop")
    def canon_metabolic_loop() -> str:
        """Prose explanation of the 000 to 999 metabolic loop."""
        return (
            "# arifOS Metabolic Loop\n\n"
            "The loop is a ten-stage constitutional pipeline:\n\n"
            f"{apex_tools_markdown_table()}\n\n"
            "Every action passes F12 then F11 guards first, then AGI floors "
            "(F1,F2,F4,F7), then ASI floors (F5,F6,F9,F13), then Mirrors (F3,F8). "
            "Hard-floor failure: VOID. Soft-floor failure: PARTIAL (warn, proceed).\n\n"
            "Motto: DITEMPA BUKAN DIBERI — Forged, not given."
        )

    # ------------------------------------------------------------------
    # Governance resources
    # ------------------------------------------------------------------

    @mcp.resource("governance://law")
    def governance_law() -> str:
        """Core arifOS invariants: 13-floor law summary and verdict hierarchy."""
        return (
            "# arifOS Constitutional Law\n\n"
            "## Verdict Hierarchy\n"
            "SABAR > VOID > 888_HOLD > PARTIAL > SEAL\n\n"
            "## Hard Floors (fail -> VOID)\n"
            "F1 Amanah · F2 Truth >=0.99 · F4 dS<=0 · F7 Omega 0.03-0.05 · "
            "F9 C_dark<0.30 · F10 Ontology LOCK · F11 Command Auth LOCK · F12 Injection<0.85\n\n"
            "## Soft Floors (fail -> PARTIAL)\n"
            "F3 Tri-Witness >=0.95 · F5 Peace^2>=1.0 · F6 kr>=0.70 · F8 G>=0.80\n\n"
            "## Veto\n"
            "F13 Sovereign — Human final authority. Cannot be overridden.\n\n"
            "## Anti-Hantu\n"
            "Forbidden: 'I feel', 'I promise', 'I am conscious', 'I have a soul'.\n"
            "Allowed: 'This sounds significant', 'I am committed to helping you'.\n\n"
            "## 888_HOLD Triggers\n"
            "DB migrations · Production deployments · Credential handling · "
            "Mass file ops >10 files · Git history modification · Major dep upgrades."
        )

    # ------------------------------------------------------------------
    # Eval resources
    # ------------------------------------------------------------------

    @mcp.resource("eval://metabolic-workflows")
    def eval_workflows() -> str:
        """Standard 000-999 metabolic workflow recipes."""
        return json.dumps({"workflows": _WORKFLOWS}, ensure_ascii=False)

    @mcp.resource("eval://floors-thresholds")
    def eval_floors_thresholds() -> str:
        """Numeric thresholds for all 13 constitutional floors."""
        thresholds = {
            f["id"]: {"name": f["name"], "threshold": f["threshold"], "type": f["type"]}
            for f in _FLOORS
        }
        return json.dumps(thresholds, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Schema resources
    # ------------------------------------------------------------------

    @mcp.resource("schema://tools/input")
    def schema_tools_input() -> str:
        """Canonical JSON Schema input specs for all 10 arifOS tools."""
        schemas = {
            "init_anchor_state": {
                "required": ["intent"],
                "properties": {
                    "intent": {
                        "type": "object",
                        "required": ["query"],
                        "properties": {
                            "query": {"type": "string"},
                            "task_type": {
                                "type": "string",
                                "enum": [
                                    "ask",
                                    "analyze",
                                    "design",
                                    "decide",
                                    "audit",
                                    "execute",
                                    "unknown",
                                ],
                                "default": "unknown",
                            },
                            "domain": {"type": "string", "default": "general"},
                            "desired_output": {
                                "type": "string",
                                "enum": ["text", "json", "table", "code", "mixed"],
                                "default": "text",
                            },
                            "reversibility": {
                                "type": "string",
                                "enum": ["reversible", "mixed", "irreversible", "unknown"],
                                "default": "unknown",
                            },
                        },
                        "additionalProperties": False,
                    },
                    "math": {
                        "type": "object",
                        "properties": {
                            "akal": {"type": "number", "minimum": 0, "maximum": 1, "default": 0.6},
                            "present": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.8,
                            },
                            "energy": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.6,
                            },
                            "exploration": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.4,
                            },
                        },
                        "additionalProperties": False,
                    },
                    "governance": {
                        "type": "object",
                        "properties": {
                            "actor_id": {"type": "string", "default": "anonymous"},
                            "authority_level": {
                                "type": "string",
                                "enum": ["human", "agent", "system", "anonymous"],
                                "default": "anonymous",
                            },
                            "stakes_class": {
                                "type": "string",
                                "enum": ["A", "B", "C", "UNKNOWN"],
                                "default": "UNKNOWN",
                            },
                        },
                        "additionalProperties": False,
                    },
                },
                "additionalProperties": False,
            },
            "integrate_analyze_reflect": {
                "required": ["session_id", "query", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "query": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "max_subquestions": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 3,
                    },
                },
                "additionalProperties": False,
            },
            "reason_mind_synthesis": {
                "required": ["session_id", "query", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "query": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "reason_mode": {
                        "type": "string",
                        "enum": ["default", "strict_truth", "design_space", "edge_cases"],
                        "default": "default",
                    },
                    "max_steps": {"type": "integer", "minimum": 3, "maximum": 16, "default": 7},
                },
                "additionalProperties": False,
            },
            "metabolic_loop_router": {
                "required": ["query"],
                "properties": {
                    "query": {"type": "string"},
                    "context": {"type": "string", "default": ""},
                    "risk_tier": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "default": "medium",
                    },
                    "actor_id": {"type": "string", "default": "anonymous"},
                    "use_memory": {"type": "boolean", "default": True},
                    "use_heart": {"type": "boolean", "default": True},
                    "use_critique": {"type": "boolean", "default": True},
                    "allow_execution": {"type": "boolean", "default": False},
                    "debug": {"type": "boolean", "default": False},
                },
                "additionalProperties": False,
            },
            "vector_memory_store": {
                "required": ["session_id", "operation", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "operation": {
                        "type": "string",
                        "enum": ["store", "recall", "search", "forget"],
                    },
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "content": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None},
                    "memory_ids": {"type": "array", "items": {"type": "string"}},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 20, "default": 5},
                },
                "additionalProperties": False,
            },
            "assess_heart_impact": {
                "required": ["session_id", "scenario", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "scenario": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "heart_mode": {
                        "type": "string",
                        "enum": [
                            "general",
                            "vulnerable_stakeholder",
                            "conflict",
                            "self_harm",
                            "legal_risk",
                        ],
                        "default": "general",
                    },
                },
                "additionalProperties": False,
            },
            "critique_thought_audit": {
                "required": ["session_id", "thought_id", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "thought_id": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "critique_mode": {
                        "type": "string",
                        "enum": ["logic", "facts", "ethics", "clarity", "overall"],
                        "default": "overall",
                    },
                },
                "additionalProperties": False,
            },
            "quantum_eureka_forge": {
                "required": ["session_id", "intent", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "intent": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "eureka_type": {
                        "type": "string",
                        "enum": ["concept", "design", "eval_case", "governance_rule", "other"],
                        "default": "concept",
                    },
                    "materiality": {
                        "type": "string",
                        "enum": ["idea_only", "prototype", "ready_for_eval"],
                        "default": "idea_only",
                    },
                },
                "additionalProperties": False,
            },
            "apex_judge_verdict": {
                "required": ["session_id", "verdict_candidate", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "verdict_candidate": {
                        "type": "string",
                        "enum": ["SEAL", "PARTIAL", "SABAR", "VOID", "HOLD-888", "UNSET"],
                    },
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "reason_summary": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "seal_vault_commit": {
                "required": ["session_id", "auth_context"],
                "properties": {
                    "session_id": {"type": "string"},
                    "auth_context": {"type": "object", "additionalProperties": True},
                    "verdict": {
                        "type": "string",
                        "enum": ["SEAL", "PARTIAL", "SABAR", "VOID", "HOLD-888"],
                        "default": "SEAL",
                    },
                    "payload_ref": {"type": "string"},
                    "payload_hash": {"type": "string"},
                },
                "additionalProperties": False,
            },
        }
        return json.dumps(schemas, ensure_ascii=False)

    @mcp.resource("schema://tools/output")
    def schema_tools_output() -> str:
        """
        Canonical output schema: the RuntimeEnvelope returned by all 10 arifOS tools.
        Tool-specific payloads live inside the 'data' field.
        """
        schema = {
            "type": "object",
            "description": "RuntimeEnvelope — common return shape for all 10 arifOS tools.",
            "required": [
                "verdict",
                "stage",
                "session_id",
                "telemetry",
                "witness",
                "auth_context",
                "data",
            ],
            "properties": {
                "verdict": {
                    "type": "string",
                    "enum": ["SEAL", "PARTIAL", "SABAR", "VOID", "HOLD-888", "UNSET"],
                },
                "stage": {
                    "type": "string",
                    "enum": [
                        "000_INIT",
                        "111_MIND",
                        "333_MIND",
                        "444_ROUTER",
                        "555_MEMORY",
                        "666_HEART",
                        "777_APEX",
                        "888_JUDGE",
                        "999_VAULT",
                    ],
                },
                "session_id": {"type": "string"},
                "telemetry": {
                    "type": "object",
                    "required": ["dS", "peace2", "confidence", "verdict"],
                    "properties": {
                        "dS": {
                            "type": "number",
                            "description": "Entropy delta (dS <= 0 is healthy)",
                        },
                        "peace2": {
                            "type": "number",
                            "description": "Stability margin squared (>= 1.0)",
                        },
                        "confidence": {"type": "number", "description": "Confidence score 0-1"},
                        "verdict": {"type": "string", "description": "System health label"},
                    },
                },
                "witness": {
                    "type": "object",
                    "required": ["human", "ai", "earth"],
                    "properties": {
                        "human": {"type": "number", "minimum": 0, "maximum": 1},
                        "ai": {"type": "number", "minimum": 0, "maximum": 1},
                        "earth": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                },
                "auth_context": {
                    "type": "object",
                    "required": ["actor_id", "authority_level", "stakes_class"],
                    "properties": {
                        "actor_id": {"type": "string"},
                        "authority_level": {
                            "type": "string",
                            "enum": ["human", "agent", "system", "anonymous"],
                        },
                        "stakes_class": {
                            "type": "string",
                            "enum": ["A", "B", "C", "UNKNOWN"],
                        },
                    },
                },
                "data": {
                    "type": "object",
                    "description": "Tool-specific payload. Contents vary per stage.",
                },
            },
            "additionalProperties": False,
        }
        return json.dumps(schema, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Vault resources
    # ------------------------------------------------------------------

    @mcp.resource("vault://latest")
    def vault_latest() -> str:
        """Last 5 sealed VAULT999 entries (metadata only, payloads redacted)."""
        return json.dumps({"entries": _read_vault_entries(5)}, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Telemetry resources
    # ------------------------------------------------------------------

    @mcp.resource("telemetry://summary")
    def telemetry_summary() -> str:
        """
        Placeholder telemetry summary.
        Wire to arifosmcp.intelligence.core.thermo_budget for live metrics.
        """
        return json.dumps(
            {
                "note": "Wire to arifosmcp.intelligence.core.thermo_budget for live metrics.",
                "example_shape": {
                    "sessions": 0,
                    "avg_dS": None,
                    "avg_peace2": None,
                    "floor_warnings": {},
                },
            },
            ensure_ascii=False,
        )

    # ------------------------------------------------------------------
    # APEX Dashboard — MCP App (HTML iframe embedded in host client)
    # ------------------------------------------------------------------

    _DASHBOARD_HTML = (
        Path(__file__).resolve().parent.parent / "sites" / "apex-dashboard" / "dashboard.html"
    )

    @mcp.tool(app=AppConfig(resource_uri="ui://apex/dashboard.html"))
    def open_apex_dashboard(session_id: str = "global") -> str:
        """Open the APEX Sovereign Dashboard showing live governed-intelligence metrics.

        Opens the dashboard iframe in compatible MCP clients. The dashboard supports
        three modes: Static Demo (instant), Live Fetch (poll your MCP endpoint), and
        MCP Mode (receives pushed apex_output from tool calls via ext-apps SDK).

        To feed live data, enable Live Fetch in the dashboard and point it at your
        MCP server's /health or /mcp/ endpoint, or wire apex_judge to push results.
        """
        return json.dumps({
            "session_id": session_id,
            "dashboard": "ui://apex/dashboard.html",
            "note": "Dashboard open. Use Live Fetch mode or call apex_judge to push metrics.",
        })

    @mcp.resource(
        "ui://apex/dashboard.html",
        app=AppConfig(
            csp=ResourceCSP(
                resource_domains=[
                    "https://unpkg.com",
                    "https://fonts.googleapis.com",
                    "https://fonts.gstatic.com",
                ]
            )
        ),
    )
    def apex_dashboard_html() -> str:
        """APEX Sovereign Dashboard — self-contained HTML with React + Recharts."""
        if _DASHBOARD_HTML.exists():
            return _DASHBOARD_HTML.read_text(encoding="utf-8")
        return "<html><body>Dashboard not found.</body></html>"
