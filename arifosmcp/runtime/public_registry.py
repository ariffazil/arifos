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
    return f"{release_version()}-SEAL"


def release_version_compact() -> str:
    return release_version().replace(".", "")


def fastmcp_dependency() -> str:
    for dep in _read_pyproject()["project"]["dependencies"]:
        if dep.startswith("fastmcp"):
            return dep
    return "fastmcp"


PUBLIC_TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec(
        name="arifOS_kernel",
        stage="444_ROUTER",
        role="Main orchestrator",
        layer="Execution",
        description=(
            "The arifOS Intelligence Kernel. Runs the full constitutional reasoning "
            "pipeline and should be the primary entrypoint for non-trivial tasks."
        ),
        trinity="ALL",
        floors=("F1-F13",),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "Task or question to evaluate."},
                "context": {"type": "string", "default": ""},
                "risk_tier": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "default": "medium",
                },
                "actor_id": {"type": "string", "default": "anonymous"},
                "auth_context": {
                    "type": "object",
                    "description": (
                        "Optional continuity envelope from init_anchor_state. "
                        "Required for anchored follow-up kernel calls."
                    ),
                },
                "use_memory": {"type": "boolean", "default": True},
                "use_heart": {"type": "boolean", "default": True},
                "use_critique": {"type": "boolean", "default": True},
                "allow_execution": {"type": "boolean", "default": False},
                "debug": {"type": "boolean", "default": False},
                "dry_run": {"type": "boolean", "default": False},
                "requested_persona": {
                    "type": "string",
                    "enum": ["architect", "engineer", "auditor", "validator"],
                },
            },
            "additionalProperties": False,
        },
    ),
    ToolSpec(
        name="search_reality",
        stage="111_SENSE",
        role="Grounding",
        layer="Cognitive Input",
        description="Find real-world sources and factual grounding before reasoning.",
        trinity="Δ Delta",
        floors=("F2", "F12"),
        input_schema={
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "Topic to ground with external facts."}
            },
            "additionalProperties": False,
        },
        readonly=True,
    ),
    ToolSpec(
        name="ingest_evidence",
        stage="222_REALITY",
        role="Ingestion",
        layer="Cognitive Input",
        description="Fetch or extract evidence from a URL, document, or file path.",
        trinity="Δ Delta",
        floors=("F2", "F11", "F12"),
        input_schema={
            "type": "object",
            "required": ["url"],
            "properties": {
                "url": {"type": "string", "description": "URL to ingest into governed context."}
            },
            "additionalProperties": False,
        },
        readonly=True,
    ),
    ToolSpec(
        name="session_memory",
        stage="555_MEMORY",
        role="Continuity",
        layer="Session",
        description="Store, retrieve, or forget session context and reasoning artifacts.",
        trinity="Ω Omega",
        floors=("F4", "F7", "F13"),
        input_schema={
            "type": "object",
            "required": ["session_id", "operation"],
            "properties": {
                "session_id": {"type": "string"},
                "operation": {
                    "type": "string",
                    "enum": ["store", "retrieve", "forget", "search"],
                },
                "content": {"type": "string"},
                "memory_ids": {"type": "array", "items": {"type": "string"}},
                "top_k": {"type": "integer", "minimum": 1, "default": 5},
            },
            "additionalProperties": False,
        },
    ),
    ToolSpec(
        name="audit_rules",
        stage="333_MIND",
        role="Governance",
        layer="Governance",
        description="Inspect the 13 constitutional floors and verify governance logic.",
        trinity="Δ Delta",
        floors=("F2", "F8", "F10"),
        input_schema={
            "type": "object",
            "properties": {"session_id": {"type": "string", "default": "global"}},
            "additionalProperties": False,
        },
        readonly=True,
    ),
    ToolSpec(
        name="check_vital",
        stage="000_INIT",
        role="Telemetry",
        layer="Governance",
        description="Read-only system health snapshot, reporting diagnostics and vitality signals.",
        trinity="Ω Omega",
        floors=("F4", "F5", "F7"),
        input_schema={
            "type": "object",
            "properties": {"session_id": {"type": "string", "default": "global"}},
            "additionalProperties": False,
        },
        readonly=True,
    ),
    ToolSpec(
        name="open_apex_dashboard",
        stage="888_JUDGE",
        role="Visualizer",
        layer="Observability",
        description="Open the APEX constitutional dashboard for live metrics and trace visibility.",
        trinity="Ψ Psi",
        floors=("F3", "F8", "F13"),
        input_schema={
            "type": "object",
            "properties": {"session_id": {"type": "string", "default": "global"}},
            "additionalProperties": False,
        },
        readonly=True,
    ),
)

NON_CHATGPT_EXTRA_TOOL_NAMES: tuple[str, ...] = (
    "init_anchor_state",
    "integrate_analyze_reflect",
    "reason_mind_synthesis",
    "assess_heart_impact",
    "critique_thought_audit",
    "quantum_eureka_forge",
    "apex_judge_verdict",
    "seal_vault_commit",
)

PUBLIC_PROMPT_SPECS: tuple[PromptSpec, ...] = (
    PromptSpec("arifos_kernel_prompt", "arifOS_kernel", "Route governed work to the kernel."),
    PromptSpec("search_reality_prompt", "search_reality", "Ground claims with external facts."),
    PromptSpec("ingest_evidence_prompt", "ingest_evidence", "Load a source into evidence context."),
    PromptSpec("session_memory_prompt", "session_memory", "Manage governed session continuity."),
    PromptSpec("audit_rules_prompt", "audit_rules", "Inspect constitutional floor logic."),
    PromptSpec("check_vital_prompt", "check_vital", "Read health and vitality telemetry."),
    PromptSpec(
        "open_apex_dashboard_prompt",
        "open_apex_dashboard",
        "Open the dashboard surface for live governed metrics.",
    ),
)

PUBLIC_RESOURCE_SPECS: tuple[ResourceSpec, ...] = (
    ResourceSpec("canon://index", "High-level arifOS canon map."),
    ResourceSpec("canon://tools", "Canonical public tool surface."),
    ResourceSpec("canon://floors", "arifOS 13 constitutional floors."),
    ResourceSpec("canon://metabolic-loop", "Public kernel flow and stages."),
    ResourceSpec("governance://law", "Verdict hierarchy and floor invariants."),
    ResourceSpec("eval://metabolic-workflows", "Standard 000-999 workflow recipes."),
    ResourceSpec("eval://floors-thresholds", "Numeric thresholds for floors."),
    ResourceSpec("schema://tools/input", "Canonical JSON Schema input specs for public tools."),
    ResourceSpec("schema://tools/output", "RuntimeEnvelope output schema."),
    ResourceSpec("schema://opex", "Epistemic intake schema."),
    ResourceSpec("schema://apex", "Governance output schema."),
    ResourceSpec("vault://latest", "Latest sealed VAULT entries."),
    ResourceSpec("telemetry://summary", "Governance telemetry summary."),
    ResourceSpec("runtime://capability-map", "Redacted capability and credential-class state."),
    ResourceSpec("ui://apex/dashboard-v2.html", "Packaged APEX dashboard asset."),
)

RUNTIME_ENVELOPE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "RuntimeEnvelope (v1.0.0) — common return shape for all public arifOS tools.",
    "required": [
        "ok",
        "tool",
        "session_id",
        "stage",
        "verdict",
        "status",
        "metrics",
        "trace",
        "authority",
        "payload",
        "errors",
        "meta",
    ],
    "properties": {
        "ok": {"type": "boolean", "description": "Transport success."},
        "tool": {"type": "string", "description": "Tool name."},
        "session_id": {"type": "string", "description": "Active session ID."},
        "stage": {"type": "string", "description": "Owning stage/organ."},
        "verdict": {
            "type": "string",
            "enum": ["SEAL", "PROVISIONAL", "PARTIAL", "SABAR", "HOLD", "HOLD_888", "VOID"],
        },
        "status": {"type": "string", "enum": ["SUCCESS", "ERROR", "TIMEOUT", "DRY_RUN"]},
        "metrics": {
            "type": "object",
            "properties": {
                "truth": {"type": "number"},
                "clarity_delta": {"type": "number"},
                "confidence": {"type": "number"},
                "peace": {"type": "number"},
                "vitality": {"type": "number"},
                "entropy_delta": {"type": "number"},
                "authority": {"type": "number"},
                "risk": {"type": "number"},
            },
        },
        "trace": {"type": "object", "description": "Stage path summary."},
        "authority": {
            "type": "object",
            "properties": {
                "actor_id": {"type": "string"},
                "level": {"type": "string"},
                "human_required": {"type": "boolean"},
                "approval_scope": {"type": "array", "items": {"type": "string"}},
                "auth_state": {"type": "string"},
            },
        },
        "payload": {"type": "object", "description": "Tool-specific result data."},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "message": {"type": "string"},
                    "stage": {"type": "string"},
                    "recoverable": {"type": "boolean"},
                },
            },
        },
        "meta": {
            "type": "object",
            "properties": {
                "schema_version": {"type": "string"},
                "timestamp": {"type": "string"},
                "debug": {"type": "boolean"},
                "dry_run": {"type": "boolean"},
            },
        },
    },
    "additionalProperties": True,
}


def public_tool_specs() -> tuple[ToolSpec, ...]:
    return PUBLIC_TOOL_SPECS


def public_tool_names() -> tuple[str, ...]:
    return tuple(spec.name for spec in PUBLIC_TOOL_SPECS)


def tool_names_for_profile(profile: str) -> tuple[str, ...]:
    normalized = profile.strip().lower() or "full"
    if normalized in {"chatgpt", "agnostic_public"}:
        return public_tool_names()
    return public_tool_names() + NON_CHATGPT_EXTRA_TOOL_NAMES


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


def build_server_json(public_base_url: str = DEFAULT_PUBLIC_BASE_URL) -> dict[str, Any]:
    base_url = public_base_url.rstrip("/")
    return {
        "name": MCP_SERVER_NAME,
        "version": release_version_label(),
        "description": (
            "Constitutional AI governance server — 7 canonical public MCP tools with "
            "F1-F13 floor enforcement, metabolic Stage 444 routing, prompts, and resources."
        ),
        "vendor": {"name": "Muhammad Arif bin Fazil", "url": "https://arif-fazil.com"},
        "license": "AGPL-3.0-only",
        "homepage": DEFAULT_REPOSITORY_URL,
        "repository": DEFAULT_REPOSITORY_URL,
        "transports": [
            {"type": "http", "url": f"{base_url}{DEFAULT_HTTP_PATH}"},
            {"type": "stdio", "command": DEFAULT_STDIO_COMMAND},
        ],
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


def build_mcp_manifest(public_base_url: str = DEFAULT_PUBLIC_BASE_URL) -> dict[str, Any]:
    base_url = public_base_url.rstrip("/")
    manifest_tools: dict[str, Any] = {}
    for spec in PUBLIC_TOOL_SPECS:
        entry: dict[str, Any] = {
            "stage": spec.stage,
            "trinity": spec.trinity,
            "floors": list(spec.floors),
            "description": spec.description,
            "inputSchema": spec.input_schema,
        }
        if spec.readonly:
            entry["readonly"] = True
        manifest_tools[spec.name] = entry

    return {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": MCP_SERVER_NAME,
        "version": release_version_label(),
        "title": MCP_SERVER_TITLE,
        "description": (
            "Constitutional AI governance server with a 7-tool public surface, 7 public prompts, "
            "14 public resources, Trinity engines (ΔΩΨ), and F1-F13 floor enforcement."
        ),
        "websiteUrl": DEFAULT_DOCS_URL,
        "vendor": {"name": "arifOS", "url": DEFAULT_DOCS_URL},
        "license": "AGPL-3.0-only",
        "repository": {"url": DEFAULT_REPOSITORY_URL, "source": "github"},
        "runtime": {
            "python": ">=3.12",
            "entrypoint": "python -m arifosmcp.runtime",
            "dependencies": [fastmcp_dependency()],
        },
        "deployment": {
            "default_transport": "http",
            "host": "0.0.0.0",
            "port": 8080,
            "path": DEFAULT_HTTP_PATH,
            "log_level": "INFO",
        },
        "packages": [
            {
                "registryType": "pypi",
                "identifier": "arifos",
                "version": release_version_label(),
                "transport": {"type": "stdio"},
            },
            {
                "registryType": "oci",
                "identifier": f"docker.io/arifazil/arifosmcp:forge-{release_version_compact()}",
                "transport": {"type": "streamable-http", "url": f"{base_url}{DEFAULT_HTTP_PATH}"},
            },
        ],
        "remotes": [
            {
                "type": "streamable-http",
                "url": f"{base_url}{DEFAULT_HTTP_PATH}",
                "authentication": {"type": "none"},
            },
        ],
        "tools": manifest_tools,
        "prompts": [
            {
                "name": spec.name,
                "targetTool": spec.target_tool,
                "description": spec.description,
            }
            for spec in PUBLIC_PROMPT_SPECS
        ],
        "resources": [
            {"uri": spec.uri, "description": spec.description} for spec in PUBLIC_RESOURCE_SPECS
        ],
        "schema": {
            "input": public_tool_input_schemas(),
            "output": RUNTIME_ENVELOPE_SCHEMA,
        },
        "trinity": {
            "delta": {
                "symbol": "Δ",
                "name": "Mind",
                "role": "AGI Reasoning",
                "stages": ["000", "111", "333"],
                "floors": ["F2", "F4", "F7", "F8"],
            },
            "omega": {
                "symbol": "Ω",
                "name": "Heart",
                "role": "ASI Safety",
                "stages": ["555", "666"],
                "floors": ["F5", "F6", "F9"],
            },
            "psi": {
                "symbol": "Ψ",
                "name": "Soul",
                "role": "APEX Judgment",
                "stages": ["777", "888", "999"],
                "floors": ["F1", "F3", "F10", "F11", "F12", "F13"],
            },
        },
    }
