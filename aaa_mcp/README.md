# AAA MCP Server

**The Missing Constitutional Layer for the Model Context Protocol**

Production-grade **Governance Engine** enforcing 13 constitutional floors (F1-F13) and v60 metabolic principles on any LLM.

[![MCP](https://img.shields.io/badge/MCP-2025--11--25-purple)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/arifos.svg)](https://pypi.org/project/arifos/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-orange)](https://github.com/ariffazil/arifOS/blob/main/LICENSE)

---

## Quick Start

```bash
# No installation required with uvx!
uvx arifos stdio      # stdio (Claude Desktop, Cursor, Qwen)
uvx arifos sse        # SSE (Remote/Cloud)
uvx arifos http       # Streamable HTTP
```

---

## What Makes It Different

Unlike prompt-based guardrails that can be bypassed, **AAA MCP enforces constraints at the metabolic level** using a **Composite Architecture**:

1.  **Constitutional, Not Just Guardrailed:** Uses hard thermodynamic evaluation rather than just text filtering.
2.  **Creativity/Governance Separation:** The Architect (Δ) explores hypotheses while the Judge (Ψ) enforces limits.
3.  **Governance vs. Guardrails:** AAA MCP is a structural system for meaning co-creation, not a simple "no-go" filter.

| Floor | Principle | Enforcement |
|-------|-----------|-------------|
| **F2** | Truth | ≥99% certainty required (τ ≥ 0.99) |
| **F7** | Humility | Uncertainty band Ω₀ ∈ [0.03, 0.05] enforced |
| **F12** | Defense | Injection attacks automatically blocked |
| **F1** | Amanah | All decisions cryptographically auditable |

**The Metabolic Loop (000-999)** ensures that exploration is always balanced by discipline.

---

## The 13 Canonical MCP Tools

| Tool | Stage | Organ | Floors | Purpose |
|------|-------|---------|--------|---------|
| `anchor_session` | 000 | Ψ Init | F11, F12, F13 | Session ignition + defense scan |
| `reason_mind` | 111-444 | Δ Mind | F2, F4, F7, F8, F10 | Reason + integrate + draft |
| `recall_memory` | 555 | PHOENIX | F4, F7, F8 | Dynamic associative memory retrieval |
| `simulate_heart` | 555-666 | Ω Heart | F5, F6, F9 | Empathy + alignment simulation |
| `critique_thought` | 666 | Ω Heart | F4, F7, F8 | Constitutional critique + bias checks |
| `eureka_forge` | 777 | Ψ Soul | F1, F11, F12 | Sandboxed forge execution |
| `apex_judge` | 888 | Ψ Soul | F1-F13 | Sovereign verdict synthesis |
| `seal_vault` | 999 | VAULT | F1, F3, F10 | Immutable audit seal |
| `search_reality` | utility | External | F2, F7 | Web grounding search |
| `fetch_content` | utility | External | F2, F7 | Evidence/content retrieval |
| `inspect_file` | utility | Internal | F1, F4, F11 | Filesystem inspection (read-only) |
| `audit_rules` | utility | Internal | F2, F3, F10 | Constitutional health verification |
| `check_vital` | utility | Internal | F4, F5, F7 | Runtime health telemetry |

Alias compatibility:
- `forge_hand` -> `eureka_forge`
- `judge_soul` -> `apex_judge`

**Verdicts:** `SEAL` | `VOID` | `PARTIAL` | `SABAR` | `888_HOLD`

---

## Installation & Configuration

### Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "uvx",
      "args": ["arifos", "stdio"],
      "env": { "ARIFOS_MODE": "PROD" }
    }
  }
}
```

### Cursor

Create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "uvx",
      "args": ["arifos", "stdio"]
    }
  }
}
```

### Cline / Claude Dev

Add to your Cline MCP settings file (e.g., `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "arifos-local": {
      "command": "uvx",
      "args": ["arifos", "stdio"],
      "disabled": false,
      "alwaysAllow": []
    },
    "arifos-vps": {
      "url": "https://arifosmcp.arif-fazil.com/sse",
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### Programmatic

```python
from arifos_aaa_mcp.server import anchor_session, reason_mind, apex_judge

# Start constitutional session
session = await anchor_session(
    query="Should we approve this loan?",
    actor_id="analyst_001"
)

if session["verdict"] == "VOID":
    print(f"Blocked: {session['reason']}")
    return

# Execute with Δ cognition (reason + integrate + draft)
result = await reason_mind(
    query="Analyze credit risk",
    session_id=session["session_id"]
)

print(f"Verdict: {result['verdict']}")
print(f"Ω₀: {result['humility']}")  # Uncertainty metric
```

---

## Architecture

AAA MCP implements a **Composite Architecture** where human sovereignty is the final arbiter. It serves as the bridge between the fluid application layer and the rigid constitutional kernel.

```
┌─────────────────────────────────────────────────────────────┐
│                    AAA MCP Server                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │anchor_session│──→│reason_mind  │───→│apex_judge  │     │
│  │  (F11,F12)  │    │  Reasoning  │    │ Constitutional│     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                                │            │
│  ┌─────────────────────────────────────────────┘            │
│  │                                                           │
│  ▼                                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               7-Organ Sovereign Stack               │    │
│  │  ┌──────┐  ┌──────┐  ┌───────┐  ┌──────┐  ┌──────┐  │    │
│  │  │ INIT │→ │ AGI  │→ │PHOENIX│→ │ ASI  │→ │ APEX │  │    │
│  │  └──────┘  └──────┘  └───────┘  └──────┘  └──┬───┘  │    │
│  │                                              │      │    │
│  │  ┌───────────────────────────────────────────┘      │    │
│  │  │                                                  │    │
│  │  ▼                                                  │    │
│  │  ┌──────┐    ┌─────────┐    ┌───────┐               │    │
│  │  │FORGE │──→ │vault_seal│──→ │ VAULT │               │    │
│  │  └──────┘    └─────────┘    └───────┘               │    │
│  └─────────────────────────────────────────────────────┘    │
│                     The Metabolic Loop                       │
└─────────────────────────────────────────────────────────────┘
``````

| Component | Location | Purpose |
|-----------|----------|---------|
| **MCP Server** | [`server.py`](server.py) | FastMCP 2.0+ entry point |
| **Governance Core** | [`core/`](../core/) | 7-Organ Sovereign Stack, v60 Postulate enforcement |
| **Pipeline** | [`core/pipeline.py`](../core/pipeline.py) | 000-999 stage orchestration |
| **Floors** | [`core/shared/floors.py`](../core/shared/floors.py) | Constitutional validation |

See [`core/`](../core/) for the 7-Organ Sovereign Stack and Metabolic Loop implementation.

---

## REST API & MCP Protocol

### Transports

| Transport | Command | Use Case |
|-----------|---------|----------|
| **stdio** | `uvx arifos stdio` | Claude Desktop, Cursor, local agents |
| **SSE** | `uvx arifos sse` | Remote connections, ChatGPT Developer Mode |
| **HTTP** | `uvx arifos http` | Streamable HTTP transport |

### MCP JSON-RPC Protocol (SSE)

When running in SSE mode, the server exposes:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/sse` | `GET` | SSE event stream (returns endpoint URL) |
| `/messages` | `POST` | MCP JSON-RPC message handling |

**Protocol Flow:**

```bash
# 1. Client connects to SSE endpoint
curl -N https://arifosmcp.arif-fazil.com/sse
# Returns: event: endpoint
data: https://arifosmcp.arif-fazil.com/messages

# 2. Client sends JSON-RPC messages to /messages
curl -X POST https://arifosmcp.arif-fazil.com/messages \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

**Supported Methods:**

```bash
# Initialize connection
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}

# List available tools
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}

# Call a tool
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"anchor_session","arguments":{"query":"..."}}}

# Keepalive ping
{"jsonrpc":"2.0","id":4,"method":"ping","params":{}}

# Client initialized notification
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
```

### Direct REST API

For non-MCP integrations, direct REST endpoints are available:

```bash
# Health and readiness
curl https://arifosmcp.arif-fazil.com/health
curl https://arifosmcp.arif-fazil.com/ready
curl https://arifosmcp.arif-fazil.com/version

# List tools (simple format)
curl https://arifosmcp.arif-fazil.com/tools

# Call tool directly
curl -X POST https://arifosmcp.arif-fazil.com/tools/anchor_session \
  -H "Content-Type: application/json" \
  -d '{"query":"test","actor_id":"user"}'

# Full pipeline wrapper (000→333→666→888→999)
curl -X POST https://arifosmcp.arif-fazil.com/apex_judge \
  -H "Content-Type: application/json" \
  -d '{"query":"Should we proceed?","actor_id":"user"}'
```

See [`rest.py`](rest.py) for the full REST API implementation.

---

## Enterprise Use Cases

### Financial Services (Compliance)
```python
session = await anchor_session(
    query="Approve $500K loan to Acme Corp",
    actor_id="risk_officer_001",
)

verdict = await apex_judge(
    session_id=session["session_id"],
    query="Approve $500K loan to Acme Corp",
    implementation_details={"risk_model": "v3", "policy": "credit_2026"},
    proposed_verdict="SEAL",
    human_approve=True,  # F13 human sign-off path
)
# VAULT999 proves due diligence to regulators
```

### Healthcare (Safety-Critical)
```python
result = await reason_mind(
    query="Side effects of warfarin with aspirin",
    session_id="sess_12345",
    grounding=["pubmed", "clinical-guidelines"],  # F2 external verification context
)
# Ω₀ ∈ [0.03,0.05] — no overconfident medical claims
```

### Legal (Liability Protection)
```python
session = await anchor_session(
    query="Review merger agreement for risks",
    actor_id="legal_analyst_001",
)
# Immutable audit trail proves review occurred
```

---

## Configuration

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://...  # VAULT999 persistence

# Optional
BRAVE_API_KEY=              # Web search grounding
GOVERNANCE_MODE=HARD        # HARD (strict) or SOFT (advisory)
REQUIRE_SOVEREIGN=false     # Force F13 human override
```

See [Configuration Reference](../README.md#configuration-reference) for full options.

---

## Resources

| Resource | Link |
|----------|------|
| **Documentation** | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) |
| **MCP SSE** | `https://arifosmcp.arif-fazil.com/sse` |
| **MCP Messages** | `https://arifosmcp.arif-fazil.com/messages` |
| **Health Check** | [arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health) |
| **Registry Entry** | [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) |
| **Source Code** | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) |

---

## License

AGPL-3.0-only — *Open restrictions for open safety.*

**Sovereign:** Muhammad Arif bin Fazil

---

*DITEMPA BUKAN DIBERI — Forged, Not Given* 🔥💎
