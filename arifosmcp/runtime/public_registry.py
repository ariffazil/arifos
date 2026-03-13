from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import tomllib

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = ROOT / "pyproject.toml"
DEFAULT_PUBLIC_BASE_URL = "https://arifosmcp.arif-fazil.com"
DEFAULT_DOCS_URL = "https://arifos.arif-fazil.com"
DEFAULT_REPOSITORY_URL = "https://github.com/ariffazil/arifosmcp"
DEFAULT_STDIO_COMMAND = "python -m arifosmcp.runtime stdio"
DEFAULT_HTTP_PATH = "/mcp"
MCP_SERVER_NAME = "io.github.ariffazil/arifos-mcp"
MCP_SERVER_TITLE = "arifOS Sovereign Governance MCP"
MCP_PROTOCOL_VERSION = "2025-11-25"
PUBLIC_PROFILE_ALIASES = {"", "public", "chatgpt", "agnostic_public"}
INTERNAL_PROFILE_ALIASES = {"internal", "full"}


@dataclass(frozen=True)
class ToolSpec:
    name: str
    stage: str
    role: str
    layer: str
    description: str
    trinity: str
    floors: tuple[str, ...]
    input_schema: dict[str, Any]
    readonly: bool = False


@dataclass(frozen=True)
class PromptSpec:
    name: str
    target_tool: str
    description: str


@dataclass(frozen=True)
class ResourceSpec:
    uri: str
    description: str


@dataclass(frozen=True)
class CompatibilitySpec:
    legacy_name: str
    public_route: str
    status: str
    notes: str


def _profile_label(profile: str) -> str:
    normalized = profile.strip().lower() or "public"
    if normalized in PUBLIC_PROFILE_ALIASES:
        return "public"
    if normalized in INTERNAL_PROFILE_ALIASES:
        return "internal"
    return normalized


def normalize_tool_profile(profile: str) -> str:
    return _profile_label(profile)


def is_public_profile(profile: str) -> bool:
    return _profile_label(profile) == "public"


@lru_cache(maxsize=1)
def _read_pyproject() -> dict[str, Any]:
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


def project_version() -> str:
    return str(_read_pyproject()["project"]["version"])


def normalize_release_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) < 3:
        return version
    year, month, day, *rest = parts
    if year.isdigit() and month.isdigit() and day.isdigit() and len(year) == 4:
        normalized = f"{year}.{int(month):02d}.{int(day):02d}"
        return ".".join([normalized, *rest]) if rest else normalized
    return version


def release_version() -> str:
    return normalize_release_version(project_version())


def release_version_label() -> str:
    return "2026.03.13-FORGED"


def release_version_compact() -> str:
    return release_version().replace(".", "")


def fastmcp_dependency() -> str:
    for dep in _read_pyproject()["project"]["dependencies"]:
        if dep.startswith("fastmcp"):
            return dep
    return "fastmcp"


PUBLIC_TOOL_SPECS: tuple[ToolSpec, ...] = (
    # ─── KERNEL LAYER (5 tools) ───
    ToolSpec(
        name="init_anchor",
        stage="000_INIT",
        role="Constitutional Airlock",
        layer="KERNEL",
        description="Initialize session jurisdiction and identity verification.",
        trinity="INIT",
        floors=("F11", "F12", "F13"),
        input_schema={
            "type": "object",
            "required": ["raw_input"],
            "properties": {"raw_input": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="revoke_anchor_state",
        stage="000_INIT",
        role="Kill Switch",
        layer="KERNEL",
        description="Invalidate a governed session immediately.",
        trinity="INIT",
        floors=("F11", "F13"),
        input_schema={
            "type": "object",
            "required": ["session_id", "reason"],
            "properties": {"session_id": {"type": "string"}, "reason": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="register_tools",
        stage="000_INIT",
        role="Tool Surface Declaration",
        layer="KERNEL",
        description="Declare and verify tool surface at boot.",
        trinity="INIT",
        floors=("F13",),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="metabolic_loop_router",
        stage="444_ROUTER",
        role="Stage Conductor",
        layer="KERNEL",
        description="Routes ΔΩΨ transitions through the pipeline.",
        trinity="ROUTER",
        floors=("F4",),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {"query": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="forge",
        stage="000_999",
        role="Full Pipeline Trigger",
        layer="KERNEL",
        description="Triggers the full INIT → SEAL pipeline in one call.",
        trinity="ALL",
        floors=("F1-F13",),
        input_schema={
            "type": "object",
            "required": ["spec"],
            "properties": {"spec": {"type": "string"}},
        },
    ),
    # ─── AGI Δ MIND (6 tools) ───
    ToolSpec(
        name="agi_reason",
        stage="111_SENSE",
        role="Governed Reasoning",
        layer="AGI Δ MIND",
        description="Structured reasoning step under F2/F4/F7.",
        trinity="AGI Δ",
        floors=("F2", "F4", "F7"),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {"query": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="agi_reflect",
        stage="333_INTEGRATE",
        role="Metacognitive Integration",
        layer="AGI Δ MIND",
        description="Checks own output and builds session context.",
        trinity="AGI Δ",
        floors=("F4", "F7"),
        input_schema={
            "type": "object",
            "required": ["topic"],
            "properties": {"topic": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="reality_compass",
        stage="222_GROUND",
        role="Epistemic Intake",
        layer="AGI Δ MIND",
        description="Grounds claims before reasoning via reality fetch.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["input"],
            "properties": {"input": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="reality_atlas",
        stage="222_GROUND",
        role="Evidence Map",
        layer="AGI Δ MIND",
        description="Structured evidence map across multiple sources.",
        trinity="AGI Δ",
        floors=("F2", "F3"),
        input_schema={
            "type": "object",
            "required": ["operation"],
            "properties": {"operation": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="search_reality",
        stage="222_GROUND",
        role="Web Acquisition",
        layer="AGI Δ MIND",
        description="Live web search for raw reality acquisition.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {"query": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="ingest_evidence",
        stage="222_GROUND",
        role="Evidence Normalization",
        layer="AGI Δ MIND",
        description="URL/File → Normalized evidence artifact.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["url"],
            "properties": {"url": {"type": "string"}},
        },
    ),
    # ─── ASI Ω HEART (4 tools) ───
    ToolSpec(
        name="asi_critique",
        stage="555_ALIGN",
        role="Adversarial Critique",
        layer="ASI Ω HEART",
        description="Safety and maruah check before action.",
        trinity="ASI Ω",
        floors=("F6", "F9"),
        input_schema={
            "type": "object",
            "required": ["draft_output"],
            "properties": {"draft_output": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="asi_simulate",
        stage="555_ALIGN",
        role="Consequence Prediction",
        layer="ASI Ω HEART",
        description="World model consequence simulation before action.",
        trinity="ASI Ω",
        floors=("F5",),
        input_schema={
            "type": "object",
            "required": ["scenario"],
            "properties": {"scenario": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="agentzero_engineer",
        stage="666_EXECUTE",
        role="Material Execution",
        layer="ASI Ω HAND",
        description="Code and env actions under F11 gate.",
        trinity="ASI Ω",
        floors=("F11",),
        input_schema={
            "type": "object",
            "required": ["task_description"],
            "properties": {"task_description": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="agentzero_memory_query",
        stage="444_MEMORY",
        role="Semantic Recall",
        layer="ASI Ω HAND",
        description="Constitutional semantic recall from Vault.",
        trinity="ASI Ω",
        floors=("F2", "F7"),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {"query": {"type": "string"}},
        },
    ),
    # ─── APEX Ψ SOUL (7 tools) ───
    ToolSpec(
        name="apex_judge",
        stage="777_JUDGE",
        role="Verdict Engine",
        layer="APEX Ψ SOUL",
        description="Tri-witness sovereign verdict engine.",
        trinity="APEX Ψ",
        floors=("F3", "F13"),
        input_schema={
            "type": "object",
            "required": ["candidate_output"],
            "properties": {"candidate_output": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="agentzero_validate",
        stage="777_JUDGE",
        role="Output Validation",
        layer="APEX Ψ SOUL",
        description="ValidatorAgent: ALLOW/HOLD/VOID judgment.",
        trinity="APEX Ψ",
        floors=("F2", "F9"),
        input_schema={
            "type": "object",
            "required": ["input_to_validate"],
            "properties": {"input_to_validate": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="audit_rules",
        stage="888_FLOOR",
        role="Floor Inspection",
        layer="APEX Ψ SOUL",
        description="F1–F13 live inspection and scoring.",
        trinity="APEX Ψ",
        floors=("F1-F13",),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="agentzero_armor_scan",
        stage="888_FLOOR",
        role="Injection Guard",
        layer="APEX Ψ SOUL",
        description="F12 PromptArmor injection pre-filtering.",
        trinity="APEX Ψ",
        floors=("F12",),
        input_schema={
            "type": "object",
            "required": ["content"],
            "properties": {"content": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="agentzero_hold_check",
        stage="888_HOLD",
        role="Hold Monitor",
        layer="APEX Ψ SOUL",
        description="888_HOLD registry and human escalation bus.",
        trinity="APEX Ψ",
        floors=("F13",),
        input_schema={"type": "object", "properties": {"hold_id": {"type": "string"}}},
    ),
    ToolSpec(
        name="check_vital",
        stage="888_VITALS",
        role="System Health",
        layer="APEX Ψ SOUL",
        description="System health: ΔS, peace², Ω₀ telemetry.",
        trinity="APEX Ψ",
        floors=("F4", "F5", "F7"),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="open_apex_dashboard",
        stage="888_OBSERVE",
        role="Live Observability",
        layer="APEX Ψ SOUL",
        description="Live floor scores and pipeline trace dashboard.",
        trinity="APEX Ψ",
        floors=("F13",),
        input_schema={"type": "object", "properties": {}},
    ),
    # ─── VAULT999 (2 tools) ───
    ToolSpec(
        name="vault_seal",
        stage="999_SEAL",
        role="Commit Decision",
        layer="VAULT999",
        description="Commit decision and telemetry to ledger.",
        trinity="VAULT",
        floors=("F1", "F13"),
        input_schema={
            "type": "object",
            "required": ["verdict", "evidence"],
            "properties": {"verdict": {"type": "string"}, "evidence": {"type": "string"}},
        },
    ),
    ToolSpec(
        name="verify_vault_ledger",
        stage="999_ATTEST",
        role="Merkle Integrity",
        layer="VAULT999",
        description="Merkle integrity check and tamper detection.",
        trinity="VAULT",
        floors=("F1",),
        input_schema={"type": "object", "properties": {"full_scan": {"type": "boolean"}}},
    ),
)

INTERNAL_STAGE_TOOL_NAMES: tuple[str, ...] = tuple(spec.name for spec in PUBLIC_TOOL_SPECS)

NON_CHATGPT_EXTRA_TOOL_NAMES: tuple[str, ...] = INTERNAL_STAGE_TOOL_NAMES

PUBLIC_COMPATIBILITY_SPECS: tuple[CompatibilitySpec, ...] = (
    CompatibilitySpec(
        legacy_name="arifOS_kernel",
        public_route="metabolic_loop_router",
        status="deprecated",
        notes="Unified kernel entrypoint.",
    ),
)

PUBLIC_PROMPT_SPECS: tuple[PromptSpec, ...] = tuple(
    PromptSpec(spec.name, spec.name, spec.description) for spec in PUBLIC_TOOL_SPECS
)

PUBLIC_RESOURCE_SPECS: tuple[ResourceSpec, ...] = (
    ResourceSpec("pns://shield", "PNS·SHIELD: Input sanitation status."),
    ResourceSpec("pns://search", "PNS·SEARCH: Web grounding facts."),
    ResourceSpec("pns://vision", "PNS·VISION: Multimodal perception."),
    ResourceSpec("pns://health", "PNS·HEALTH: Model stability metadata."),
    ResourceSpec("pns://floor", "PNS·FLOOR: Hallucination safety floor."),
    ResourceSpec("pns://orchestrate", "PNS·ORCHESTRATE: Tool routing mediation."),
    ResourceSpec("pns://redteam", "PNS·REDTEAM: Adversarial testing."),
    ResourceSpec("vault://999", "VAULT999: Sealed constitutional memory."),
    ResourceSpec("ledger://cooling", "Cooling Ledger: Ancestry chain."),
    ResourceSpec("canon://invariants", "ΔΩΨ constitutional invariants."),
)

RUNTIME_ENVELOPE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "RuntimeEnvelope (v1.0.0) — arifOS Double Helix common return shape.",
    "required": ["ok", "tool", "session_id", "stage", "verdict", "status", "metrics"],
    "properties": {
        "ok": {"type": "boolean"},
        "tool": {"type": "string"},
        "session_id": {"type": "string"},
        "stage": {"type": "string"},
        "verdict": {"type": "string"},
        "status": {"type": "string"},
        "metrics": {"type": "object"},
        "payload": {"type": "object"},
        "trace": {"type": "object"},
        "errors": {"type": "array", "items": {"type": "object"}},
        "meta": {"type": "object"},
    },
}


def public_tool_specs() -> tuple[ToolSpec, ...]:
    return PUBLIC_TOOL_SPECS


def public_tool_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in PUBLIC_TOOL_SPECS)


def internal_tool_specs() -> tuple[ToolSpec, ...]:
    return ()


def internal_tool_names() -> tuple[str, ...]:
    return ()


def legacy_internal_tool_specs() -> tuple[ToolSpec, ...]:
    return ()


def tool_names_for_profile(profile: str) -> tuple[str, ...]:
    return public_tool_names()


def deployment_tool_contract(profile: str) -> tuple[int, tuple[str, ...]]:
    names = tool_names_for_profile(profile)
    return len(names), names


def public_tool_input_schemas() -> dict[str, dict[str, Any]]:
    return {spec.name: spec.input_schema for spec in PUBLIC_TOOL_SPECS}


def public_tool_input_contracts() -> dict[str, dict[str, str]]:
    contracts: dict[str, dict[str, str]] = {}
    for spec in PUBLIC_TOOL_SPECS:
        schema = spec.input_schema
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        contracts[spec.name] = {
            field: str(properties.get(field, {}).get("type", "str")) for field in required
        }
    return contracts


def public_resource_uris() -> list[str]:
    return [spec.uri for spec in PUBLIC_RESOURCE_SPECS]


def public_prompt_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in PUBLIC_PROMPT_SPECS)


def public_compatibility_specs() -> tuple[CompatibilitySpec, ...]:
    return PUBLIC_COMPATIBILITY_SPECS


def build_mcp_manifest() -> dict[str, Any]:
    manifest_tools: dict[str, Any] = {}
    for spec in PUBLIC_TOOL_SPECS:
        manifest_tools[spec.name] = {
            "stage": spec.stage,
            "trinity": spec.trinity,
            "floors": list(spec.floors),
            "description": spec.description,
            "inputSchema": spec.input_schema,
        }

    return {
        "name": MCP_SERVER_NAME,
        "version": release_version_label(),
        "tools": manifest_tools,
        "resources": [
            {"uri": spec.uri, "description": spec.description} for spec in PUBLIC_RESOURCE_SPECS
        ],
    }


def build_server_json(public_base_url: str = DEFAULT_PUBLIC_BASE_URL) -> dict[str, Any]:
    """Build the canonical server.json manifest with all 24 tools."""
    return {
        "name": MCP_SERVER_NAME,
        "version": release_version_label(),
        "description": "Constitutional governance server — 24 canonical MCP tools with F1-F13 floor enforcement, metabolic routing, prompts, and resources.",
        "vendor": {"name": "Muhammad Arif bin Fazil", "url": "https://arif-fazil.com"},
        "license": "AGPL-3.0-only",
        "homepage": "https://github.com/ariffazil/arifosmcp",
        "repository": "https://github.com/ariffazil/arifosmcp",
        "capabilities": {
            "constitutional_floors": 13,
            "metabolic_routing": True,
            "vault999": "postgresql+redis+merkle",
            "vector_memory": "qdrant+bge-m3-1024dim",
            "prompts": len(PUBLIC_PROMPT_SPECS),
            "resources": len(PUBLIC_RESOURCE_SPECS),
        },
        "tools": [
            {"name": spec.name, "stage": spec.stage, "role": spec.role}
            for spec in PUBLIC_TOOL_SPECS
        ],
    }


def build_internal_server_json(public_base_url: str = DEFAULT_PUBLIC_BASE_URL) -> dict[str, Any]:
    """Build internal profile manifest with all 24 tools (public + internal aliases)."""
    server = build_server_json(public_base_url=public_base_url)
    server["name"] = f"{MCP_SERVER_NAME}.internal"
    server["capabilities"] = dict(server.get("capabilities", {}))
    server["capabilities"]["profile"] = "internal"
    return server


def build_mcp_discovery_json(public_base_url: str = DEFAULT_PUBLIC_BASE_URL) -> dict[str, Any]:
    """Build MCP discovery manifest for internal profile endpoints."""
    return build_internal_server_json(public_base_url=public_base_url)
