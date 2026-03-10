"""
arifosmcp/runtime/resources.py — arifOS FastMCP Resource Layer

Read-only, structured views of the arifOS canon, governance floors,
kernel workflows, tool schemas (input + output), vault, and telemetry.

Register via register_resources(mcp).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.server.apps import UI_EXTENSION_ID, AppConfig, ResourceCSP
from fastmcp.tools import ToolResult

from .public_registry import (
    RUNTIME_ENVELOPE_SCHEMA,
    public_resource_uris,
    public_tool_input_schemas,
    public_tool_specs,
    release_version,
)

try:
    from prefab_ui.app import PrefabApp
    from prefab_ui.components import (
        Card,
        CardContent,
        CardHeader,
        CardTitle,
        Column,
        DataTable,
        DataTableColumn,
        Heading,
        Metric,
        Row,
        Text,
    )

    PREFAB_AVAILABLE = True
except ImportError:
    PREFAB_AVAILABLE = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VAULT_CANDIDATES = (
    Path(__file__).resolve().parent.parent / "data" / "VAULT999",
    Path(__file__).resolve().parent.parent.parent / "VAULT999",
)
_DASHBOARD_HTML = (
    Path(__file__).resolve().parent.parent / "sites" / "apex-dashboard" / "dashboard.html"
)

APEX_DASHBOARD_URI = "ui://apex/dashboard-v2.html"
APEX_DASHBOARD_WIDGET_DOMAIN = os.getenv(
    "ARIFOS_WIDGET_DOMAIN",
    "https://arifosmcp.arif-fazil.com",
).rstrip("/")
APEX_DASHBOARD_CONNECT_DOMAINS = [
    os.getenv("ARIFOS_PUBLIC_BASE_URL", "https://arifosmcp.arif-fazil.com").rstrip("/"),
]
APEX_DASHBOARD_RESOURCE_DOMAINS = [
    "https://unpkg.com",
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
]
APEX_DASHBOARD_DEFAULT_ENDPOINT = f"{APEX_DASHBOARD_CONNECT_DOMAINS[0]}/api/governance-status"


def _read_vault_entries(n: int = 5) -> list[dict[str, Any]]:
    vault_path = next((path for path in _VAULT_CANDIDATES if path.exists()), None)
    if vault_path is None:
        return []
    entries: list[dict[str, Any]] = []
    for f in sorted(vault_path.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:n]:
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
        "name": spec.name,
        "role": spec.description,
        "type": spec.layer,
    }
    for spec in public_tool_specs()
]

APEX_CORE_TOOLS: tuple[dict[str, str], ...] = tuple(_TOOLS)


def apex_tools_html_rows() -> str:
    """Return HTML table rows for the canonical 7-tool arifOS stack."""
    rows: list[str] = []
    for tool in APEX_CORE_TOOLS:
        rows.append(
            f'<tr><td><span class="name">{tool["name"]}</span></td>'
            f'<td class="role">{tool["type"]}</td>'
            f'<td class="role">{tool["role"]}</td></tr>'
        )
    return "\n".join(rows)


def apex_tools_markdown_table() -> str:
    """Return the canonical 7-tool arifOS stack as a Markdown table."""
    header = "| Tool Name | Layer | Role |\n" "|-----------|-------|------|"
    rows = [(f'| {tool["name"]} | {tool["type"]} | {tool["role"]} |') for tool in APEX_CORE_TOOLS]
    return "\n".join([header, *rows])


def apex_dashboard_html_content() -> str:
    """Return the packaged HTML fallback for the dashboard resource."""
    if _DASHBOARD_HTML.exists():
        return _DASHBOARD_HTML.read_text(encoding="utf-8")
    return "<html><body>Dashboard not found.</body></html>"


def build_apex_dashboard_prefab(session_id: str = "global") -> Any | None:
    """Build the canonical Prefab dashboard view when Prefab is installed."""
    if not PREFAB_AVAILABLE:
        return None

    tool_rows = [
        {
            "name": tool["name"],
            "type": tool["type"],
            "role": tool["role"],
        }
        for tool in APEX_CORE_TOOLS
    ]

    with Column(gap=4, css_class="p-6") as view:
        Heading("APEX Sovereign Dashboard", level=2)
        Text("Unified Prefab app surface for the canonical runtime and legacy transport.")

        with Row(gap=4):
            Metric(
                label="Session",
                value=session_id,
                description="Governed session scope for this dashboard view.",
            )
            Metric(
                label="Core Tools",
                value=str(len(APEX_CORE_TOOLS)),
                description="Canonical APEX-G runtime tools.",
            )
            Metric(
                label="Floors",
                value=str(len(_FLOORS)),
                description="Constitutional enforcement floors.",
            )

        with Card():
            with CardHeader():
                CardTitle("Live Sources")
            with CardContent():
                Text(f"Default telemetry endpoint: {APEX_DASHBOARD_DEFAULT_ENDPOINT}")
                Text("Deployed static dashboard: /dashboard/")
                Text(f"Fallback HTML resource: {APEX_DASHBOARD_URI}")

        with DataTable(data=tool_rows):
            DataTableColumn("name", label="Tool Name")
            DataTableColumn("type", label="Layer")
            DataTableColumn("role", label="Role")

    return PrefabApp(
        view=view,
        state={
            "session_id": session_id,
            "default_endpoint": APEX_DASHBOARD_DEFAULT_ENDPOINT,
        },
    )


def build_open_apex_dashboard_result(
    session_id: str = "global",
    ctx: Context | None = None,
) -> ToolResult:
    """Return a unified dashboard tool result with Prefab when supported."""
    payload = {
        "session_id": session_id,
        "dashboard": APEX_DASHBOARD_URI,
        "default_endpoint": APEX_DASHBOARD_DEFAULT_ENDPOINT,
        "note": (
            "Unified Prefab dashboard ready. Use /api/governance-status for live telemetry "
            "or /dashboard/ for the deployed HTML surface."
        ),
    }
    content = [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]

    supports_prefab = bool(
        ctx and PREFAB_AVAILABLE and ctx.client_supports_extension(UI_EXTENSION_ID)
    )
    if not supports_prefab:
        return ToolResult(content=content)

    prefab_app = build_apex_dashboard_prefab(session_id=session_id)
    if prefab_app is None:
        return ToolResult(content=content)

    return ToolResult(content=content, structured_content=prefab_app)


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
                "version": release_version(),
                "motto": "DITEMPA BUKAN DIBERI",
                "organs": ["AGI", "ASI", "APEX", "VAULT", "INIT", "UnifiedMemory"],
                "tool_count": len(_TOOLS),
                "floor_count": len(_FLOORS),
                "resources": public_resource_uris(),
            },
            ensure_ascii=False,
        )

    @mcp.resource("canon://tools")
    def canon_tools() -> str:
        """Canonical public tool surface for the arifOS kernel and companion tools."""
        return json.dumps({"tools": _TOOLS}, ensure_ascii=False)

    @mcp.resource("canon://floors")
    def canon_floors() -> str:
        """arifOS 13 constitutional floors (F1-F13) with types and thresholds."""
        return json.dumps({"floors": _FLOORS}, ensure_ascii=False)

    @mcp.resource("canon://metabolic-loop")
    def canon_metabolic_loop() -> str:
        """Prose explanation of the public kernel flow and internal execution stages."""
        return (
            "# arifOS Kernel Flow\n\n"
            "Public execution flow:\n\n"
            "User -> arifOS.kernel -> judgment/verdict -> vault/trace\n\n"
            "Internal execution stages:\n\n"
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
        """Canonical JSON Schema input specs for the public arifOS tool surface."""
        return json.dumps(public_tool_input_schemas(), ensure_ascii=False)

    @mcp.resource("schema://tools/output")
    def schema_tools_output() -> str:
        """
        Canonical output schema: the RuntimeEnvelope returned by all public arifOS tools.
        Tool-specific payloads live inside the 'payload' field.
        """
        return json.dumps(RUNTIME_ENVELOPE_SCHEMA, ensure_ascii=False)

    @mcp.resource("schema://opex")
    def schema_opex() -> str:
        """OPEX schema for the epistemic intake layer on each tool response."""
        schema = {
            "schema": "OPEX v1.0",
            "description": (
                "Epistemic intake schema. Forces every tool response to declare: "
                "what it thinks (output_candidate), how confident (probability), "
                "why (evidence), and what it doesn't know (uncertainty)."
            ),
            "type": "object",
            "properties": {
                "output_candidate": {
                    "type": "string",
                    "description": "The proposed result or answer this tool is asserting.",
                },
                "probability": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "description": "Confidence in the output_candidate [0-1].",
                },
                "evidence": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Supporting evidence items grounding the output_candidate.",
                },
                "uncertainty": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Known unknowns, open questions, or boundary conditions.",
                },
            },
            "motto": "OPEX asks: What is true enough to say?",
        }
        return json.dumps(schema, ensure_ascii=False)

    @mcp.resource("schema://apex")
    def schema_apex() -> str:
        """APEX schema for the governance output layer on each tool response."""
        schema = {
            "schema": "APEX v1.0",
            "description": (
                "Governance output schema. Evaluates whether a tool result is "
                "fit to present, act on, or escalate. Derived automatically from "
                "RuntimeEnvelope telemetry + OPEX fields."
            ),
            "type": "object",
            "properties": {
                "akal": {
                    "type": "object",
                    "description": "Reasoning coherence check (F2 Truth + F4 Clarity).",
                    "properties": {
                        "coherence": {
                            "type": "string",
                            "enum": ["passes", "fails", "unknown"],
                        },
                        "contradiction": {"type": "string"},
                    },
                },
                "present": {
                    "type": "object",
                    "description": "Context relevance check (F1 Amanah mandate fit).",
                    "properties": {
                        "context_fit": {
                            "type": "string",
                            "enum": ["high", "medium", "low", "unknown"],
                        },
                        "user_intent_match": {
                            "type": "string",
                            "enum": ["high", "medium", "low", "unknown"],
                        },
                    },
                },
                "energy": {
                    "type": "object",
                    "description": "Cost/risk assessment (F5 Peace² stability).",
                    "properties": {
                        "effort_to_verify": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                        },
                        "entropy_if_wrong": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                        },
                    },
                },
                "exploration_amanah": {
                    "type": "object",
                    "description": "Discovery breadth + trust boundary (F9 C_dark + F7 Humility).",
                    "properties": {
                        "explored_alternatives": {"type": "integer", "minimum": 0},
                        "trust_boundary": {
                            "type": "string",
                            "enum": ["do not overclaim", "cleared"],
                        },
                    },
                },
                "judgment": {
                    "type": "object",
                    "description": "Final governance call (F13 Sovereign + F3 Tri-Witness).",
                    "properties": {
                        "recommendation": {
                            "type": "string",
                            "enum": ["Approved", "Partial", "Pause", "Hold", "Void"],
                        },
                        "human_decision_required": {"type": "boolean"},
                    },
                },
            },
            "verdict_mapping": {
                "SEAL": "Approved",
                "PARTIAL": "Partial",
                "SABAR": "Pause",
                "VOID": "Void",
                "HOLD-888": "Hold",
                "UNSET": "Pause",
            },
            "motto": "APEX asks: What is responsible enough to release?",
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
        Wire to arifosmcp.intelligence.tools.logic.thermo_budget for live metrics.
        """
        return json.dumps(
            {
                "note": "Wire to thermo_budget for live metrics.",
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

    @mcp.tool(app=AppConfig(resource_uri=APEX_DASHBOARD_URI))
    def open_apex_dashboard(ctx: Context, session_id: str = "global") -> ToolResult:
        """Open the APEX Sovereign Dashboard showing live governed-intelligence metrics.

        Prefers the unified Prefab app surface in compatible MCP hosts and exposes
        the packaged HTML dashboard as the stable fallback asset for deployment.
        """
        return build_open_apex_dashboard_result(session_id=session_id, ctx=ctx)

    @mcp.resource(
        APEX_DASHBOARD_URI,
        app=AppConfig(
            domain=APEX_DASHBOARD_WIDGET_DOMAIN,
            prefers_border=True,
            csp=ResourceCSP(
                connect_domains=APEX_DASHBOARD_CONNECT_DOMAINS,
                resource_domains=APEX_DASHBOARD_RESOURCE_DOMAINS,
            ),
        ),
    )
    def apex_dashboard_html() -> str:
        """APEX Sovereign Dashboard — self-contained HTML with React + Recharts."""
        return apex_dashboard_html_content()
