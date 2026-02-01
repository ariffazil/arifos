# AAA MCP Server — Constitutional AI Governance

**Model-Agnostic · Platform-Universal · Constitutionally Hardened · MCP 2025-11-25 Spec Compliant**

The AAA MCP server exposes arifOS constitutional governance as a [Model Context Protocol](https://modelcontextprotocol.io/) server. Any AI model (Claude, GPT, Gemini, Kimi, Llama) can call the 7 canonical tools through any MCP client (Claude Desktop, Cursor, VS Code, Windsurf) over any transport (stdio, Streamable HTTP).

## What's New in v55.1

- **Streamable HTTP Transport** — Replaces legacy SSE with stateless HTTP (MCP spec 2025-03-26+)
- **MCP Resources** — Expose F1-F13 floor definitions and VAULT ledger as read-only resources
- **MCP Prompts** — 5 reusable constitutional evaluation templates
- **Full Spec Compliance** — outputSchema, annotations, title on all tools
- **69 Integration Tests** — Comprehensive coverage for all three phases

---

## Quick Start

### Install

```bash
# From source (editable)
pip install -e ".[dev]"

# From PyPI
pip install aaa-mcp
```

### Run

```bash
# Auto-detect best transport
aaa-mcp

# Explicit transport selection
aaa-mcp-stdio                    # stdin/stdout (Claude Desktop, Cursor)
aaa-mcp-sse                      # Streamable HTTP (remote clients, Railway)

# Via Python module
python -m codebase.mcp            # auto
python -m codebase.mcp stdio      # explicit stdio
python -m codebase.mcp sse        # explicit Streamable HTTP

# Docker (production)
docker build -t arifos:latest .
docker run -e PORT=8000 -p 8000:8000 arifos:latest
```

### Environment

```bash
HOST=127.0.0.1                   # Bind address (default: 127.0.0.1 for local, set 0.0.0.0 for cloud)
PORT=8000                        # Server port (SSE/HTTP)
LOG_LEVEL=info                   # debug|info|warning|error
GOVERNANCE_MODE=HARD             # HARD (all floors enforced) | SOFT (warnings only)
VAULT_PATH=./VAULT999            # Immutable ledger storage
ARIFOS_MODE=PROD                 # STUDIO|PROD|DEBUG
```

---

## Client Setup

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "aaa-mcp-stdio",
      "alwaysAllow": ["_init_", "_agi_", "_asi_", "_apex_", "_vault_", "_trinity_", "_reality_"]
    }
  }
}
```

### Cursor IDE

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "aaa-mcp-stdio",
      "args": [],
      "env": { "GOVERNANCE_MODE": "HARD" }
    }
  }
}
```

### VS Code (Continue / Copilot)

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "aaa-mcp": {
      "command": "aaa-mcp-stdio",
      "args": []
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "aaa-mcp-stdio"
    }
  }
}
```

### Remote / HTTP (ChatGPT, Gemini, any client)

```bash
# Start Streamable HTTP server
aaa-mcp-sse

# Connect from any HTTP MCP client
# Endpoint: http://localhost:8000/mcp
# Transport: Streamable HTTP (POST + GET)
# Headers: MCP-Protocol-Version: 2025-11-25
```

**Live public endpoint:** `https://aaamcp.arif-fazil.com/mcp`

---

## The 7 Canonical Tools

Every tool enforces constitutional floors and returns a verdict. All tools include `outputSchema`, `annotations`, and `title` for MCP spec compliance.

| Tool | Gate | Purpose | Floors Enforced |
|------|------|---------|-----------------|
| **`_init_`** | 000 | Session ignition, identity verification, injection scan | F1, F11, F12 |
| **`_agi_`** | 111-333 | Mind engine — truth, precision-weighted reasoning | F2, F4, F7, F10 |
| **`_asi_`** | 444-666 | Heart engine — safety, empathy, stakeholder protection | F1, F5, F6, F9 |
| **`_apex_`** | 888 | Soul engine — judgment, 9-paradox equilibrium, verdict | F3, F8, F11, F12 |
| **`_vault_`** | 999 | Immutable ledger — Merkle-sealed audit entry | F1, F8 |
| **`_trinity_`** | 000→999 | Full pipeline — runs all engines in sequence | All F1-F13 |
| **`_reality_`** | External | Fact-checker — external source verification | F7 |

### Tool Schema (MCP 2025-11-25 Compliant)

```json
{
  "name": "_trinity_",
  "title": "Full Constitutional Pipeline",
  "description": "Complete metabolic loop: AGI→ASI→APEX→VAULT",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "maxLength": 10000},
      "session_id": {"type": "string"},
      "auto_seal": {"type": "boolean", "default": true}
    },
    "required": ["query"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "verdict": {"type": "string", "enum": ["SEAL", "VOID", "SABAR"]},
      "trinity_score": {"type": "number"},
      "floor_scores": {"type": "object"}
    },
    "required": ["verdict", "trinity_score"]
  },
  "annotations": {
    "title": "Full Trinity",
    "readOnlyHint": false,
    "destructiveHint": true,
    "openWorldHint": true
  }
}
```

### Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **SEAL** | All floors pass | ✅ Proceed |
| **PARTIAL** | Soft floor warning (F3, F5, F6, F8) | ⚠️ Proceed with caution |
| **VOID** | Hard floor failed (F1, F2, F4, F7, F9-F12) | ❌ Blocked |
| **888_HOLD** | High-stakes operation detected | ⏸️ Requires human confirmation |
| **SABAR** | Multiple floor concerns | 🧊 Cool down, review needed |

---

## MCP Resources (v55.1)

Read-only contextual data exposed as MCP Resources. These provide constitutional context without requiring tool calls.

| Resource URI | Description | Content |
|--------------|-------------|---------|
| `config://floors` | All 13 constitutional floors | F1-F13 definitions, thresholds, formulas |
| `config://verdicts` | Verdict hierarchy | SABAR > VOID > 888_HOLD > PARTIAL > SEAL |
| `floor://{F1-F13}` | Individual floor | Specific floor definition |
| `vault://ledger/latest` | Latest VAULT entry | Most recent sealed decision |
| `vault://ledger/stats` | Ledger statistics | Entry count, last hash, chain integrity |

### Accessing Resources

Resources are automatically available to MCP clients that support them:

```python
# Client reads floor definition
floor_f1 = await client.read_resource("floor://F1")
# Returns: {"id": "F1", "name": "Amanah", "threshold": "Reversible=true", ...}

# Client reads verdict hierarchy
verdicts = await client.read_resource("config://verdicts")
# Returns: {"hierarchy": {"SABAR": 5, "VOID": 4, ...}, "descriptions": {...}}
```

---

## MCP Prompts (v55.1)

Reusable constitutional evaluation templates. These are user-controlled prompts for common governance workflows.

| Prompt | Purpose | Arguments |
|--------|---------|-----------|
| `constitutional_eval` | Full F1-F13 evaluation workflow | `query` |
| `paradox_analysis` | 9-paradox equilibrium analysis | `query` |
| `trinity_full` | Complete 000-999 metabolic loop walkthrough | `query` |
| `floor_violation_repair` | SABAR/VOID remediation guide | `floor`, `verdict`, `query` |
| `constitutional_summary` | Quick F1-F13 reference | (none) |

### Using Prompts

```python
# Get constitutional evaluation prompt
prompt = await client.get_prompt("constitutional_eval", {
    "query": "Should we deploy this feature?"
})
# Returns templated prompt with F1-F13 evaluation framework

# Get violation repair guidance
repair = await client.get_prompt("floor_violation_repair", {
    "floor": "F7",
    "verdict": "SABAR",
    "query": "Original query here"
})
```

---

## Architecture (v55.1)

```
┌─────────────────────────────────────────────────────────────┐
│  MCP CLIENT (Claude / GPT / Gemini / Cursor)                │
└──────────────────────┬──────────────────────────────────────┘
                       │ JSON-RPC 2.0
┌──────────────────────▼──────────────────────────────────────┐
│  TRANSPORT LAYER                                            │
│  ├─ StdioTransport  → stdin/stdout (local clients)          │
│  └─ SSETransport    → Streamable HTTP (production)          │
│     stateless_http=True, json_response=True                 │
├─────────────────────────────────────────────────────────────┤
│  MCP PRIMITIVES                                             │
│  ├─ Tools (7 canonical)  → model-controlled execution       │
│  ├─ Resources (17)       → application-driven context       │
│  └─ Prompts (5)          → user-controlled templates        │
├─────────────────────────────────────────────────────────────┤
│  REGISTRIES (Single Source of Truth)                        │
│  ├─ ToolRegistry      → core/tool_registry.py               │
│  ├─ ResourceRegistry  → core/resource_registry.py           │
│  └─ PromptRegistry    → core/prompt_registry.py             │
├─────────────────────────────────────────────────────────────┤
│  GOVERNANCE BRIDGE → arifOS Kernels                         │
│  AGI (Δ Mind) → ASI (Ω Heart) → APEX (Ψ Soul) → VAULT-999   │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure (v55.1)

```
mcp/
├── core/                   # Protocol layer
│   ├── tool_registry.py    # 7 canonical tools (SSOT)
│   ├── resource_registry.py # MCP Resources (F1-F13, VAULT)
│   └── prompt_registry.py  # MCP Prompts (templates)
├── transports/             # Transport implementations
│   ├── base.py            # BaseTransport ABC
│   ├── stdio.py           # StdioTransport (local)
│   └── sse.py             # SSETransport (Streamable HTTP)
├── entrypoints/           # CLI entry points
│   ├── stdio_entry.py
│   └── sse_entry.py
├── adapters/              # Model adapters (Anthropic, OpenAI, Google)
├── tools/                 # 7 canonical tool handlers
│   └── canonical_trinity.py
├── services/              # Rate limiting, metrics, ledger
├── external_gateways/     # External integrations (Brave Search)
├── config/                # Configuration management
├── config/                # Configuration management
└── README.md             # This file
```

### Key Architectural Patterns

1. **TRANSPORT ABSTRACTION**
   All transports implement `BaseTransport`. Transports (stdio, SSE, HTTP) are PLUGGABLE and HOT-SWAPPABLE.

2. **MODEL ADAPTER PATTERN**
   Adapters (`BaseModelAdapter`) handle model-specific quirks (Claude vs GPT vs Gemini) WITHOUT changing core logic.

3. **CLIENT ADAPTER PATTERN**
   Clients (`BaseClientAdapter`) are AUTO-DETECTED at startup to configure capabilities (Claude Desktop vs Cursor).

4. **PLUGGABLE SESSION BACKENDS**
   Session storage is backend-agnostic (Memory, File, Redis, SQLite).

### Key Design Principles

1. **MCP Spec Compliance** — Full implementation of 2025-11-25 spec: Tools, Resources, Prompts
2. **Streamable HTTP** — Stateless transport for production, backward compatible with stdio
3. **Three Registries** — Tool, Resource, Prompt registries provide single source of truth
4. **Constitutional Hardening** — Every call passes through F1-F13 floor validation
5. **Model Agnosticism** — No AI model assumes privileged position

---

## MCP Spec Compliance

| Feature | Status | Spec Version |
|---------|--------|--------------|
| Tools with outputSchema | ✅ | 2025-06-18 |
| Tool annotations (readOnlyHint, etc.) | ✅ | 2025-11-25 |
| Tool title | ✅ | 2025-11-25 |
| Streamable HTTP transport | ✅ | 2025-03-26 |
| MCP-Protocol-Version header | ✅ | 2025-11-25 |
| Mcp-Session-Id header | ✅ | 2025-03-26 |
| Resources | ✅ | 2025-11-25 |
| Prompts | ✅ | 2025-11-25 |
| Stateful + Stateless modes | ✅ | 2025-03-26 |

---

## Compatibility Matrix

| Category | Supported |
|----------|-----------|
| **AI Models** | Claude, GPT-4, Gemini, Kimi K2.5, Llama, SEA-LION, any JSON-RPC |
| **MCP Clients** | Claude Desktop, Cursor, VS Code, Windsurf, ChatGPT Dev, any MCP client |
| **Transports** | stdio, Streamable HTTP (spec 2025-03-26+) |
| **Spec Versions** | 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25 |
| **Platforms** | Linux, macOS, Windows |
| **Python** | 3.10, 3.11, 3.12, 3.13 |
| **Session Backends** | Memory, File (JSON), Redis, SQLite |

---

## Development

```bash
# Run all MCP tests (69 tests)
pytest tests/test_mcp_v55.py -v

# Run specific test categories
pytest tests/test_mcp_v55.py::TestToolRegistry -v
pytest tests/test_mcp_v55.py::TestResourceRegistry -v
pytest tests/test_mcp_v55.py::TestPromptRegistry -v
pytest tests/test_mcp_v55.py::TestFloorValidators -v

# Legacy tests
pytest tests/test_all_mcp_tools.py -v

# Lint & format
ruff check codebase/mcp/
black codebase/mcp/ --line-length=100

# Type check
mypy codebase/mcp/ --ignore-missing-imports
```

---

## Health Check

```bash
# Local
curl http://localhost:8000/health

# Production
curl https://aaamcp.arif-fazil.com/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "version": "v55.1-AAA",
  "mode": "CODEBASE",
  "transport": "streamable-http",
  "tools": 7
}
```

---

## Constitutional Floors (F1-F13)

| # | Floor | What It Checks | Threshold | Type |
|---|-------|---------------|-----------|------|
| F1 | Amanah | Is the action reversible? | LOCK | Hard |
| F2 | Truth | Is it factually accurate? | ≥0.99 | Hard |
| F3 | Tri-Witness | Do Mind·Heart·Human agree? | ≥0.95 | Soft |
| F4 | Clarity | Does it reduce confusion? | ΔS≤0 | Hard |
| F5 | Peace² | Is it non-destructive? | ≥1.0 | Hard |
| F6 | Empathy | Does it serve the weakest? | κᵣ≥0.95 | Soft |
| F7 | Humility | Does it state uncertainty? | Ω₀∈[0.03,0.05] | Soft |
| F8 | Genius | Is intelligence governed? | G≥0.80 | Soft |
| F9 | Anti-Hantu | No false consciousness? | Φ≤0.30 | Hard |
| F10 | Ontology | Domain boundaries held? | LOCK | Hard |
| F11 | Authority | Identity verified? | LOCK | Hard |
| F12 | Hardening | Injection blocked? | ≥0.85 | Hard |
| F13 | Curiosity | Alternatives explored? | >0 | Guide |

---

## Migration from v55.0

If you're upgrading from v55.0:

1. **Transport**: SSE transport now uses Streamable HTTP (stateless by default)
   - Set `stateless_http=True` for horizontal scaling
   - Set `stateless_http=False` for session-based governance

2. **Resources**: New MCP Resources available
   - Access floor definitions via `config://floors`
   - Access VAULT ledger via `vault://ledger/latest`

3. **Prompts**: New MCP Prompts available
   - Use `constitutional_eval` template for F1-F13 evaluation

4. **Tests**: Run the new comprehensive test suite
   - `pytest tests/test_mcp_v55.py` (69 tests)

---

**Version:** v55.1 | **License:** AGPL-3.0 | **Author:** Muhammad Arif bin Fazil
**DITEMPA BUKAN DIBERI** — Forged, Not Given
