"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""
arifOS MCP Gateway — Constitutional Control Plane

Single entry point for all Docker/Kubernetes infrastructure operations.
Enforces 13 floors before forwarding to downstream MCP servers.

Modules:
    identity: Actor identity and RBAC (F11 Authority)
    observability: Post-deploy health checks (F4 Clarity)

Usage:
    from arifosmcp.transport.gateway import identity_registry, post_deploy_monitor
    from arifosmcp.transport.gateway.identity import create_human_actor

    # Register human actor
    actor = create_human_actor(
        user_id="user-123",
        email="arif@arif-fazil.com",
        name="Arif Fazil",
        groups=["platform-engineers"],
    )

    # Start monitoring
    await post_deploy_monitor.start_monitoring(
        session_id="sess-001",
        deployment_name="api-server",
        namespace="prod",
    )

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from arifosmcp.transport.gateway.identity import (
    Actor,
    ActorType,
    IdentityRegistry,
    IdentitySource,
    SessionIdentity,
    create_agent,
    create_human_actor,
    create_service_account,
    identity_registry,
)
from arifosmcp.transport.gateway.observability import (
    F4ClarityResult,
    HealthMetrics,
    HealthStatus,
    PostDeployMonitor,
    post_deploy_monitor,
)

__all__ = [
    # Identity
    "IdentityRegistry",
    "Actor",
    "ActorType",
    "IdentitySource",
    "SessionIdentity",
    "identity_registry",
    "create_human_actor",
    "create_service_account",
    "create_agent",
    # Observability
    "PostDeployMonitor",
    "F4ClarityResult",
    "HealthMetrics",
    "HealthStatus",
    "post_deploy_monitor",
]
