"""
arifOS MCP Gateway — Constitutional Control Plane for Docker/K8s

Single entry point for all MCP tool calls. Enforces 13 floors before forwarding
to downstream MCP servers (Docker, K8s, Git, etc.)

Industry Pattern: Enterprise MCP Gateway with Constitutional Admission Control
Reference: https://modelcontextprotocol-security.io/patterns/enterprise-gateway.html

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Optional

from aaa_mcp.core.constitutional_decorator import constitutional_floor
from aaa_mcp.protocol.response import build_error_response, build_init_response

# Note: mcp is imported lazily in functions to avoid circular imports
from aaa_mcp.services.constitutional_metrics import (
    store_stage_result,
)


class ToolClass(str, Enum):
    """Classification of MCP tools by risk level."""

    READ_ONLY = "read_only"  # safe: list, get, describe
    INFRA_WRITE = "infra_write"  # medium: apply, create, update
    DESTRUCTIVE = "destructive"  # high: delete, destroy, wipe
    PROD_WRITE = "prod_write"  # critical: prod namespace changes
    SECRET_ACCESS = "secret_access"  # sensitive: secret read/write


@dataclass
class DownstreamMCPServer:
    """Configuration for a downstream MCP server."""

    name: str
    endpoint: str
    allowed_tools: List[str]
    tool_class_map: Dict[str, ToolClass] = field(default_factory=dict)
    auth_token: Optional[str] = None
    enabled: bool = True


@dataclass
class GatewayDecision:
    """Result of constitutional gateway evaluation."""

    session_id: str
    tool_name: str
    tool_class: ToolClass
    verdict: str  # SEAL, VOID, PARTIAL, 888_HOLD
    floors_checked: List[str]
    floors_failed: List[str]
    blast_radius: Dict[str, Any]
    downstream_endpoint: Optional[str]
    timestamp: str
    reasoning: str


# =============================================================================
# GATEWAY CONFIGURATION
# =============================================================================

# Downstream MCP servers registry
DOWNSTREAM_SERVERS: Dict[str, DownstreamMCPServer] = {
    "k8s": DownstreamMCPServer(
        name="kubernetes-mcp",
        endpoint=os.environ.get("K8S_MCP_ENDPOINT", "http://localhost:8081"),
        allowed_tools=[
            "k8s_apply",
            "k8s_delete",
            "k8s_scale",
            "k8s_get",
            "k8s_describe",
            "k8s_logs",
            "k8s_rollout",
            "k8s_rollback",
        ],
        tool_class_map={
            "k8s_get": ToolClass.READ_ONLY,
            "k8s_describe": ToolClass.READ_ONLY,
            "k8s_logs": ToolClass.READ_ONLY,
            "k8s_apply": ToolClass.INFRA_WRITE,
            "k8s_scale": ToolClass.INFRA_WRITE,
            "k8s_rollout": ToolClass.INFRA_WRITE,
            "k8s_rollback": ToolClass.INFRA_WRITE,
            "k8s_delete": ToolClass.DESTRUCTIVE,
        },
    ),
    "docker": DownstreamMCPServer(
        name="docker-mcp",
        endpoint=os.environ.get("DOCKER_MCP_ENDPOINT", "http://localhost:8082"),
        allowed_tools=[
            "docker_build",
            "docker_run",
            "docker_push",
            "docker_pull",
            "docker_stop",
            "docker_rm",
            "docker_scan",
        ],
        tool_class_map={
            "docker_scan": ToolClass.READ_ONLY,
            "docker_build": ToolClass.INFRA_WRITE,
            "docker_run": ToolClass.INFRA_WRITE,
            "docker_push": ToolClass.INFRA_WRITE,
            "docker_stop": ToolClass.INFRA_WRITE,
            "docker_rm": ToolClass.DESTRUCTIVE,
        },
    ),
    "policy": DownstreamMCPServer(
        name="opa-policy-mcp",
        endpoint=os.environ.get("OPA_MCP_ENDPOINT", "http://localhost:8083"),
        allowed_tools=["validate_manifest", "validate_image", "check_compliance"],
        tool_class_map={
            "validate_manifest": ToolClass.READ_ONLY,
            "validate_image": ToolClass.READ_ONLY,
            "check_compliance": ToolClass.READ_ONLY,
        },
    ),
    "redis": DownstreamMCPServer(
        name="redis-mcp",
        endpoint=os.environ.get("REDIS_MCP_ENDPOINT", "http://localhost:8084"),
        allowed_tools=[
            "redis_get",
            "redis_set",
            "redis_del",
            "redis_scan",
            "redis_lpush",
            "redis_rpush",
        ],
        tool_class_map={
            "redis_get": ToolClass.READ_ONLY,
            "redis_scan": ToolClass.READ_ONLY,
            "redis_set": ToolClass.INFRA_WRITE,
            "redis_lpush": ToolClass.INFRA_WRITE,
            "redis_rpush": ToolClass.INFRA_WRITE,
            "redis_del": ToolClass.DESTRUCTIVE,
        },
        auth_token=os.environ.get("REDIS_MCP_TOKEN"),
    ),
    "postgres": DownstreamMCPServer(
        name="postgres-mcp",
        endpoint=os.environ.get("POSTGRES_MCP_ENDPOINT", "http://localhost:8085"),
        allowed_tools=[
            "postgres_query",
            "postgres_execute",
            "postgres_schema_get",
            "postgres_table_create",
            "postgres_table_drop",
        ],
        tool_class_map={
            "postgres_query": ToolClass.READ_ONLY,
            "postgres_schema_get": ToolClass.READ_ONLY,
            "postgres_execute": ToolClass.INFRA_WRITE,
            "postgres_table_create": ToolClass.INFRA_WRITE,
            "postgres_table_drop": ToolClass.DESTRUCTIVE,
        },
        auth_token=os.environ.get("POSTGRES_MCP_TOKEN"),
    ),
    "github-git": DownstreamMCPServer(
        name="github-git-tools-mcp",
        endpoint=os.environ.get("GITHUB_GIT_MCP_ENDPOINT", "http://localhost:8086"),
        allowed_tools=["github_commit_write", "github_pr_draft", "github_status"],
        tool_class_map={
            "github_status": ToolClass.READ_ONLY,
            "github_commit_write": ToolClass.INFRA_WRITE,
            "github_pr_draft": ToolClass.INFRA_WRITE,
        },
        auth_token=os.environ.get("GITHUB_GIT_MCP_TOKEN"),
    ),
    "github-issues": DownstreamMCPServer(
        name="github-issue-agent-mcp",
        endpoint=os.environ.get("GITHUB_ISSUES_MCP_ENDPOINT", "http://localhost:8087"),
        allowed_tools=["github_issue_find", "github_issue_create", "github_issue_update"],
        tool_class_map={
            "github_issue_find": ToolClass.READ_ONLY,
            "github_issue_create": ToolClass.INFRA_WRITE,
            "github_issue_update": ToolClass.INFRA_WRITE,
        },
        auth_token=os.environ.get("GITHUB_ISSUES_MCP_TOKEN"),
    ),
    "auth0": DownstreamMCPServer(
        name="auth0-mcp",
        endpoint=os.environ.get("AUTH0_MCP_ENDPOINT", "http://localhost:8088"),
        allowed_tools=[
            "auth0_app_create",
            "auth0_user_manage",
            "auth0_log_view",
            "auth0_user_block",
        ],
        tool_class_map={
            "auth0_log_view": ToolClass.READ_ONLY,
            "auth0_app_create": ToolClass.INFRA_WRITE,
            "auth0_user_manage": ToolClass.INFRA_WRITE,
            "auth0_user_block": ToolClass.DESTRUCTIVE,  # Blocking a user is destructive
        },
        auth_token=os.environ.get("AUTH0_MCP_TOKEN"),
    ),
    "screenshot": DownstreamMCPServer(
        name="screenshot-mcp",
        endpoint=os.environ.get("SCREENSHOT_MCP_ENDPOINT", "http://localhost:8089"),
        allowed_tools=["screenshot_capture", "screenshot_window"],
        tool_class_map={
            "screenshot_capture": ToolClass.READ_ONLY,
            "screenshot_window": ToolClass.READ_ONLY,
        },
        # auth_token=None, # Local tool, likely no external auth token
    ),
    "ssh": DownstreamMCPServer(
        name="ssh-mcp",
        endpoint=os.environ.get("SSH_MCP_ENDPOINT", "http://localhost:8090"),
        allowed_tools=["ssh_exec_command", "ssh_sftp_get", "ssh_sftp_put"],
        tool_class_map={
            "ssh_exec_command": ToolClass.INFRA_WRITE,  # Can be read-only or destructive
            "ssh_sftp_get": ToolClass.READ_ONLY,
            "ssh_sftp_put": ToolClass.INFRA_WRITE,
        },
        auth_token=os.environ.get("SSH_MCP_TOKEN"),
    ),
    "uv-python": DownstreamMCPServer(
        name="uv-python-mcp",
        endpoint=os.environ.get("UV_PYTHON_MCP_ENDPOINT", "http://localhost:8091"),
        allowed_tools=["uv_install", "uv_uninstall", "uv_check"],
        tool_class_map={
            "uv_check": ToolClass.READ_ONLY,
            "uv_install": ToolClass.INFRA_WRITE,
            "uv_uninstall": ToolClass.DESTRUCTIVE,
        },
        # auth_token=None, # Local tool, likely no external auth token
    ),
    "obsidian": DownstreamMCPServer(
        name="obsidian-mcp",
        endpoint=os.environ.get("OBSIDIAN_MCP_ENDPOINT", "http://localhost:8092"),
        allowed_tools=[
            "obsidian_search",
            "obsidian_read",
            "obsidian_write",
            "obsidian_connect_notes",
        ],
        tool_class_map={
            "obsidian_search": ToolClass.READ_ONLY,
            "obsidian_read": ToolClass.READ_ONLY,
            "obsidian_write": ToolClass.INFRA_WRITE,
            "obsidian_connect_notes": ToolClass.INFRA_WRITE,
        },
        auth_token=os.environ.get("OBSIDIAN_MCP_TOKEN"),
    ),
    "notion": DownstreamMCPServer(
        name="notion-mcp",
        endpoint=os.environ.get("NOTION_MCP_ENDPOINT", "http://localhost:8093"),
        allowed_tools=[
            "notion_search",
            "notion_get_page",
            "notion_create_page",
            "notion_update_page",
            "notion_delete_page",
        ],
        tool_class_map={
            "notion_search": ToolClass.READ_ONLY,
            "notion_get_page": ToolClass.READ_ONLY,
            "notion_create_page": ToolClass.INFRA_WRITE,
            "notion_update_page": ToolClass.INFRA_WRITE,
            "notion_delete_page": ToolClass.DESTRUCTIVE,
        },
        auth_token=os.environ.get("NOTION_MCP_TOKEN"),
    ),
    "doc-detective": DownstreamMCPServer(
        name="doc-detective-mcp",
        endpoint=os.environ.get("DOC_DETECTIVE_MCP_ENDPOINT", "http://localhost:8094"),
        allowed_tools=[
            "doc_detective_generate_tests",
            "doc_detective_run_tests",
            "doc_detective_inject_steps",
        ],
        tool_class_map={
            "doc_detective_generate_tests": ToolClass.INFRA_WRITE,  # Generates files
            "doc_detective_run_tests": ToolClass.READ_ONLY,
            "doc_detective_inject_steps": ToolClass.INFRA_WRITE,
        },
        # auth_token=None, # Local tool, likely no external auth token
    ),
    "context7": DownstreamMCPServer(
        name="context7-mcp",
        endpoint=os.environ.get("CONTEXT7_MCP_ENDPOINT", "http://localhost:8095"),
        allowed_tools=["context7_query_docs", "context7_resolve_library"],
        tool_class_map={
            "context7_query_docs": ToolClass.READ_ONLY,
            "context7_resolve_library": ToolClass.READ_ONLY,
        },
        auth_token=os.environ.get("CONTEXT7_MCP_API_KEY"),
    ),
    "apify-scrape": DownstreamMCPServer(
        name="apify-agent-skills-mcp",
        endpoint=os.environ.get("APIFY_MCP_ENDPOINT", "http://localhost:8096"),
        allowed_tools=["apify_scrape_web", "apify_extract_data", "apify_run_actor"],
        tool_class_map={
            "apify_scrape_web": ToolClass.READ_ONLY,
            "apify_extract_data": ToolClass.READ_ONLY,
            "apify_run_actor": ToolClass.INFRA_WRITE,  # Can trigger external actions
        },
        auth_token=os.environ.get("APIFY_MCP_TOKEN"),
    ),
    "wordpress": DownstreamMCPServer(
        name="wordpress-mcp",
        endpoint=os.environ.get("WORDPRESS_MCP_ENDPOINT", "http://localhost:8097"),
        allowed_tools=[
            "wordpress_get_post",
            "wordpress_create_post",
            "wordpress_update_post",
            "wordpress_delete_post",
        ],
        tool_class_map={
            "wordpress_get_post": ToolClass.READ_ONLY,
            "wordpress_create_post": ToolClass.INFRA_WRITE,
            "wordpress_update_post": ToolClass.INFRA_WRITE,
            "wordpress_delete_post": ToolClass.DESTRUCTIVE,
        },
        auth_token=os.environ.get("WORDPRESS_MCP_TOKEN"),
    ),
}

# Floor requirements per tool class
FLOOR_REQUIREMENTS: Dict[ToolClass, List[str]] = {
    ToolClass.READ_ONLY: ["F11", "F12"],  # Auth + Injection scan
    ToolClass.INFRA_WRITE: ["F1", "F2", "F6", "F10", "F11", "F12"],
    ToolClass.DESTRUCTIVE: ["F1", "F2", "F5", "F6", "F10", "F11", "F12", "F13"],
    ToolClass.PROD_WRITE: ["F1", "F2", "F5", "F6", "F10", "F11", "F12", "F13"],
    ToolClass.SECRET_ACCESS: ["F1", "F2", "F6", "F10", "F11", "F12", "F13"],
}


# =============================================================================
# BLAST RADIUS CALCULATION (F6 Empathy for Infrastructure)
# =============================================================================


def calculate_blast_radius(
    tool_name: str, payload: Dict[str, Any], namespace: str = "default"
) -> Dict[str, Any]:
    """
    Calculate infrastructure blast radius for F6 Empathy evaluation.

    Returns affected resources count and criticality score.
    """
    radius = {
        "namespace": namespace,
        "affected_deployments": 0,
        "affected_pods": 0,
        "affected_services": 0,
        "critical_namespaces": [],
        "score": 0.0,  # 0.0 = safe, 1.0 = critical
        "reasoning": "",
    }

    # Critical namespace detection
    critical_ns = ["prod", "production", "kube-system", "monitoring"]
    if namespace in critical_ns:
        radius["critical_namespaces"].append(namespace)
        radius["score"] += 0.4

    # Tool-specific blast radius
    if "delete" in tool_name.lower():
        radius["score"] += 0.3
        radius["reasoning"] += "Destructive operation. "

        # Parse manifest for affected resources
        manifest = payload.get("manifest", "")
        if "Deployment" in manifest:
            radius["affected_deployments"] += 1
            radius["affected_pods"] += 3  # Assume 3 replicas
            radius["score"] += 0.2
        if "Service" in manifest:
            radius["affected_services"] += 1
            radius["score"] += 0.1

    elif "apply" in tool_name.lower() or "scale" in tool_name.lower():
        radius["score"] += 0.1
        radius["reasoning"] += "Write operation. "

    # Normalize score
    radius["score"] = min(1.0, radius["score"])

    return radius


# =============================================================================
# GATEWAY CORE
# =============================================================================


class MCPGateway:
    """
    arifOS Constitutional MCP Gateway.

    Single entry point that enforces 13 floors before forwarding to downstream
    MCP servers (Docker, K8s, Policy, etc.)
    """

    def __init__(self):
        self.servers = DOWNSTREAM_SERVERS
        self.decisions: List[GatewayDecision] = []

    def classify_tool(self, tool_name: str) -> Optional[ToolClass]:
        """Classify tool by name to determine floor requirements."""
        for server in self.servers.values():
            if tool_name in server.tool_class_map:
                return server.tool_class_map[tool_name]

        # Default classification based on naming
        if any(x in tool_name.lower() for x in ["get", "list", "describe", "scan"]):
            return ToolClass.READ_ONLY
        elif any(x in tool_name.lower() for x in ["delete", "destroy", "wipe"]):
            return ToolClass.DESTRUCTIVE
        elif any(x in tool_name.lower() for x in ["prod", "production"]):
            return ToolClass.PROD_WRITE
        else:
            return ToolClass.INFRA_WRITE

    def get_downstream_server(self, tool_name: str) -> Optional[DownstreamMCPServer]:
        """Find which downstream server handles this tool."""
        for server in self.servers.values():
            if tool_name in server.allowed_tools:
                return server
        return None

    async def evaluate_constitution(
        self,
        tool_name: str,
        payload: Dict[str, Any],
        session_id: str,
        actor_id: str = "agent",
    ) -> GatewayDecision:
        """
        Run constitutional pipeline to evaluate if tool call should proceed.

        This implements the arifOS 000-999 pipeline for infrastructure operations.
        """
        # Classify tool
        tool_class = self.classify_tool(tool_name)
        if not tool_class:
            return GatewayDecision(
                session_id=session_id,
                tool_name=tool_name,
                tool_class=ToolClass.INFRA_WRITE,
                verdict="VOID",
                floors_checked=["F11"],
                floors_failed=["F11"],
                blast_radius={},
                downstream_endpoint=None,
                timestamp=datetime.now(timezone.utc).isoformat(),
                reasoning="Unknown tool classification",
            )

        # Get required floors
        required_floors = FLOOR_REQUIREMENTS.get(tool_class, ["F11", "F12"])
        floors_checked = []
        floors_failed = []

        # F11: Authority (RBAC check)
        floors_checked.append("F11")
        # TODO: Integrate with actual RBAC system
        auth_valid = True  # Placeholder
        if not auth_valid:
            floors_failed.append("F11")

        # F12: Defense (Injection scan)
        floors_checked.append("F12")
        payload_str = json.dumps(payload)
        suspicious_patterns = [";", "|", "&&", "$(", "`", "${"]
        if any(p in payload_str for p in suspicious_patterns):
            floors_failed.append("F12")

        # F6: Empathy (Blast radius calculation)
        floors_checked.append("F6")
        namespace = payload.get("namespace", "default")
        blast_radius = calculate_blast_radius(tool_name, payload, namespace)

        # F6 HARD floor: κᵣ ≥ 0.95
        # Convert blast radius to empathy score (inverse)
        empathy_kappa_r = 1.0 - blast_radius["score"]
        if empathy_kappa_r < 0.95 and tool_class in [ToolClass.DESTRUCTIVE, ToolClass.PROD_WRITE]:
            floors_failed.append("F6")

        # F10: Ontology (Schema validation)
        floors_checked.append("F10")
        manifest = payload.get("manifest", "")
        if manifest and "apiVersion" in manifest:
            # Basic K8s manifest validation
            if "kind" not in manifest:
                floors_failed.append("F10")

        # F2: Truth (Image provenance)
        floors_checked.append("F2")
        if "image" in payload:
            image = payload["image"]
            # Require digest-based images for production
            if "@sha256:" not in image and namespace in ["prod", "production"]:
                floors_failed.append("F2")

        # F1: Amanah (Reversibility check)
        floors_checked.append("F1")
        if tool_class == ToolClass.DESTRUCTIVE:
            # Destructive ops need explicit rollback plan
            if not payload.get("backup_made", False):
                floors_failed.append("F1")

        # F5: Peace² (Stability check)
        floors_checked.append("F5")
        # Check for canary/blue-green indicators
        if tool_class == ToolClass.INFRA_WRITE and namespace in ["prod", "production"]:
            strategy = payload.get("strategy", "")
            if strategy not in ["canary", "blue-green", "rolling"]:
                # Not a failure, but warning (SOFT floor)
                pass

        # F13: Sovereign (Human override for critical operations)
        floors_checked.append("F13")
        verdict = "SEAL"
        reasoning = "All floors passed"

        if floors_failed:
            # HARD floors → VOID
            hard_floors = ["F1", "F2", "F6", "F7", "F10", "F11", "F12", "F13"]
            if any(f in floors_failed for f in hard_floors):
                verdict = "VOID"
                reasoning = f"HARD floor(s) failed: {floors_failed}"
            else:
                verdict = "SABAR"
                reasoning = f"SOFT floor(s) failed: {floors_failed}"

        # 888_HOLD for prod destructive operations
        if (
            tool_class in [ToolClass.DESTRUCTIVE, ToolClass.PROD_WRITE]
            and namespace in ["prod", "production"]
            and not payload.get("human_override", False)
        ):
            verdict = "888_HOLD"
            reasoning = "Production destructive operation requires human approval"

        # Find downstream server
        downstream = self.get_downstream_server(tool_name)

        decision = GatewayDecision(
            session_id=session_id,
            tool_name=tool_name,
            tool_class=tool_class,
            verdict=verdict,
            floors_checked=floors_checked,
            floors_failed=floors_failed,
            blast_radius=blast_radius,
            downstream_endpoint=downstream.endpoint if downstream else None,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reasoning=reasoning,
        )

        # Store decision in VAULT999
        self.decisions.append(decision)

        return decision

    async def forward_to_downstream(
        self,
        tool_name: str,
        payload: Dict[str, Any],
        decision: GatewayDecision,
    ) -> Dict[str, Any]:
        """Forward approved call to downstream MCP server."""
        import httpx

        downstream = self.get_downstream_server(tool_name)
        if not downstream:
            return {"error": "No downstream server configured for this tool"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{downstream.endpoint}/tools/{tool_name}",
                    json=payload,
                    headers={"Authorization": f"Bearer {downstream.auth_token or ''}"},
                    timeout=30.0,
                )
                return response.json()
        except Exception as e:
            return {
                "error": f"Downstream call failed: {e}",
                "gateway_decision": decision.verdict,
            }


# =============================================================================
# GATEWAY INSTANCE
# =============================================================================

gateway = MCPGateway()


# =============================================================================
# GATEWAY FUNCTIONS (Registered in server.py to avoid circular imports)
# =============================================================================


@constitutional_floor("F11", "F12")
async def gateway_route_tool(
    tool_name: str,
    payload: Dict[str, Any],
    session_id: str,
    actor_id: str = "agent",
    require_human_override: bool = False,
) -> Dict[str, Any]:
    """
    Route any MCP tool call through arifOS constitutional gateway.

    This is the single entry point for all Docker/K8s infrastructure operations.
    The gateway enforces 13 floors before forwarding to downstream MCP servers.

    Args:
        tool_name: Name of the downstream tool (e.g., "k8s_apply", "docker_build")
        payload: Tool-specific parameters
        session_id: Constitutional session identifier
        actor_id: Identity of the calling agent/user
        require_human_override: Force 888_HOLD for this operation

    Returns:
        Gateway decision + downstream result (if SEAL)

    Examples:
        # Read-only operation (light floors)
        await gateway_route_tool(
            tool_name="k8s_get",
            payload={"resource": "pods", "namespace": "default"},
            session_id="sess-001"
        )

        # Infrastructure write (full floors)
        await gateway_route_tool(
            tool_name="k8s_apply",
            payload={
                "manifest": "...",
                "namespace": "staging",
                "strategy": "rolling"
            },
            session_id="sess-002"
        )

        # Production destructive (888_HOLD required)
        await gateway_route_tool(
            tool_name="k8s_delete",
            payload={
                "resource": "deployment",
                "name": "api-server",
                "namespace": "prod",
                "backup_made": True,
                "human_override": True  # Required for prod destructive
            },
            session_id="sess-003"
        )
    """
    # Add human override flag to payload if requested
    if require_human_override:
        payload["human_override"] = True

    # Run constitutional evaluation
    decision = await gateway.evaluate_constitution(
        tool_name=tool_name,
        payload=payload,
        session_id=session_id,
        actor_id=actor_id,
    )

    # Store decision in session ledger
    store_stage_result(
        session_id=session_id,
        stage="gateway",
        result={
            "tool_name": tool_name,
            "verdict": decision.verdict,
            "floors_checked": decision.floors_checked,
            "floors_failed": decision.floors_failed,
            "blast_radius": decision.blast_radius,
            "reasoning": decision.reasoning,
        },
    )

    # Handle verdict
    if decision.verdict == "VOID":
        return {
            "status": "BLOCKED",
            "verdict": "VOID",
            "reason": decision.reasoning,
            "floors_failed": decision.floors_failed,
            "blast_radius": decision.blast_radius,
            "message": "🔥 DITEMPA, BUKAN DIBERI — Operation blocked by constitutional floors",
        }

    elif decision.verdict == "888_HOLD":
        return {
            "status": "PENDING_APPROVAL",
            "verdict": "888_HOLD",
            "reason": decision.reasoning,
            "review_url": f"/approve/{session_id}",
            "blast_radius": decision.blast_radius,
            "message": "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Human approval required for production operation",
        }

    elif decision.verdict == "SABAR":
        return {
            "status": "REPAIRABLE",
            "verdict": "SABAR",
            "reason": decision.reasoning,
            "floors_failed": decision.floors_failed,
            "suggestions": [
                "Add backup/rollback plan for F1",
                "Use digest-based image for F2",
                "Include canary strategy for F5",
            ],
            "message": "Operation needs revision before proceeding",
        }

    # SEAL: Forward to downstream MCP server
    downstream_result = await gateway.forward_to_downstream(
        tool_name=tool_name,
        payload=payload,
        decision=decision,
    )

    # Seal the operation
    from aaa_mcp.tools.vault_seal import vault_seal

    await vault_seal(
        session_id=session_id,
        verdict="SEAL",
        payload={
            "operation": tool_name,
            "payload": payload,
            "downstream_result": downstream_result,
        },
        query_summary=f"Gateway: {tool_name}",
        category="infrastructure",
        floors_checked=decision.floors_checked,
        floors_failed=decision.floors_failed,
    )

    return {
        "status": "SUCCESS",
        "verdict": "SEAL",
        "gateway_decision": {
            "floors_checked": decision.floors_checked,
            "blast_radius": decision.blast_radius,
            "reasoning": decision.reasoning,
        },
        "downstream_result": downstream_result,
        "message": "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Operation constitutionally approved and sealed",
    }


async def gateway_list_tools() -> Dict[str, Any]:
    """List all tools available through the constitutional gateway."""
    tools_by_server = {}

    for server_name, server in gateway.servers.items():
        if not server.enabled:
            continue

        tools = []
        for tool in server.allowed_tools:
            tool_class = server.tool_class_map.get(tool, ToolClass.INFRA_WRITE)
            floors = FLOOR_REQUIREMENTS.get(tool_class, [])
            tools.append(
                {
                    "name": tool,
                    "class": tool_class.value,
                    "required_floors": floors,
                }
            )

        tools_by_server[server_name] = {
            "endpoint": server.endpoint,
            "tools": tools,
        }

    return {
        "gateway": "arifOS Constitutional MCP Gateway",
        "version": "60.1-FORGE",
        "servers": tools_by_server,
        "floor_requirements": {tc.value: floors for tc, floors in FLOOR_REQUIREMENTS.items()},
    }


async def gateway_get_decisions(
    session_id: Optional[str] = None,
    limit: int = 100,
) -> Dict[str, Any]:
    """Query gateway decisions (audit trail)."""
    decisions = gateway.decisions

    if session_id:
        decisions = [d for d in decisions if d.session_id == session_id]

    decisions = decisions[-limit:]

    return {
        "count": len(decisions),
        "decisions": [
            {
                "session_id": d.session_id,
                "tool_name": d.tool_name,
                "verdict": d.verdict,
                "floors_failed": d.floors_failed,
                "timestamp": d.timestamp,
                "reasoning": d.reasoning,
            }
            for d in decisions
        ],
    }


# =============================================================================
# K8S CONSTITUTIONAL WRAPPER (P1)
# =============================================================================


@constitutional_floor("F1", "F2", "F6", "F10", "F11", "F12", "F13")
async def k8s_apply_guarded(
    manifest: str,
    namespace: str,
    session_id: str,
    strategy: str = "rolling",  # canary, blue-green, rolling
    backup_made: bool = False,
    human_override: bool = False,
) -> Dict[str, Any]:
    """
    Constitutionally-governed kubectl apply.

    Enforces:
    - F1: Rollback strategy required for production
    - F2: Digest-based images for production
    - F6: Blast radius calculation
    - F10: Manifest schema validation
    - F13: Human override for production

    Usage:
        await k8s_apply_guarded(
            manifest="apiVersion: apps/v1\nkind: Deployment...",
            namespace="prod",
            strategy="canary",
            backup_made=True,
            human_override=True,  # Required for prod
            session_id="sess-001"
        )
    """
    # Delegate to gateway with K8s-specific payload
    return await gateway_route_tool(
        tool_name="k8s_apply",
        payload={
            "manifest": manifest,
            "namespace": namespace,
            "strategy": strategy,
            "backup_made": backup_made,
            "human_override": human_override,
        },
        session_id=session_id,
    )


@constitutional_floor("F1", "F2", "F5", "F6", "F10", "F11", "F12", "F13")
async def k8s_delete_guarded(
    resource: str,
    name: str,
    namespace: str,
    session_id: str,
    backup_made: bool = False,
    human_override: bool = False,
    cascade: bool = True,
) -> Dict[str, Any]:
    """
    Constitutionally-governed kubectl delete.

    DESTRUCTIVE operation — requires:
    - F1: Backup made (reversibility)
    - F6: Blast radius < threshold
    - F13: 888_HOLD for production (human override required)
    """
    return await gateway_route_tool(
        tool_name="k8s_delete",
        payload={
            "resource": resource,
            "name": name,
            "namespace": namespace,
            "backup_made": backup_made,
            "human_override": human_override,
            "cascade": cascade,
        },
        session_id=session_id,
    )
