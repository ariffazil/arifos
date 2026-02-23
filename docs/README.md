# arifOS Human-AI Interface SDK

> **The HumanLayer for Constitutional AI**  
> Connect humans to the arifOS control plane with 13-floor governance.

**Pattern:** Human-in-the-Loop (HITL) SDK  
**Industry Analog:** HumanLayer, Agents SDK, Permit HITL  
**Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given

---

## Overview

The arifOS SDK provides a clean interface for AI agents and human operators to interact with the constitutional governance control plane. It handles:

- ✅ **Identity & Accountability** — Who is responsible?
- ✅ **Floor Enforcement** — Should this proceed?
- ✅ **Human Override** — 888_HOLD for critical operations
- ✅ **Audit & Compliance** — Everything logged to VAULT999

---

## Quick Start

### Python SDK

```bash
pip install arifos-sdk
```

```python
import arifos_sdk as arifos
import asyncio

async def main():
    # Initialize session
    session = arifos.Session(
        actor_id="arif@arif-fazil.com",
        actor_type="human",
        groups=["platform-engineers"],
    )
    
    # Check action constitutionally
    result = await session.check_action(
        tool="k8s_apply",
        payload={
            "manifest": "...",
            "namespace": "prod",
            "strategy": "canary",
        },
    )
    
    print(f"Verdict: {result.verdict}")
    print(f"Blast Radius: {result.blast_radius.score}")
    
    # Handle 888_HOLD
    if result.verdict == "888_HOLD":
        print("⏳ Waiting for human approval...")
        
        approval = await session.request_approval(
            result,
            notify=["slack", "email"],
        )
        
        final = await session.await_approval(approval.hold_id, timeout=3600)
        
        if final.is_approved:
            print("✅ Approved! Proceeding with deployment...")
        else:
            print(f"❌ Rejected: {final.rejection_reason}")

asyncio.run(main())
```

---

## SDK Components

### Python SDK (`SDK/python/`)

| Module | Purpose |
|--------|---------|
| `client.py` | `ArifOSClient`, `Session` — Core interface |
| `types.py` | `Verdict`, `GatewayDecision`, `BlastRadius` |
| `decorators.py` | `@requires_f13`, `@constitutional_infra_write` |
| `exceptions.py` | `FloorViolationError`, `HumanApprovalTimeoutError` |

### UI Components (`SDK/ui/`)

| Component | Purpose |
|-----------|---------|
| `ApprovalQueue` | Dashboard for pending 888_HOLDs |
| `BlastRadiusCard` | Visual blast radius display |
| `FloorBreakdown` | Constitutional floor results |
| `DecisionButtons` | SEAL/SABAR/VOID controls |

---

## Key Features

### 1. Risk-Tiered Actions

```python
# Read-only: Fast path (F11, F12 only)
result = await session.check_action("k8s_get", {...})
# → SEAL immediately

# Infrastructure write: Full floors
result = await session.check_action("k8s_apply", {...})
# → SEAL or 888_HOLD (if production)

# Destructive: Mandatory human approval
result = await session.check_action("k8s_delete", {...})
# → 888_HOLD always
```

### 2. Decorators for Agent Frameworks

```python
from arifos_sdk import requires_f13, constitutional_infra_write

@constitutional_infra_write()
async def deploy_service(session, manifest):
    """Auto-enforces F1, F2, F6, F10, F11, F12."""
    return await session.apply_manifest(manifest, namespace="prod")

@requires_f13(timeout=7200)
async def delete_database(session, name):
    """Requires human approval (F13 Sovereign)."""
    return await session.check_action("k8s_delete", {
        "resource": "StatefulSet",
        "name": name,
        "namespace": "prod",
    })
```

### 3. Human-as-Tool Pattern

```python
@human_as_tool(contact_method="slack", contact_id="#oncall")
async def ask_oncall(session, question: str):
    """
    Escalate question to human on-call.
    Blocks until human responds.
    """
    pass
```

---

## 888_HOLD UI Flow

### Staging (Auto-Approved)

```
Agent → SDK → Gateway → SEAL → Deploy
                 ↓
              No UI needed
```

### Production (888_HOLD)

```
Agent → SDK → Gateway → 888_HOLD → Notify (Slack/Email)
                                        ↓
                                     Human opens UI
                                        ↓
                              Review Blast Radius + Floors
                                        ↓
                              SEAL / SABAR / VOID
                                        ↓
                              Webhook → SDK → Deploy
```

**UI Screens:**
1. **Approval Queue** — List of pending 888_HOLDs
2. **Detail View** — Blast radius, floors, manifest
3. **Decision Panel** — SEAL/SABAR/VOID with reason

See `SDK/ui/888-hold-approval-ui.md` for full specification.

---

## Integration Examples

### LangGraph Agent

```python
from langgraph.graph import Graph
from arifos_sdk import Session

session = Session(actor_id="agent-1", actor_type="agent")

async def deploy_node(state):
    result = await session.check_action(
        "k8s_apply",
        state["manifest"],
    )
    
    if result.verdict == "888_HOLD":
        return {"action": "await_human"}
    
    return {"action": "deploy", "approved": result.verdict == "SEAL"}

async def human_approval_node(state):
    approval = await session.request_approval(state["result"])
    final = await session.await_approval(approval.hold_id)
    return {"verdict": final.verdict}

graph = Graph()
graph.add_node("deploy", deploy_node)
graph.add_node("human_approval", human_approval_node)
graph.add_edge("deploy", "human_approval")
```

### Slack Bot

```python
@app.command("/arifos-approve")
async def approve_command(ack, command):
    await ack()
    hold_id = command["text"]
    
    # Call SDK to approve
    client = ArifOSClient()
    await client.resolve_hold(hold_id, verdict="SEAL")
    
    return f"✅ Approved {hold_id}"
```

---

## Configuration

```python
import arifos_sdk as arifos

# Global configuration
arifos.configure(
    gateway_url="https://aaamcp.arif-fazil.com",
    api_key="arifos_sk_...",
    default_timeout=30.0,
)

# Or via environment
export ARIFOS_GATEWAY_URL="https://aaamcp.arif-fazil.com"
export ARIFOS_API_KEY="arifos_sk_..."
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Your Application                               │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Agent / Service / Script                                          │ │
│  │  ───────────────────────────────────────────────────────────────   │ │
│  │  import arifos_sdk as arifos                                       │ │
│  │                                                                    │ │
│  │  session = arifos.Session(...)                                     │ │
│  │  result = await session.check_action(...)                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────────────┐
│                     arifOS Constitutional Gateway                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Identity   │→ │    Floors    │→ │   F13 Gate   │→ │   VAULT999   │ │
│  │   (F11)      │  │  (F1-F12)    │  │  (Human)     │  │   (Audit)    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
               ┌────────┐     ┌────────┐     ┌──────────┐
               │  K8s   │     │ Docker │     │   OPA    │
               │  MCP   │     │  MCP   │     │  Policy  │
               └────────┘     └────────┘     └──────────┘
```

---

## Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| H2.1 | Python SDK Core | 🔄 In Progress |
| H2.1 | UI Components (React) | 📋 Planned |
| H2.1 | Slack Integration | 📋 Planned |
| H2.2 | TypeScript SDK | 📋 Planned |
| H2.2 | LangGraph Integration | 📋 Planned |
| H2.3 | Mobile App | 📋 Planned |

---

## License

AGPL-3.0-only — Same as arifOS core.

---

**DITEMPA BUKAN DIBERI** 💎🔥🧠

*Intelligence forged through human-AI collaboration.*
