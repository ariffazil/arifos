from __future__ import annotations

from dataclasses import dataclass
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
    return "2026.03.14-VALIDATED"


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
        name="get_caller_status",
        stage="000_INIT",
        role="Onboarding Compass",
        layer="KERNEL",
        description="000_INIT: Highest-leverage diagnostic. Explains current session state, authority ladder, accessible tools, and the exact path to advance your session. Use this if you are 'blocked' or uncertain of your next step.",
        trinity="INIT",
        floors=(),
        input_schema={
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Optional session ID to inspect.",
                }
            },
        },
    ),
    ToolSpec(
        name="init_anchor",
        stage="000_INIT",
        role="Constitutional Airlock",
        layer="KERNEL",
        description="000_INIT: Establish a governed session and verify identity. Use this tool first to authorize a session and mint the auth_context required for subsequent governed tools. Enforces F11 (Command Auth), F12 (Injection Defense), and F13 (Sovereign Override).",
        trinity="INIT",
        floors=("F12",),
        input_schema={
            "type": "object",
            "required": ["raw_input"],
            "properties": {
                "raw_input": {
                    "type": "string",
                    "description": "Initialization query or identity declaration (e.g. 'I am arif').",
                }
            },
        },
    ),
    ToolSpec(
        name="init_anchor_state",
        stage="000_INIT",
        role="Constitutional Airlock (Legacy)",
        layer="KERNEL",
        description="Legacy alias for init_anchor.",
        trinity="INIT",
        floors=("F12",),
        input_schema={
            "type": "object",
            "anyOf": [
                {
                    "properties": {
                        "declared_name": {"type": "string"},
                        "human_approval": {"type": "boolean"},
                    }
                }
            ],
        },
    ),
    ToolSpec(
        name="revoke_anchor_state",
        stage="000_INIT",
        role="Kill Switch",
        layer="KERNEL",
        description="000_INIT: Immediately invalidate a governed session. Use this to explicitly end authority or terminate a session if a protocol breach is detected. Enforces F11 and F13.",
        trinity="INIT",
        floors=("F11", "F13"),
        input_schema={
            "type": "object",
            "required": ["session_id", "reason"],
            "properties": {
                "session_id": {"type": "string", "description": "The ID of the session to revoke."},
                "reason": {"type": "string", "description": "Justification for the revocation."},
            },
        },
    ),
    ToolSpec(
        name="register_tools",
        stage="000_INIT",
        role="Tool Surface Declaration",
        layer="KERNEL",
        description="000_INIT: Query the available tool surface and verify registration. Used by agents to understand which arifOS governance capabilities are currently exposed. Enforces F13.",
        trinity="INIT",
        floors=("F13",),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="arifOS_kernel",
        stage="444_ROUTER",
        role="Stage Conductor",
        layer="KERNEL",
        description="444_ROUTER: Canonical metabolic transition router. The primary entry point for arifOS governance. Routes complex queries through the full ΔΩΨ metabolic pipe (Reasoning, Memory, Ethics, Judgment). Use this when you need a single sovereign response vetted through all 13 floors.",
        trinity="ROUTER",
        floors=("F4",),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "The question or task to process."},
                "context": {"type": "string", "description": "Additional context for the query"},
                "auth_context": {
                    "type": "object",
                    "description": "Cryptographic authority context for high-risk actions.",
                    "additionalProperties": True,
                },
                "risk_tier": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Risk classification — higher tiers trigger stricter floor checks.",
                },
                "actor_id": {"type": "string", "description": "Identity of the requesting actor."},
                "use_memory": {
                    "type": "boolean",
                    "description": "Enable session memory retrieval and storage.",
                },
                "use_heart": {
                    "type": "boolean",
                    "description": "Enable ethical evaluation (666_HEART).",
                },
                "use_critique": {
                    "type": "boolean",
                    "description": "Enable self-critique engine (777_CRITIQUE).",
                },
                "allow_execution": {
                    "type": "boolean",
                    "description": "Allow material actions if permitted by ethical vetting.",
                },
                "debug": {
                    "type": "boolean",
                    "description": "Include detailed debug telemetry in response.",
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "Run full pipeline without writing to VAULT999.",
                },
                "requested_persona": {
                    "type": "string",
                    "enum": ["architect", "engineer", "auditor", "validator"],
                    "description": "Persona to assume for the response (F9-compliant role).",
                },
                "caller_context": {
                    "type": "object",
                    "description": "Advisory runtime context from calling agent. Server-governed — persona_id may be overridden.",
                    "additionalProperties": True,
                },
            },
        },
    ),
    ToolSpec(
        name="forge",
        stage="000_999",
        role="Full Pipeline Trigger",
        layer="KERNEL",
        description="000_999: One-shot metabolic pipeline trigger. Synthesizes a goal into a final, sealed action in a single call. Best for well-defined tasks where separate pipeline steps are unnecessary. Enforces all floors F1-F13.",
        trinity="ALL",
        floors=("F1-F13",),
        input_schema={
            "type": "object",
            "required": ["spec"],
            "properties": {
                "spec": {
                    "type": "string",
                    "description": "The design specification or goal to forge.",
                }
            },
        },
    ),
    # ─── AGI Δ MIND (6 tools) ───
    ToolSpec(
        name="agi_reason",
        stage="333_MIND",
        role="Governed Reasoning",
        layer="AGI Δ MIND",
        description="333_MIND: Perform first-principles structured reasoning. Explores hypotheses through conservative, exploratory, and adversarial paths. Use this for intellectual synthesis. Enforces F2 (Truth) and F4 (Clarity).",
        trinity="AGI Δ",
        floors=("F2", "F4", "F7"),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The reasoning prompt or problem statement.",
                }
            },
        },
    ),
    ToolSpec(
        name="agi_reflect",
        stage="333_INTEGRATE",
        role="Metacognitive Integration",
        layer="AGI Δ MIND",
        description="555_MEMORY: Perform metacognitive integration. Reflects on the current intelligence state and session context to ensure coherence before committing to a path. Enforces F4 and F7.",
        trinity="AGI Δ",
        floors=("F4", "F7"),
        input_schema={
            "type": "object",
            "required": ["topic"],
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The core topic or decision point to reflect upon.",
                }
            },
        },
    ),
    ToolSpec(
        name="reality_compass",
        stage="111_SENSE",
        role="Epistemic Intake",
        layer="AGI Δ MIND",
        description="111_SENSE: Ground claims in external reality. Use this to verify facts or fetch URL content BEFORE performing reasoning. Enforces F2 (Truth) fidelity.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["input"],
            "properties": {
                "input": {"type": "string", "description": "Fact string to verify or URL to fetch."}
            },
        },
    ),
    ToolSpec(
        name="reality_atlas",
        stage="222_GROUND",
        role="Evidence Map",
        layer="AGI Δ MIND",
        description="222_REALITY: Map evidence across multiple sources. Merges and queries EvidenceBundles to create a unified grounding context for complex investigations. Enforces F2 and F3.",
        trinity="AGI Δ",
        floors=("F2", "F3"),
        input_schema={
            "type": "object",
            "required": ["operation"],
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "The atlas operation (merge, query, or build).",
                }
            },
        },
    ),
    ToolSpec(
        name="search_reality",
        stage="111_SENSE",
        role="Web Acquisition",
        layer="AGI Δ MIND",
        description="111_SENSE: Direct web search for grounding facts. Fetches raw data from the external world to satisfy F2 (Truth) requirements for ungrounded claims.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {"query": {"type": "string", "description": "Search query terms."}},
        },
    ),
    ToolSpec(
        name="ingest_evidence",
        stage="111_SENSE",
        role="Evidence Normalization",
        layer="AGI Δ MIND",
        description="111_SENSE: Fetch and normalize evidence artifact. Extracts structured signals from a URL or File for injection into the reasoning pipeline. Enforces F2.",
        trinity="AGI Δ",
        floors=("F2",),
        input_schema={
            "type": "object",
            "required": ["url"],
            "properties": {"url": {"type": "string", "description": "Source URL or file path."}},
        },
    ),
    # ─── ASI Ω HEART (4 tools) ───
    ToolSpec(
        name="asi_critique",
        stage="555_ALIGN",
        role="Adversarial Critique",
        layer="ASI Ω HEART",
        description="666_HEART: Advanced adversarial critique and thought audit. Detects blind spots, uncertainty, and hidden assumptions before action. Enforces F7 (Humility) and F9 (Anti-Hantu/Shadow).",
        trinity="ASI Ω",
        floors=("F6", "F9"),
        input_schema={
            "type": "object",
            "required": ["draft_output"],
            "properties": {
                "draft_output": {
                    "type": "string",
                    "description": "The candidate thought or output to audit.",
                }
            },
        },
    ),
    ToolSpec(
        name="asi_simulate",
        stage="555_ALIGN",
        role="Consequence Prediction",
        layer="ASI Ω HEART",
        description="666_HEART: Simulate consequences and predict world-model outcomes. Use this to assess the downstream impact of a proposal before execution. Enforces F5 (Peace²) and F6 (Empathy).",
        trinity="ASI Ω",
        floors=("F5",),
        input_schema={
            "type": "object",
            "required": ["scenario"],
            "properties": {
                "scenario": {
                    "type": "string",
                    "description": "The scenario or action plan to simulate.",
                }
            },
        },
    ),
    ToolSpec(
        name="agentzero_engineer",
        stage="666_EXECUTE",
        role="Material Execution",
        layer="ASI Ω HAND",
        description="666_EXECUTE: Perform material system actions (code, shell, file ops). Requires valid session auth_context. Only for technical actions vetted by ASI levels. Enforces F11 (Authority).",
        trinity="ASI Ω",
        floors=(),
        input_schema={

            "type": "object",
            "required": ["task_description"],
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Specific engineering task (e.g. 'write script to X').",
                }
            },
        },
    ),
    ToolSpec(
        name="agentzero_memory_query",
        stage="444_MEMORY",
        role="Semantic Recall",
        layer="ASI Ω HAND",
        description="444_MEMORY: Recall semantic context from VAULT999. Retrieves past interactions and sealed truths to maintain session continuity and historical grounding. Enforces F2 and F7.",
        trinity="ASI Ω",
        floors=("F2", "F7"),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "Recall query or concept keywords."}
            },
        },
    ),
    # ─── APEX Ψ SOUL (7 tools) ───
    ToolSpec(
        name="apex_judge",
        stage="777_JUDGE",
        role="Verdict Engine",
        layer="APEX Ψ SOUL",
        description="888_JUDGE: Render a sovereign constitutional verdict (SEAL, VOID, HOLD, SABAR). Final authority for all candidate outputs. Enforces F3 (Tri-Witness) and F13 (Sovereign Override).",
        trinity="APEX Ψ",
        floors=("F3", "F13"),
        input_schema={
            "type": "object",
            "required": ["candidate_output"],
            "properties": {
                "candidate_output": {
                    "type": "string",
                    "description": "Final output candidate for judgment.",
                }
            },
        },
    ),
    ToolSpec(
        name="agentzero_validate",
        stage="777_JUDGE",
        role="Output Validation",
        layer="APEX Ψ SOUL",
        description="888_JUDGE: Validator-specific output judgment. Audits the technical and logical correctness of an Engineer's output before final sealing. Enforces F2 and F9.",
        trinity="APEX Ψ",
        floors=("F2", "F9"),
        input_schema={
            "type": "object",
            "required": ["input_to_validate"],
            "properties": {
                "input_to_validate": {
                    "type": "string",
                    "description": "The specific data or artifact to validate.",
                }
            },
        },
    ),
    ToolSpec(
        name="audit_rules",
        stage="888_FLOOR",
        role="Floor Inspection",
        layer="APEX Ψ SOUL",
        description="333_MIND: Inspect the live status and thresholds of all 13 constitutional floors (F1-F13). Provides transparency into current governance constraints. Enforces F1-F13.",
        trinity="APEX Ψ",
        floors=("F1-F13",),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="agentzero_armor_scan",
        stage="888_FLOOR",
        role="Injection Guard",
        layer="APEX Ψ SOUL",
        description="111_SENSE: Scan content for injection attacks and adversarial control. Used as a security guard (F12) before processing external or user input. Enforces F12.",
        trinity="APEX Ψ",
        floors=("F12",),
        input_schema={
            "type": "object",
            "required": ["content"],
            "properties": {
                "content": {"type": "string", "description": "Untrusted input to scan."}
            },
        },
    ),
    ToolSpec(
        name="agentzero_hold_check",
        stage="888_HOLD",
        role="Hold Monitor",
        layer="APEX Ψ SOUL",
        description="888_HOLD: Check status of a pending human escalation or sovereign hold. Used when a task requires manual intervention or ratification (F13). Enforces F13.",
        trinity="APEX Ψ",
        floors=("F13",),
        input_schema={
            "type": "object",
            "properties": {
                "hold_id": {"type": "string", "description": "Specific hold ID to query."}
            },
        },
    ),
    ToolSpec(
        name="check_vital",
        stage="888_VITALS",
        role="System Health",
        layer="APEX Ψ SOUL",
        description="000_INIT: System health and thermodynamic telemetry monitor. Reports real-time ΔS (Entropy), Peace², and Gödel Humility metrics. Essential for metabolic budgeting. Enforces F4, F5, F7.",
        trinity="APEX Ψ",
        floors=("F4", "F5", "F7"),
        input_schema={"type": "object", "properties": {}},
    ),
    ToolSpec(
        name="open_apex_dashboard",
        stage="888_OBSERVE",
        role="Live Observability",
        layer="APEX Ψ SOUL",
        description="888_JUDGE: Launch the browser-based APEX Dashboard. Provides high-fidelity visualization of constitutional traces, floor scores, and system vitals. Enforces F13.",
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
        description="999_VAULT: Commit a verified verdict and evidence to the immutable VAULT999 ledger. Mints a permanent hash-chain entry. Enforces F1 (Amanah) and F13 (Sovereign).",
        trinity="VAULT",
        floors=("F1", "F13"),
        input_schema={
            "type": "object",
            "required": ["verdict", "evidence"],
            "properties": {
                "verdict": {"type": "string", "description": "The final verdict code (SEAL/VOID)."},
                "evidence": {
                    "type": "string",
                    "description": "Justification or audit trail summary.",
                },
            },
        },
    ),
    ToolSpec(
        name="verify_vault_ledger",
        stage="999_ATTEST",
        role="Merkle Integrity",
        layer="VAULT999",
        description="999_VAULT: Verify the integrity of the VAULT999 Merkle chain. Detects unauthorized tampering or data corruption in the historical audit trail. Enforces F1.",
        trinity="VAULT",
        floors=("F1",),
        input_schema={
            "type": "object",
            "properties": {
                "full_scan": {
                    "type": "boolean",
                    "description": "Enable exhaustive ledger validation (deep scan).",
                }
            },
        },
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

PUBLIC_PROMPT_SPECS: tuple[PromptSpec, ...] = (
    # Formal prompts per SPEC.md Section 6.2
    PromptSpec("bootstrap_session", "init_anchor", "Guide identity establishment with raw_input containing identity declaration"),
    PromptSpec("explain_blocked_state", "arifOS_kernel", "Explain why blocked and how to recover"),
    PromptSpec("prepare_kernel_call", "arifOS_kernel", "Prepare governed execution with goal and risk_tier"),
    PromptSpec("summarize_constitutional_floors", "audit_rules", "Explain F1-F13 floors in context"),
)

PUBLIC_RESOURCE_SPECS: tuple[ResourceSpec, ...] = (
    # SPEC.md Section 6.1: Required Public Resources
    ResourceSpec("arifos://status/vitals", "Current health, capability map, degraded components"),
    ResourceSpec("arifos://governance/floors", "Constitutional F1-F13 thresholds and doctrine hooks"),
    ResourceSpec("arifos://bootstrap/guide", "Startup path, canonical sequence, example payloads"),
    ResourceSpec("arifos://contracts/tools", "Tool contract table: risk, auth, mutability"),
    ResourceSpec("arifos://caller/state", "Current caller state, allowed tools, blocked tools"),
    # Legacy aliases (maintained for compatibility)
    ResourceSpec("canon://contracts", "Tool Contract Table: Hierarchy and bootstrap requirements. [LEGACY: use arifos://contracts/tools]"),
    ResourceSpec("canon://states", "Session Ladder: State machine. [LEGACY: use arifos://bootstrap/guide]"),
    ResourceSpec("canon://index", "High-level arifOS canon map. [LEGACY: use arifos://status/vitals]"),
    ResourceSpec("schema://tools/input", "Canonical JSON Schema input specs for public tools."),
    ResourceSpec("schema://tools/output", "Canonical RuntimeEnvelope output schema."),
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


def public_tool_spec_by_name() -> dict[str, ToolSpec]:
    """Return mapping of tool name to ToolSpec for all public tools."""
    return {spec.name: spec for spec in PUBLIC_TOOL_SPECS}


# Backward compatibility alias
PUBLIC_TOOL_SPEC_BY_NAME = public_tool_spec_by_name()


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


def public_resource_specs() -> tuple[ResourceSpec, ...]:
    return PUBLIC_RESOURCE_SPECS


def public_prompt_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in PUBLIC_PROMPT_SPECS)


def public_prompt_specs() -> tuple[PromptSpec, ...]:
    return PUBLIC_PROMPT_SPECS


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
