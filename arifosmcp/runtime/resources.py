"""
arifosmcp/runtime/resources.py — arifOS Double Helix Resources

Peripheral Nervous System (PNS) organs and Constitutional Ring assets.
Exposes operational grounding, health, and invariants as dynamic resources.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os
import json
from fastmcp import FastMCP
from .public_registry import (
    RUNTIME_ENVELOPE_SCHEMA,
    public_resource_uris,
    public_tool_specs,
    public_tool_input_schemas,
    release_version,
)


def apex_tools_html_rows() -> str:
    """Compatibility helper for legacy REST status pages."""
    rows: list[str] = []
    for spec in public_tool_specs():
        rows.append(
            f"<tr><td><span class='name'>{spec.name}</span></td>"
            f"<td class='role'>{spec.layer}</td>"
            f"<td class='role'>{spec.description}</td></tr>"
        )
    return "\n".join(rows)


def apex_tools_markdown_table() -> str:
    """Compatibility helper for markdown status summaries."""
    header = "| Tool Name | Layer | Role |\n|-----------|-------|------|"
    rows = [f"| {spec.name} | {spec.layer} | {spec.description} |" for spec in public_tool_specs()]
    return "\n".join([header, *rows])


def register_resources(mcp: FastMCP) -> None:
    """Wire the Double Helix resources (Inner Ring + PNS Outer Ring)."""

    # --- PNS OUTER RING (Dynamic Resources) ---

    @mcp.resource("pns://shield")
    def pns_shield() -> str:
        """PNS·SHIELD: Input sanitation and injection defense status."""
        return json.dumps(
            {
                "organ": "PNS·SHIELD",
                "role": "Entry Sanitizer",
                "status": "ACTIVE",
                "f12_threshold": 0.85,
            }
        )

    @mcp.resource("pns://search")
    def pns_search() -> str:
        """PNS·SEARCH: Web search grounding facts and reality feed."""
        return json.dumps({"organ": "PNS·SEARCH", "role": "Reality Acquisition", "status": "READY"})

    @mcp.resource("pns://vision")
    def pns_vision() -> str:
        """PNS·VISION: Multimodal perception status (Vision/PDF/Audio)."""
        return json.dumps(
            {
                "organ": "PNS·VISION",
                "role": "Sensory Perception",
                "status": "ACTIVE",
                "capabilities": ["OCR", "ImageSummary", "DocumentLayout"],
            }
        )

    @mcp.resource("pns://health")
    def pns_health() -> str:
        """PNS·HEALTH: Model health and stability metadata."""
        return json.dumps({"organ": "PNS·HEALTH", "role": "Stability Monitor", "status": "STABLE"})

    @mcp.resource("pns://floor")
    def pns_floor() -> str:
        """PNS·FLOOR: Hallucination safety floor metrics."""
        return json.dumps({"organ": "PNS·FLOOR", "role": "Semantic Grounding", "status": "ACTIVE"})

    @mcp.resource("pns://orchestrate")
    def pns_orchestrate() -> str:
        """PNS·ORCHESTRATE: Tool routing and action mediation."""
        return json.dumps(
            {"organ": "PNS·ORCHESTRATE", "role": "Action Mediator", "status": "READY"}
        )

    @mcp.resource("pns://redteam")
    def pns_redteam() -> str:
        """PNS·REDTEAM: Adversarial stress testing status."""
        return json.dumps(
            {"organ": "PNS·REDTEAM", "role": "Adversarial Stress", "status": "ACTIVE"}
        )

    # --- INNER RING & CANON ---

    @mcp.resource("vault://999")
    def vault_999() -> str:
        """VAULT999: Sealed constitutional memory access point."""
        return json.dumps({"organ": "VAULT", "role": "Immutable Ledger", "version": "v1.0-MERKLE"})

    @mcp.resource("ledger://cooling")
    def cooling_ledger() -> str:
        """Cooling Ledger: Hash-chain of previous session verdicts."""
        return json.dumps({"asset": "Cooling Ledger", "integrity": "VERIFIED"})

    @mcp.resource("canon://invariants")
    def canon_invariants() -> str:
        """ΔΩΨ constitutional invariants and thermodynamic laws."""
        return json.dumps({"delta": "ΔS ≤ 0", "omega": "Ω₀ ∈ [0.03, 0.05]", "psi": "G ≥ 0.80"})

    @mcp.resource("canon://floors")
    def canon_floors() -> str:
        """Static F1-F13 constitutional floor thresholds and execution order reference."""
        return json.dumps(
            {
                "structure": "9 Floors + 2 Mirrors + 2 Walls = 13 LAWS",
                "execution_order": "F12→F11 → AGI (F1,F2,F4,F7) → ASI (F5,F6,F9,F13) → Mirrors (F3,F8) → Ledger",
                "hard_fail": "VOID",
                "soft_fail": "PARTIAL",
                "floors": {
                    "F1":  {"name": "Amanah",      "threshold": "LOCK",      "type": "Hard",    "engine": "ASI",  "check": "Reversible? Within mandate?"},
                    "F2":  {"name": "Truth",        "threshold": "≥ 0.99",    "type": "Hard",    "engine": "AGI",  "check": "Factually accurate?"},
                    "F3":  {"name": "Tri-Witness",  "threshold": "≥ 0.95",    "type": "Mirror",  "engine": "APEX", "check": "External calibration (Human·AI·Earth)"},
                    "F4":  {"name": "ΔS Clarity",   "threshold": "≤ 0",       "type": "Hard",    "engine": "AGI",  "check": "Reduces confusion?"},
                    "F5":  {"name": "Peace²",       "threshold": "≥ 1.0",     "type": "Soft",    "engine": "ASI",  "check": "Non-destructive?"},
                    "F6":  {"name": "κᵣ Empathy",   "threshold": "≥ 0.70",    "type": "Soft",    "engine": "ASI",  "check": "Serves weakest stakeholder?"},
                    "F7":  {"name": "Ω₀ Humility",  "threshold": "0.03-0.05", "type": "Hard",    "engine": "AGI",  "check": "States uncertainty?"},
                    "F8":  {"name": "G Genius",     "threshold": "≥ 0.80",    "type": "Mirror",  "engine": "AGI",  "check": "Internal coherence (AxPxXxE2)"},
                    "F9":  {"name": "C_dark",       "threshold": "< 0.30",    "type": "Derived", "engine": "ASI",  "check": "Dark cleverness contained?"},
                    "F10": {"name": "Ontology",     "threshold": "LOCK",      "type": "Wall",    "engine": "APEX", "check": "No consciousness/soul claims"},
                    "F11": {"name": "Command Auth", "threshold": "LOCK",      "type": "Hard",    "engine": "ASI",  "check": "Nonce-verified identity?"},
                    "F12": {"name": "Injection",    "threshold": "< 0.85",    "type": "Wall",    "engine": "APEX", "check": "Block adversarial control"},
                    "F13": {"name": "Sovereign",    "threshold": "HUMAN",     "type": "Veto",    "engine": "APEX", "check": "Human final authority?"},
                },
            },
            ensure_ascii=False,
        )

    @mcp.resource("canon://index")
    def canon_index() -> str:
        """High-level arifOS canon map: tools, floors, and resource index."""
        return json.dumps(
            {
                "version": release_version(),
                "motto": "DITEMPA BUKAN DIBERI",
                "architecture": "Double Helix",
                "resources": public_resource_uris(),
            },
            ensure_ascii=False,
        )

    @mcp.resource("schema://tools/input")
    def schema_tools_input() -> str:
        """Canonical JSON Schema input specs for public tools."""
        return json.dumps(public_tool_input_schemas(), ensure_ascii=False)

    @mcp.resource("schema://tools/output")
    def schema_tools_output() -> str:
        """Canonical RuntimeEnvelope output schema."""
        return json.dumps(RUNTIME_ENVELOPE_SCHEMA, ensure_ascii=False)


def manifest_resources() -> list[str]:
    """Return list of all registered resource URIs."""
    return public_resource_uris()


async def read_resource_content(uri: str) -> str | None:
    """Read resource content by URI (Hardened 9 support)."""
    if uri not in public_resource_uris():
        return None
        
    if uri == "canon://index":
        return json.dumps({
            "version": release_version(),
            "motto": "DITEMPA BUKAN DIBERI",
            "resources": public_resource_uris()
        })
    return f"Content for {uri} (PNS/Canon Asset)"


def build_open_apex_dashboard_result(session_id: str = "global") -> ToolResult | None:
    """Return a ToolResult containing the APEX dashboard v2.1 redirect/HTML."""
    from fastmcp.tools import ToolResult
    dashboard_path = os.path.join(
        os.path.dirname(__file__), "..", "sites", "dashboard", "index.html"
    )
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            html = f.read()
        return ToolResult(content=[{"type": "text", "text": html}])
    return None
