# AAA MCP Server

**Constitutional AI Governance for the Model Context Protocol**

Production-grade MCP server enforcing 13 constitutional floors (F1-F13) on any LLM.

[![MCP](https://img.shields.io/badge/MCP-2025--11--25-purple)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/arifos.svg)](https://pypi.org/project/arifos/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-orange)](https://github.com/ariffazil/arifOS/blob/main/LICENSE)

---

## Quick Start

```bash
# Install
pip install arifos

# Run (stdio transport for Claude Desktop, Cursor)
python -m aaa_mcp

# Run (SSE transport for remote clients)
python -m aaa_mcp sse

# Run (HTTP transport)
python -m aaa_mcp http
```

---

## What Makes It Different

Unlike prompt-based guardrails that can be bypassed, **AAA MCP enforces constraints at the architectural level**:

| Floor | Principle | Enforcement |
|-------|-----------|-------------|
| **F2** | Truth | ≥99% certainty required (τ ≥ 0.99) |
| **F7** | Humility | Uncertainty band Ω₀ ∈ [0.03, 0.05] enforced |
| **F12** | Defense | Injection attacks automatically blocked |
| **F1** | Amanah | All decisions cryptographically auditable |

**Every tool call** passes through the 000-999 constitutional pipeline.

---

## The 10 Canonical MCP Tools

| Tool | Stage | Trinity | Floors | Purpose |
|------|-------|---------|--------|---------|
| `init_gate` | 000_INIT | Gate | F11, F12 | Session ignition, injection scan |
| `forge_pipeline` | 000-999 | All | F1-F13 | Unified pipeline entry |
| `agi_sense` | 111_SENSE | Δ Mind | F4 | Intent classification |
| `agi_think` | 222_THINK | Δ Mind | F2, F4, F7 | Hypothesis generation |
| `agi_reason` | 333_REASON | Δ Mind | F2, F4, F7, F10 | Logic & deduction |
| `reality_search` | — | External | F2, F7, F10 | Web grounding |
| `asi_empathize` | 555_EMPATHY | Ω Heart | F5, F6 | Stakeholder impact |
| `asi_align` | 666_ALIGN | Ω Heart | F5, F6, F9 | Ethics alignment |
| `apex_verdict` | 888_JUDGE | Ψ Soul | F3, F8, F11 | Final judgment |
| `vault_seal` | 999_SEAL | VAULT | F1, F3 | Immutable audit |

**Verdicts:** `SEAL` | `VOID` | `PARTIAL` | `SABAR` | `888_HOLD`

---

## Installation & Configuration

### Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp"],
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
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

### Programmatic

```python
from aaa_mcp.server import init_gate, agi_reason, apex_verdict

# Start constitutional session
session = await init_gate(
    query="Should we approve this loan?",
    actor_id="analyst_001"
)

if session["verdict"] == "VOID":
    print(f"Blocked: {session['reason']}")
    return

# Execute with F2, F4, F7 enforcement
result = await agi_reason(
    query="Analyze credit risk",
    session_id=session["session_id"]
)

print(f"Verdict: {result['verdict']}")
print(f"Ω₀: {result['humility']}")  # Uncertainty metric
```

---

## Architecture

This MCP server is part of **[arifOS](https://arifos.arif-fazil.com)**, a constitutional AI framework.

```
┌─────────────────────────────────────────────────────────────┐
│                    AAA MCP Server                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  init_gate  │───→│   agi_*     │───→│ apex_verdict│     │
│  │  (F11,F12)  │    │ (F2,F4,F7)  │    │(F3,F8,F11)  │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                                │            │
│  ┌─────────────────────────────────────────────┘            │
│  │                                                           │
│  ▼                                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  5-Organ Kernel                      │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │    │
│  │  │INIT(000)│→ │AGI(Δ)   │→ │ASI(Ω)   │→ │APEX(Ψ)  │ │    │
│  │  │Airlock  │  │Mind     │  │Heart    │  │Soul     │ │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └────┬────┘ │    │
│  │                                               │      │    │
│  │  ┌────────────────────────────────────────────┘      │    │
│  │  │                                                    │    │
│  │  ▼                                                    │    │
│  │  ┌─────────────┐    ┌─────────────┐                   │    │
│  │  │ vault_seal  │    │  VAULT999   │                   │    │
│  │  │  (F1,F3)    │───→│  Ledger     │                   │    │
│  │  └─────────────┘    └─────────────┘                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                          [core/]                             │
└─────────────────────────────────────────────────────────────┘
```

| Component | Location | Purpose |
|-----------|----------|---------|
| **MCP Server** | [`server.py`](server.py) | FastMCP 2.0+ entry point |
| **Tool Handlers** | [`core/`](../core/) | 5-Organ Kernel, F1-F13 enforcement |
| **Pipeline** | [`core/pipeline.py`](../core/pipeline.py) | 000-999 stage orchestration |
| **Floors** | [`core/shared/floors.py`](../core/shared/floors.py) | Constitutional validation |

See [`core/`](../core/) for the 5-Organ Kernel implementation.

---

## Enterprise Use Cases

### Financial Services (Compliance)
```python
verdict = await apex_verdict(
    query="Approve $500K loan to Acme Corp",
    require_sovereign=True  # F13: Forces human sign-off
)
# VAULT999 proves due diligence to regulators
```

### Healthcare (Safety-Critical)
```python
result = await agi_reason(
    query="Side effects of warfarin with aspirin",
    grounding_required=True  # F2: Requires external verification
)
# Ω₀ ∈ [0.03,0.05] — no overconfident medical claims
```

### Legal (Liability Protection)
```python
session = await init_gate(
    query="Review merger agreement for risks",
    grounding_required=True
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
| **MCP Endpoint** | [aaamcp.arif-fazil.com/mcp](https://aaamcp.arif-fazil.com/mcp) |
| **Health Check** | [aaamcp.arif-fazil.com/health](https://aaamcp.arif-fazil.com/health) |
| **Registry Entry** | [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) |
| **Source Code** | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) |

---

## License

AGPL-3.0-only — *Open restrictions for open safety.*

**Sovereign:** Muhammad Arif bin Fazil

---

*DITEMPA BUKAN DIBERI — Forged, Not Given* 🔥💎
