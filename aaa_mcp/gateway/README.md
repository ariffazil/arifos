# arifOS MCP Gateway

**Constitutional Control Plane for Docker/Kubernetes Operations**

The MCP Gateway is a single entry point that enforces arifOS's 13 constitutional floors before forwarding infrastructure operations to downstream MCP servers (K8s, Docker, OPA).

> **Pattern:** Human-Centric AI Governance Control Plane  
> **Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      arifOS MCP Gateway                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  Identity   │ →  │  Floors     │ →  │   Observability     │ │
│  │   (F11)     │    │  (F1-F13)   │    │      (F4)           │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│         │                  │                     │               │
│         ▼                  ▼                     ▼               │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    Verdict Engine                        │   │
│   │   SEAL → Forward to downstream                          │   │
│   │   VOID → Block immediately                               │   │
│   │   888_HOLD → Wait for human approval                    │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │   K8s    │       │  Docker  │       │   OPA    │
    │   MCP    │       │   MCP    │       │  Policy  │
    └──────────┘       └──────────┘       └──────────┘
```

---

## Quick Start

### 1. Route a Tool Call

```python
from aaa_mcp.server import gateway_route_tool

# Staging deployment (SEAL)
result = await gateway_route_tool(
    tool_name="k8s_apply",
    payload={
        "manifest": "...",
        "namespace": "staging",
        "strategy": "rolling",
    },
    session_id="sess-001",
)

# Production deployment (888_HOLD)
result = await gateway_route_tool(
    tool_name="k8s_apply",
    payload={
        "manifest": "...",
        "namespace": "prod",
        "strategy": "canary",
        "backup_made": True,
        "human_override": True,  # Required for prod
    },
    session_id="sess-002",
)
```

### 2. Register Identity

```python
from aaa_mcp.gateway import create_human_actor, identity_registry

actor = create_human_actor(
    user_id="arif-123",
    email="arif@arif-fazil.com",
    name="Arif Fazil",
    groups=["platform-engineers"],
)

identity_registry.register(
    session_id="sess-001",
    actor=actor,
    tool_name="k8s_apply",
    tool_class="infra_write",
)
```

### 3. Post-Deploy Observability

```python
from aaa_mcp.gateway import post_deploy_monitor

# Start monitoring
await post_deploy_monitor.start_monitoring(
    session_id="sess-001",
    deployment_name="api-server",
    namespace="prod",
)

# Later: finalize seal with F4 validation
result = await post_deploy_monitor.finalize_seal("sess-001")
# Returns: SEAL (if healthy) or SABAR (if entropy increased)
```

---

## Tool Classification

| Class | Floors | 888_HOLD Trigger |
|-------|--------|------------------|
| `read_only` | F11, F12 | Never |
| `infra_write` | F1, F2, F6, F10, F11, F12 | prod namespace |
| `destructive` | F1-F13 (except F7) | Always |
| `prod_write` | Full F1-F13 | Always |

---

## Floor Enforcement

### F1 Amanah (Reversibility)
- Requires `backup_made: True` for destructive ops
- Requires deployment strategy (`canary`, `blue-green`, `rolling`)

### F2 Truth (Image Provenance)
- Detects `:latest` tags (mutable)
- Requires `@sha256:` digest for production
- Trusted registry whitelist

### F5 Peace² (Stability)
- Validates deployment strategy
- Checks for resource limits
- Verifies liveness/readiness probes

### F6 Empathy (Blast Radius)
- Calculates affected pods/deployments
- Critical namespace detection (`prod`, `kube-system`)
- κᵣ ≥ 0.95 threshold for production

### F10 Ontology (Schema Validation)
- K8s manifest schema validation
- OPA/Conftest policy evaluation
- Built-in Rego-like rules fallback

### F13 Sovereign (Human Override)
- `human_override: True` required for:
  - Production destructive operations
  - High blast radius (score > 0.7)
  - `prod_write` class operations

---

## Configuration

Edit `aaa_mcp/policies/gateway_config.yaml` to tune thresholds:

```yaml
thresholds:
  f2_truth:
    default: 0.90
    production: 0.95
  
  f6_empathy:
    default: 0.70
    critical: 0.95

hold_triggers:
  always_require_override:
    - namespace: prod
      operation: delete
```

---

## MCP Tools

| Tool | Purpose |
|------|---------|
| `gateway_route_tool` | Single entry point for all infra ops |
| `gateway_list_tools` | List available tools |
| `gateway_get_decisions` | Query audit trail |
| `k8s_apply_guarded` | Constitutional kubectl apply |
| `k8s_delete_guarded` | Constitutional kubectl delete |
| `k8s_analyze_manifest` | Security posture analysis |
| `opa_validate_manifest` | F10 Ontology validation |

---

## Industry Alignment

This implementation follows patterns from:
- **Credo AI** — Risk-tiered actions with human oversight
- **Forrester** — AI governance control plane architecture
- **Mint MCP** — Agentic AI governance framework
- **Open Policy Agent** — Policy-as-code admission control

---

**DITEMPA BUKAN DIBERI** 💎🔥🧠
