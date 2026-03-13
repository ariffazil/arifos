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
from fastmcp.tools import ToolResult
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


def build_open_apex_dashboard_result(session_id: str = "global") -> ToolResult | None:
    """Return a ToolResult containing the APEX dashboard redirect/HTML."""
    # Find the HTML file relative to this file
    dashboard_path = os.path.join(
        os.path.dirname(__file__), "..", "sites", "apex-dashboard", "index.html"
    )
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            html = f.read()
        return ToolResult(content=[{"type": "text", "text": html}])
    return None
