# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Project:** arifOS — Constitutional AI governance system (AAA MCP Server)
**Package:** `arifos` v55.5.0 (editable install)
**Python:** >=3.10 | **License:** AGPL-3.0-only
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## Build & Dev Commands

```bash
# Install (editable with dev dependencies)
pip install -e ".[dev]"

# Run MCP Server (3 transports)
python -m aaa_mcp            # stdio (default — Claude Code, Claude Desktop)
python -m aaa_mcp sse         # SSE (legacy remote/Railway)
python -m aaa_mcp http        # Streamable HTTP (ChatGPT, OpenAI, modern remote)
aaa-mcp                       # Console script equivalent (stdio default)
```

## Testing

```bash
# Full suite
pytest tests/ -v

# Quick smoke test (~3 min)
pytest tests/test_mcp_quick.py -v

# All MCP tool integration tests
pytest tests/test_mcp_all_tools.py -v

# Specific test file
pytest tests/mcp_tests/test_session_ledger.py -v

# Single test function
pytest tests/mcp_tests/test_metrics.py::test_constitutional_metrics -v

# By marker
pytest -m constitutional      # Floor enforcement tests
pytest -m integration         # Integration tests
pytest -m "not slow"          # Skip slow tests

# E2E pipeline
pytest tests/test_pipeline_e2e.py -v

# With coverage
pytest --cov=aaa_mcp tests/ -v
```

**Async mode is `auto`** — all `async def test_*` functions are auto-detected without `@pytest.mark.asyncio` decorators. Physics is disabled globally in `conftest.py` (use `enable_physics_for_apex_theory` fixture to opt-in).

Test files that still `import arifos` (the pre-v52 package name) are auto-skipped by `conftest.py`.

## Linting & Formatting

```bash
black --line-length 100 aaa_mcp/
ruff check aaa_mcp/
ruff check aaa_mcp/ --fix
mypy aaa_mcp/ --ignore-missing-imports
```

**Style:** Black (100 char lines), Ruff (py310 target, excludes `archive/**` and `tests/**`), MyPy strict on core governance modules.

---

## Critical: aaa_mcp vs mcp Import Distinction

The local MCP server package was renamed from `mcp/` to `aaa_mcp/` to avoid shadowing the MCP Python SDK.

```python
# Local arifOS code — use aaa_mcp
from aaa_mcp.server import mcp
from aaa_mcp.constitutional_decorator import constitutional_floor
from aaa_mcp.session_ledger import SessionLedger

# MCP SDK from PyPI — use mcp
from mcp import Client, StdioClientTransport
```

**`pyproject.toml` packages.find must NOT include `mcp*`** — that would re-shadow the SDK.

---

## Architecture

### Trinity Framework (Three Engines)

```
000_INIT → AGI(Δ) → ASI(Ω) → APEX(Ψ) → 999_VAULT
             111-333   444-666    777-888
```

| Engine | Role | Floors | Location |
|--------|------|--------|----------|
| **AGI (Δ)** | Mind — reasoning, precision, truth | F2, F4, F7, F10 | `codebase/agi/` |
| **ASI (Ω)** | Heart — empathy, safety, alignment | F1, F5, F6, F9 | `codebase/asi/` |
| **APEX (Ψ)** | Soul — judgment, 9-paradox equilibrium | F3, F8, F11, F12 | `codebase/apex/` |

**Thermodynamic wall:** AGI and ASI cannot see each other's reasoning until stage 444 (TRINITY_SYNC). Enforced via immutable `DeltaBundle` (AGI output) and `OmegaBundle` (ASI output) that merge into `MergedBundle` at convergence.

### 9 Canonical MCP Tools (v55)

All tools accept `session_id` for chaining multi-step workflows. Defined in `aaa_mcp/server.py` with `@constitutional_floor()` guards.

| Tool | Engine | Purpose | Key Floors |
|------|--------|---------|------------|
| `init_gate` | — | Session init + injection scan + auth check | F11, F12 |
| `agi_sense` | AGI | Parse input, detect intent, classify lane | F2, F4 |
| `agi_think` | AGI | Generate hypotheses without committing | F2, F4, F7 |
| `agi_reason` | AGI | Deep logical reasoning chain | F2, F4, F7 |
| `asi_empathize` | ASI | Stakeholder impact, vulnerability scoring | F5, F6 |
| `asi_align` | ASI | Ethics/law/policy reconciliation | F5, F6, F9 |
| `apex_verdict` | APEX | Final verdict (SEAL/VOID/SABAR) | F3, F8 |
| `reality_search` | — | External fact-checking | F2, F7 |
| `vault_seal` | — | Merkle-chained immutable ledger record | F1, F3 |

### Verdict Hierarchy

```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```

- **SEAL**: All floors pass — approved to execute
- **VOID**: Hard floor failed — cannot proceed
- **888_HOLD**: High-stakes — needs human confirmation
- **PARTIAL**: Soft floor warning — proceed with caution
- **SABAR**: Floor violated — stop and repair first

### Key Module Map

| Path | Purpose |
|------|---------|
| `aaa_mcp/` | Active MCP server (FastMCP-based, 9 tools) |
| `aaa_mcp/server.py` | Tool definitions with `@constitutional_floor()` |
| `aaa_mcp/engine_adapters.py` | Bridges FastMCP tools to real engine implementations |
| `aaa_mcp/constitutional_decorator.py` | Floor enforcement decorator |
| `aaa_mcp/session_ledger.py` | VAULT999 session persistence (Merkle hash-chaining) |
| `aaa_mcp/mcp_config.py` | External MCP server registry with constitutional mapping |
| `codebase/` | Core engines (AGI, ASI, APEX), stages, floors, guards |
| `codebase/stages/` | Metabolic loop stages (444-999) |
| `codebase/floors/` | Floor implementations (F1, F8, F10, F12 as standalone) |
| `codebase/guards/` | Hypervisor guards (ontology F10, nonce F11, injection F12) |
| `codebase/kernel.py` | KernelManager singleton — lazy-loads Trinity cores |
| `codebase/state.py` | SessionState — immutable copy-on-write pattern |
| `333_APPS/` | Metabolic layers (L1-L7), skills, actions |
| `vault_999/` | Immutable audit ledger (tamper-evident, hash-chained) |
| `mcp_server/` | Config/integration layer (separate from `aaa_mcp/`) |
| `spec/` | PRIMARY constitutional source — JSON schemas, thresholds |

### SessionState Pattern (Immutable Copy-on-Write)

```python
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")       # Returns NEW instance
new_state = state.set_floor_score(...)   # Returns NEW instance
# Never: state.field = value (mutation forbidden)
```

---

## Key Conventions

### Floor Enforcement on New Tools

Every new MCP tool must declare its constitutional floors:

```python
@mcp.tool()
@constitutional_floor("F2", "F4")
async def my_new_tool(input: str, session_id: str = "") -> dict:
    ...
```

### Lazy Imports for Optional Dependencies

```python
try:
    import numpy as np
except ImportError:
    np = None
```

Never crash on import for optional deps.

### Source Verification for Constitutional Claims

Before making constitutional claims, verify against PRIMARY sources:
1. **PRIMARY (Required):** `spec/*.json`, `canon/*_v38Omega.md` (SEALED status)
2. **SECONDARY:** `codebase/*.py` (implementation reference)
3. **TERTIARY:** `docs/*.md`, `README.md` (informational, may lag)
4. **NOT EVIDENCE:** grep/search results, code comments

### Code-Level Floor Enforcement (Phoenix-72 Amendment)

Floors apply to generated code, not just statements:

| Floor | Code Smell | Fix |
|-------|------------|-----|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

### APEX Solver Uses Geometric Mean

The 9-paradox solver uses geometric mean (GM), not arithmetic. GM punishes imbalance. Target: GM >= 0.85, std dev <= 0.10.

---

## Adding New Components

### New MCP Tool

1. Add tool function with `@mcp.tool()` and `@constitutional_floor()` in `aaa_mcp/server.py`
2. Create/update handler in engine adapters
3. Add tests in `tests/test_mcp_all_tools.py`

### New Floor Validator

1. Create module in `codebase/floors/fX_name.py`
2. Export from `codebase/floors/__init__.py`
3. Wire into `codebase/enforcement/floor_validators.py`
4. Add tests in `tests/constitutional/`

---

## Environment & Config

- **Windows environment** — use PowerShell for commands, watch quoting issues with `$env:` in nested `-Command` strings
- **MCP config locations:** `.mcp.json` (root), `.claude/mcp.json`, `.agents/mcp.json`
- **Test env vars** (set automatically by conftest): `ARIFOS_PHYSICS_DISABLED=1`, `ARIFOS_ALLOW_LEGACY_SPEC=1`
- **`333_APPS/L4_TOOLS/mcp/`** is LEGACY — still has old `from mcp.` imports (not critical, do not fix)
