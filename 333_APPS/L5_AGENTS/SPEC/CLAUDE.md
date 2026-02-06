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

# Run MCP Server (2 transports)
python -m aaa_mcp            # stdio (default — Local Agents)
python -m aaa_mcp sse         # sse (Remote — Railway/Network)
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

**Async mode is `auto`** — all `async def test_*` functions are auto-detected without `@pytest.mark.asyncio` decorators. Physics is disabled globally in `tests/conftest.py` (use `enable_physics_for_apex_theory` fixture to opt-in).

Test files that still `import arifos` (the pre-v52 package name) or live under `tests/archive/` are auto-skipped by `conftest.py`.

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

The local MCP server package was renamed from `mcp/` → `aaa_mcp/` to avoid shadowing the MCP Python SDK (`mcp` v1.26.0 on PyPI). This distinction is the single most important thing to get right.

```python
# Local arifOS code — use aaa_mcp (with subdirectory paths)
from aaa_mcp.server import mcp
from aaa_mcp.core.constitutional_decorator import constitutional_floor
from aaa_mcp.core.engine_adapters import AGIEngine, ASIEngine, APEXEngine
from aaa_mcp.services.constitutional_metrics import store_stage_result
from aaa_mcp.sessions.session_ledger import SessionLedger

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
| `apex_verdict` | APEX | Final verdict (SEAL/VOID/SABAR) | F5, F3, F8 |
| `reality_search` | — | External fact-checking | F2, F7 |
| `vault_seal` | — | Merkle-chained immutable ledger record | F1, F3 |

**Tool pipeline flow:** `init_gate → agi_sense → agi_think → agi_reason → asi_empathize → asi_align → apex_verdict → vault_seal` (with `reality_search` callable from any stage).

### Verdict Hierarchy

```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```

- **SEAL**: All floors pass — approved to execute
- **VOID**: Hard floor failed — cannot proceed
- **888_HOLD**: High-stakes — needs human confirmation
- **PARTIAL**: Soft floor warning — proceed with caution
- **SABAR**: Floor violated — stop and repair first

### aaa_mcp/ Package Structure (Post-Cooling Refactor)

```
aaa_mcp/
├── __init__.py              # Package exports (9 tools, decorators, config)
├── __main__.py              # CLI entry: python -m aaa_mcp [stdio|sse]
├── server.py                # 9 tool definitions with @mcp.tool() + @constitutional_floor()
├── mcp_config.py            # External MCP server registry, TrinityComponent config
├── mcp_integration.py       # MCPIntegrationLayer for external server management
├── bridge.py                # Legacy bridge module (Ed25519, Shannon entropy)
├── asi_gateway.py           # ASI gateway layer
├── core/                    # Constitutional enforcement & engine wiring
│   ├── constitutional_decorator.py  # Floor enforcement decorator (the real one)
│   ├── engine_adapters.py           # Bridges tools to codebase engines + fallback stubs
│   ├── mode_selector.py             # MCPMode enum (stdio/sse)
│   └── tool_registry.py             # Tool registration management
├── services/                # Runtime services
│   ├── constitutional_metrics.py    # In-memory stage result storage, verdict logging
│   └── redis_client.py              # Redis session persistence (optional)
├── sessions/                # Session persistence & audit
│   ├── session_ledger.py            # VAULT999 Merkle hash-chained ledger
│   ├── session_dependency.py        # Session dependency management
│   └── archive/                     # 900+ sealed session JSON files
├── tools/                   # Tool implementation helpers
│   ├── canonical_trinity.py         # Trinity architecture validator
│   ├── reality_grounding.py         # Fact-checking (reality_search backend)
│   ├── trinity_validator.py         # Trinity pipeline validator
│   └── mcp_tools_v53.py            # v53 tool specs
├── infrastructure/          # System services
│   └── rate_limiter.py              # Rate limiting
├── external_gateways/       # External API clients
│   └── brave_client.py              # Brave Search API
└── transports/              # Transport implementations
    └── sse.py                       # SSE transport (Railway, legacy remote)
```

### Key Module Map (Rest of Repository)

| Path | Purpose |
|------|---------|
| `codebase/` | Core engines (AGI, ASI, APEX), stages, floors, guards |
| `codebase/stages/` | Metabolic loop stages (444-999) |
| `codebase/floors/` | Floor implementations (F1, F8, F10, F12 as standalone modules) |
| `codebase/guards/` | Hypervisor guards (ontology F10, nonce F11, injection F12) |
| `codebase/kernel.py` | KernelManager singleton — lazy-loads Trinity cores |
| `codebase/state.py` | SessionState — immutable copy-on-write pattern |
| `codebase/vault/persistence.py` | Ledger backend used by `vault_seal` tool |
| `333_APPS/` | Metabolic layers (L1-L7), skills, actions |
| `mcp_server/` | Config/integration layer (separate from `aaa_mcp/`) |
| `spec/` | **PRIMARY** constitutional source — JSON schemas, thresholds |
| `canon/` | **PRIMARY** sealed canonical law (`*_v38Omega.md` with SEALED status) |

### SessionState Pattern (Immutable Copy-on-Write)

```python
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")       # Returns NEW instance
new_state = state.set_floor_score(...)   # Returns NEW instance
# Never: state.field = value (mutation forbidden)
```

---

## Key Conventions

### Decorator Order on MCP Tools

**`@mcp.tool()` must be OUTER, `@constitutional_floor()` must be INNER.** FastMCP's `@mcp.tool()` stores a `FunctionTool(fn=wrapper)`. If the constitutional decorator is outer, FastMCP registers the unwrapped function and enforcement never runs.

```python
@mcp.tool()                              # OUTER — FastMCP registration
@constitutional_floor("F2", "F4")        # INNER — floor enforcement
async def my_new_tool(input: str, session_id: str = "") -> dict:
    ...
```

### Floor Types and Enforcement

- **Hard floors** (F1, F2, F6, F7, F10, F11, F12, F13): Failure → **VOID** (blocked)
- **Soft floors** (F3, F4, F5, F8, F9): Failure → **PARTIAL** (warn, proceed with caution)
- **Pre-execution floors** (F1, F5, F11, F12, F13): Validate INPUT before tool runs
- **Post-execution floors** (F2, F3, F4, F6, F7, F8, F9, F10): Validate OUTPUT after tool runs

### Engine Adapters: Real Engines with Fallback Stubs

`aaa_mcp/core/engine_adapters.py` tries to import real engines from `codebase/`. When unavailable, it uses fallback stubs that compute heuristic scores from query text (Shannon entropy, lexical diversity, etc.) rather than returning hardcoded values.

```python
try:
    from codebase.agi.engine import AGIEngine as RealAGIEngine
    AGI_AVAILABLE = True
except ImportError:
    AGI_AVAILABLE = False  # Falls back to heuristic stub
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

### APEX Solver Uses Geometric Mean

The 9-paradox solver uses geometric mean (GM), not arithmetic. GM punishes imbalance. Target: GM >= 0.85, std dev <= 0.10.

---

## Adding New Components

### New MCP Tool

1. Add tool function with `@mcp.tool()` (outer) and `@constitutional_floor()` (inner) in `aaa_mcp/server.py`
2. Add engine handler in `aaa_mcp/core/engine_adapters.py` (with fallback stub)
3. Update `FLOOR_ENFORCEMENT` dict in `aaa_mcp/core/constitutional_decorator.py`
4. Add tests in `tests/test_mcp_all_tools.py`

### New Floor Validator

1. Create module in `codebase/floors/fX_name.py`
2. Export from `codebase/floors/__init__.py`
3. Wire into `codebase/enforcement/floor_validators.py`
4. Add tests in `tests/constitutional/`

---

## Known Gotchas

- **F4/F6 numbering swap**: CLAUDE.md and `constitutional_floors.py` historically had F4 (Empathy) and F6 (Clarity) swapped. Check the actual `FLOOR_ENFORCEMENT` dict in `constitutional_decorator.py` for truth.
- **vault_seal KeyError**: `vault_seal` in `server.py` can crash on `result["seal"]` if the persistence backend returns unexpected format — use `.get("seal", fallback)`.
- **test_mcp_all_tools.py**: 3 pre-existing assertion failures (stub returns `confidence=0.92` but tests assert `0.99`). These are known and non-blocking.
- **Dual init paths**: `bridge.py` (Ed25519 + Shannon entropy + APEX summary) vs `codebase/init/000_init/init_000.py` (loop manager + canonical bootstrap) have drifted. `server.py` uses `engine_adapters.py`, not either directly.
- **`333_APPS/L4_TOOLS/mcp/`** is LEGACY — still has old `from mcp.` imports. Not critical, do not fix.
- **F2 Truth gotcha**: Don't default `truth_score` in decorator context — `F2_Truth` has internal logic (defaults to 1.0) which is correct for stubs. Only engine results should override.

## Environment & Config

- **Windows environment** — use PowerShell for commands, watch quoting issues with `$env:` in nested `-Command` strings
- **MCP config locations:** `.mcp.json` (root), `.claude/mcp.json`, `.agents/mcp.json`
- **Test env vars** (set automatically by `tests/conftest.py`): `ARIFOS_PHYSICS_DISABLED=1`, `ARIFOS_ALLOW_LEGACY_SPEC=1`
- **Dependencies:** FastMCP 2.14.4, MCP SDK 1.26.0, Python 3.12 (supports 3.10+)
