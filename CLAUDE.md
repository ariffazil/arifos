# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<<<<<<< HEAD
**Project:** arifOS — Constitutional AI governance system (AAA MCP Server)
**Package:** `arifos` (PyPI)
**Python:** >=3.10
**License:** AGPL-3.0-only
=======
**Project:** arifOS — Constitutional AI Governance System
**Package:** `arifos` v64.2.0 (PyPI)
**Python:** >=3.10 | **License:** AGPL-3.0-only
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## Build & Dev Commands

```bash
# Install (editable with dev dependencies)
pip install -e ".[dev]"

<<<<<<< HEAD
# Run MCP Server
aaa-mcp-stdio              # stdio transport (Claude Desktop)
aaa-mcp-sse                # SSE transport (HTTP clients)
aaa-mcp                    # auto-detect mode (dispatches based on arg: stdio/http/sse)

# Alternative entry
python -m mcp
python -m mcp http --port 8080
python -m mcp sse --port 3000

# Docker
docker build -t arifos:latest .
docker run -e PORT=8000 -p 8000:8000 arifos:latest
=======
# Run MCP Server (3 transports)
python -m aaa_mcp              # stdio (default — Claude Desktop, local agents)
python -m aaa_mcp sse          # SSE (Railway, remote HTTP clients)
python -m aaa_mcp http         # Streamable HTTP at /mcp

# Alternative CLI entry points (from pyproject.toml [project.scripts])
aaa-mcp                        # same as python -m aaa_mcp
aclip-cai health               # ACLIP infrastructure CLI
aclip-server                   # ACLIP MCP server mode
arifos-router                  # Unified gateway (AAA-MCP + ACLIP-CAI)

# Docker
docker build -t arifos .
docker run -e PORT=8080 -p 8080:8080 arifos
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c
```

## Testing

```bash
# Full suite
<<<<<<< HEAD
pytest tests/ -v --cov=codebase --cov-report=html

# Single file
pytest tests/test_precision.py -v

# Single test function
pytest tests/test_precision.py::test_function_name -v
=======
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=codebase --cov-report=html

# Single file / single test
pytest tests/test_quick.py -v
pytest tests/test_core_foundation.py::test_function_name -v
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c

# By marker
pytest -m constitutional       # F1-F13 floor tests
pytest -m integration          # Integration tests
pytest -m slow                 # Long-running tests

# Quick MCP smoke test
<<<<<<< HEAD
pytest tests/test_mcp_quick.py -v

# v55 tools integration
pytest tests/test_handlers_v55.py -v
pytest tests/test_phase3_transport.py -v

# Debug constitutional failure
pytest tests/constitutional/test_01_core_F1_to_F13.py -v -k "f1"
```

Async mode is `auto` (configured in pyproject.toml) — all `async def test_*` functions are auto-detected without `@pytest.mark.asyncio` decorators. Test paths: `tests/` and `arifos/tests/`. If async tests fail, ensure `pytest-asyncio` is installed (not in dev extras — install manually if needed).
=======
pytest tests/test_quick.py -v

# E2E pipeline
pytest tests/test_e2e_all_tools.py -v
pytest tests/test_e2e_core_to_aaa_mcp.py -v
```

Async mode is `auto` in pyproject.toml — async test functions are auto-detected without `@pytest.mark.asyncio` decorators. Test paths: `tests/` and `arifos/tests/`.
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c

## Linting & Formatting

```bash
<<<<<<< HEAD
black codebase/ --line-length=100
ruff check codebase/
ruff check codebase/ --fix
mypy codebase/ --ignore-missing-imports
```

**Style:** Black (100 char line length), Ruff (py310 target), MyPy strict on governance modules.
Ruff excludes `archive/**`, `archive_local/**`, `tests/**`.

---

## Architecture: AAA Trinity

Three independent engines process in isolation, then converge at stage 444:

```
000_INIT -> AGI (Delta) -> ASI (Omega) -> APEX (Psi) -> 999_VAULT
   ^        111-333     444-666     888         |
   +---------------- 000<->999 Loop ------------+
```

| Engine | Dir | Role | Entry Point | Floors |
|--------|-----|------|-------------|--------|
| **AGI (Delta)** | `codebase/agi/` | Reasoning — precision, hierarchy, active inference | `engine_hardened.py` | F2, F4, F7, F10 |
| **ASI (Omega)** | `codebase/asi/` | Safety — empathy, stakeholder care | `engine_hardened.py` | F1, F5, F6, F9 |
| **APEX (Psi)** | `codebase/apex/` | Judgment — 9-paradox equilibrium solver | `kernel.py` (APEXJudicialCore) | F3, F8, F11, F12 |

### Thermodynamic Wall (Critical Design Constraint)

AGI and ASI **cannot see each other's reasoning** until stage 444 (TRINITY_SYNC). Enforced through bundle isolation:

- **DeltaBundle** (`bundles.py`): AGI output — precision, hypotheses, entropy. Immutable after creation.
- **OmegaBundle** (`bundles.py`): ASI output — stakeholders, empathy kappa_r, reversibility. Immutable after creation.
- **MergedBundle** (`bundles.py`): Created at 444 via `compute_consensus()` and `apply_trinity_dissent_law()`.

Never cross bundles — AGI logic stays in Delta, ASI in Omega.

### KernelManager (`codebase/kernel.py`)

Singleton orchestrator that lazy-loads Trinity cores via bridge adapters:
- `AGINeuralCore` wraps `AGIEngineHardened` (lazy)
- `ASIActionCore` wraps `ASIEngineHardened` (lazy)
- `APEXJudicialCore` imported directly from `codebase.apex.kernel`
- `init_session()` delegates to `codebase.init.mcp_000_init` (canonical 7-step), falls back to native stub

### SessionState (`codebase/state.py`)

Immutable copy-on-write pattern:
```python
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")       # Returns new instance
new_state = state.set_floor_score(...)   # Returns new instance
# Never: state.field = value (mutation forbidden)
```

`SessionStore` provides in-memory L0 hot storage via `get()`/`put()`/`delete()`.

### Trinity Agent Roles

Claude Code operates as the **ENGINEER (Ω)** at stages 444-666, responsible for implementation with safety. The other roles:
- **ARCHITECT (Δ/Mind)** — stages 111-333 (governed by GEMINI.md)
- **AUDITOR+VALIDATOR (👁+Ψ/Soul)** — stages 888-999 (governed by AGENTS.md)

Handoff chain: DeltaBundle → OmegaBundle → Judgment + Seal.

---

## MCP Server Structure

### Entry Points (pyproject.toml scripts)

```
aaa-mcp       -> mcp.__main__:main        # Auto-detect dispatcher
aaa-mcp-stdio -> mcp.entrypoints.stdio_entry:main
aaa-mcp-sse   -> mcp.entrypoints.sse_entry:main
```

### Transports

| Transport | Command | Use Case |
|-----------|---------|----------|
| stdio | `aaa-mcp-stdio` | Claude Desktop, local tools |
| SSE | `aaa-mcp-sse` | HTTP clients, remote |
| Streamable HTTP | `aaa-mcp` (auto) | Production (MCP spec 2025-03-26+) |

### 9 Canonical MCP Tools (v55 — `codebase/mcp/core/tool_registry.py`)

v55 split the old 7 multi-action tools into 9 explicit, LLM-friendly tools. All accept `session_id` for chaining multi-step workflows.

| Tool | Engine | Purpose | Floors |
|------|--------|---------|--------|
| `init_gate` | — | Session ignition, injection scan (F12), authority check | F11, F12 |
| `agi_sense` | AGI | Parse input, detect intent, classify lane (HARD/SOFT/PHATIC) | F12 |
| `agi_think` | AGI | Generate hypotheses/options without committing | F4 |
| `agi_reason` | AGI | Deep logical reasoning chain (modes: default/atlas/physics/forge) | F2, F4, F7, F10 |
| `asi_empathize` | ASI | Stakeholder impact, vulnerability scores, weakest stakeholder | F5, F6, F9 |
| `asi_align` | ASI | Ethics/law/policy reconciliation | F9 |
| `apex_verdict` | APEX | Final constitutional verdict (SEAL/VOID/SABAR) | F3, F8, F11 |
| `reality_search` | — | External fact-checking via Brave Search | F7, F10 |
| `vault_seal` | — | Merkle-tree immutable ledger | F1 |

**Implementation:** Tool definitions live in `tool_registry.py`. Handlers delegate to `canonical_trinity.py` functions (`mcp_init`, `mcp_agi`, `mcp_asi`, `mcp_apex`, `mcp_vault`, `mcp_reality`) via lambda wrappers with action parameters.

**Legacy tools** (`_init_`, `_agi_`, `_asi_`, `_apex_`, `_reality_`, `_trinity_`, `_vault_`): Still functional in `canonical_trinity.py`, deprecated since v55, removal planned for v56.

### MCP Resources & Prompts

Resources (read-only constitutional data):
- `config://floors` — All 13 floor definitions
- `floor://{F1-F13}` — Individual floor details
- `vault://ledger/latest` — Latest sealed decision

Prompts (reusable evaluation templates):
- `constitutional_eval` — Full F1-F13 evaluation
- `paradox_analysis` — 9-paradox equilibrium
- `trinity_full` — Complete 000-999 pipeline
- `floor_violation_repair` — SABAR/VOID remediation

### MCP Layer Structure (v55 refactoring in progress)

```
codebase/mcp/
+-- core/           # Protocol layer
|   +-- bridge.py       # 25KB monolith (being split)
|   +-- tool_registry.py  # 9-tool definitions (v55)
|   +-- validators.py     # Input validation (v55)
+-- transports/     # stdio, sse, base
+-- services/       # rate_limiter, immutable_ledger, metrics
+-- infrastructure/ # redis_client
+-- config/         # modes
+-- entrypoints/    # stdio_entry, sse_entry
+-- tools/          # canonical_trinity.py handlers + mcp_tools_v53.py (28KB internal engine)
+-- maintenance.py  # Maintenance utilities
```

Key monoliths to be aware of: `core/bridge.py` (25KB) and `tools/mcp_tools_v53.py` (28KB).
=======
black codebase/ aaa_mcp/ core/ --line-length=100
ruff check codebase/ aaa_mcp/ core/
ruff check codebase/ aaa_mcp/ core/ --fix
mypy codebase/ --ignore-missing-imports
```

Black: 100 char line length. Ruff: py310 target, excludes `archive/**`, `tests/**`. MyPy: strict on governance modules (see pyproject.toml overrides).

---

## Architecture

### Kernel + Adapter Pattern

```
core/                    → KERNEL (all decision logic, zero transport deps)
├── governance_kernel.py → GovernanceKernel (unified Ψ state, 9,128 lines)
├── judgment.py          → judge_cognition, judge_empathy, judge_apex
├── uncertainty_engine.py→ Ω₀ calculation (harmonic/geometric mean)
├── telemetry.py         → 30-day locked adaptation with drift tracking
├── pipeline.py          → Constitutional pipeline orchestrator
├── shared/              → 4 foundation modules (physics, atlas, types, crypto)
└── organs/              → 5 enforcement organs (_0_init → _4_vault)

aaa_mcp/                 → ADAPTER (transport only, NO decision logic)
├── server.py            → FastMCP server with 9 hardened skills (tools)
├── __main__.py          → CLI entry: stdio/sse/http dispatcher
├── rest.py              → REST API bridge
├── core/                → Heuristics, state management
├── capabilities/        → t6_web_search (Brave), code analysis
├── integrations/        → Container tools (VPS only)
└── vault/               → Audit logging adapter

codebase/                → LEGACY engine layer (still used by adapter)
├── agi/                 → AGI engine (engine_hardened.py = v53.4 LIVE)
├── asi/                 → ASI engine (engine_hardened.py)
├── apex/                → APEX kernel (APEXJudicialCore, 9-paradox solver)
├── init/                → mcp_000_init (canonical 7-step session init)
├── floors/              → F1, F8, F10, F12 standalone floor modules
├── guards/              → F10 ontology, F11 nonce, F12 injection guards
├── stages/              → 444-999 metabolic loop stages
├── vault/               → Merkle-tree immutable ledger
└── shared/              → Bundles (DeltaBundle, OmegaBundle, MergedBundle)

aclip_cai/               → 9-Sense Infrastructure Console (read-only sensory layer)
333_APPS/                → 7-Layer Application Stack (L1 Prompts → L7 AGI)
VAULT999/                → Immutable ledger storage (AAA_HUMAN, BBB_LEDGER, CCC_CANON)
```

**Critical boundary:** `core/` has zero transport dependencies. `aaa_mcp/` has zero decision logic. Never cross this boundary.

### Trinity Architecture (ΔΩΨ)

Three engines process in isolation, then converge:

```
000_INIT → AGI(Δ) Mind → ASI(Ω) Heart → APEX(Ψ) Soul → 999_VAULT
             111-333        555-666          888              999
```

- **AGI (Δ/Delta)**: Reasoning — truth (F2), clarity (F4), humility (F7), genius (F8)
- **ASI (Ω/Omega)**: Safety — amanah (F1), peace (F5), empathy (F6), anti-hantu (F9)
- **APEX (Ψ/Psi)**: Judgment — tri-witness (F3), ontology (F10), authority (F11), injection (F12), sovereignty (F13)

**Bundle isolation**: AGI and ASI cannot see each other's reasoning until stage 444 (TRINITY_SYNC). DeltaBundle and OmegaBundle are immutable after creation; they merge via `compute_consensus()`.

### SessionState (Copy-on-Write)

`codebase/state.py` — immutable pattern:
```python
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")       # Returns new instance
# Never: state.field = value  (mutation forbidden)
```

---

## 9 Canonical MCP Tools (v64.1 — "Hardened Skills")

All defined in `aaa_mcp/server.py` with `@mcp.tool()` decorators:

| Tool | Stage | Floors | Purpose |
|------|-------|--------|---------|
| `anchor` | 000 | F11, F12 | Session init, injection scan, authority check |
| `reason` | 222 | F2, F4, F8 | Hypothesize & analyze (truth, clarity) |
| `integrate` | 333 | F7, F10 | Map context, ground in evidence |
| `respond` | 444 | F4, F6 | Draft response (clarity, empathy) |
| `validate` | 555 | F5, F6, F1 | Stakeholder impact check |
| `align` | 666 | F9 | Ethics check (anti-hantu) |
| `forge` | 777 | F2, F4, F7 | Synthesize solution |
| `audit` | 888 | F3, F11, F13 | Verdict & consensus (SEAL/VOID/SABAR) |
| `seal` | 999 | F1, F3 | Commit to VAULT999 immutable ledger |
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c

---

## Constitutional Floors (F1-F13)

<<<<<<< HEAD
13 safety rules enforced at code level. Hard floors block execution (VOID); soft floors warn (PARTIAL).

| Floor | Name | Type | Threshold | Key File(s) |
|-------|------|------|-----------|-------------|
| F1 | Amanah (Reversibility) | Hard | LOCKED | `codebase/floors/amanah.py` |
| F2 | Truth | Hard | tau >= 0.99 | `codebase/enforcement/floor_validators.py` |
| F4 | Clarity | Hard | delta_S <= 0 | AGI hierarchy check |
| F5 | Peace² | Soft | >= 1.0 | ASI engine |
| F6 | Empathy | Soft | kappa_r >= 0.95 | ASI engine |
| F7 | Humility | Hard | Omega_0 in [0.03,0.05] | AGI precision check |
| F8 | Genius | Derived | G >= 0.80 | `codebase/floors/genius.py` |
| F9 | Anti-Hantu (C_dark) | Soft | < 0.30 | ASI engine |
| F10 | Ontology | Hard | — | `codebase/floors/ontology.py`, `codebase/guards/ontology_guard.py` |
| F11 | Command Auth | Hard | — | `codebase/guards/nonce_manager.py` |
| F12 | Injection | Hard | < 0.85 | `codebase/floors/injection.py`, `codebase/guards/injection_guard.py` |
| F13 | Sovereign | Hard | — | APEX kernel |

**Implementation status:** `codebase/floors/` has F1, F8, F10, F12 as standalone modules. Remaining floors are enforced within engine code and `enforcement/floor_validators.py`.

**Authoritative thresholds:** Always verify against `spec/` schemas (PRIMARY source), not this table.

---

## Guards (`codebase/guards/`)

Hypervisor-level guards for floors F10-F12:
- `ontology_guard.py` — F10: Prevents consciousness claims, reality confusion
- `nonce_manager.py` — F11: Nonce-based identity verification for auth commands
- `injection_guard.py` — F12: Blocks prompt injection patterns
- `session_dependency.py` — Session validation

---

## Stages (`codebase/stages/`)

The 000-999 metabolic loop. Early stages (000-333) handled in `codebase/init/` and engine modules:

- `stage_444.py` / `stage_444_trinity_sync.py` — Trinity convergence (DeltaBundle + OmegaBundle → MergedBundle)
- `stage_555.py` — Empathy (kappa_r calculation)
- `stage_666.py` / `stage_666_bridge.py` — Alignment (Peace²)
- `stage_777_forge.py` — Society/Justice
- `stage_888_judge.py` — APEX 9-paradox judgment
- `stage_889_proof.py` — Proof generation
- `stage_999_seal.py` — Vault seal (Merkle tree)
=======
13 safety rules: 9 Floors + 2 Mirrors + 2 Walls. Hard floors → VOID (block). Soft floors → PARTIAL (warn).

| Floor | Name | Type | Threshold |
|-------|------|------|-----------|
| F1 | Amanah (Reversibility) | Hard | LOCKED |
| F2 | Truth | Hard | τ ≥ 0.99 |
| F3 | Tri-Witness | Mirror | ≥ 0.95 |
| F4 | Clarity (ΔS) | Hard | ΔS ≤ 0 |
| F5 | Peace² | Soft | ≥ 1.0 |
| F6 | Empathy (κᵣ) | Soft | κᵣ ≥ 0.70 |
| F7 | Humility (Ω₀) | Hard | 0.03–0.05 |
| F8 | Genius (G) | Mirror | G ≥ 0.80 |
| F9 | Anti-Hantu (C_dark) | Soft | < 0.30 |
| F10 | Ontology | Wall | LOCKED |
| F11 | Command Auth | Wall | LOCKED |
| F12 | Injection Defense | Hard | < 0.85 |
| F13 | Sovereign | Veto | HUMAN |

**Execution order:** F12→F11 (Walls) → AGI Floors (F1,F2,F4,F7) → ASI Floors (F5,F6,F9) → Mirrors (F3,F8) → Ledger

**Verdict hierarchy:** `SABAR > VOID > 888_HOLD > PARTIAL > SEAL`
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c

---

## Key Conventions

<<<<<<< HEAD
### 1. Lazy Imports for Optional Dependencies
=======
### Import Namespacing
- `aaa_mcp.*` — local constitutional MCP code
- `mcp.*` — external MCP SDK (v1.26.0). **Never** shadow with local modules
- `core.*` — canonical kernel imports (`from core.shared.physics import W_3`)
- `codebase.*` — legacy engine layer (still functional)

### Decorator Order (Critical)
```python
@mcp.tool()                    # OUTER — FastMCP registers this
@constitutional_floor("F2")   # INNER — enforcement runs at call time
async def my_tool(...):
```
If reversed, FastMCP registers the unwrapped function and enforcement never runs.

### Lazy Imports for Optional Dependencies
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c
```python
try:
    import numpy as np
except ImportError:
    np = None
```
<<<<<<< HEAD
Never crash on import for optional deps. Core dependencies: numpy, pydantic, anyio, starlette, fastmcp, mcp, fastapi, uvicorn.

### 2. Source Verification for Constitutional Claims

Before making ANY constitutional claim, verify against PRIMARY sources:

1. **PRIMARY (Required):** `spec/*.json`, `canon/*_v38Omega.md` (SEALED status)
2. **SECONDARY:** `codebase/*.py` (implementation reference)
3. **TERTIARY:** `docs/*.md`, `README.md` (informational, may lag behind PRIMARY)
4. **NOT EVIDENCE:** grep/search results, code comments, this file

If you cannot answer "Which PRIMARY source did I read?" then you have NOT verified. See `.github/copilot-instructions.md` for the full A CLIP enforcement protocol (v41.2).

### 3. Verdict Hierarchy
```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```
- **SEAL**: All floors pass, approved
- **VOID**: Hard floor failed, cannot proceed
- **888_HOLD**: High-stakes, needs human confirmation
- **PARTIAL**: Soft floor warning, proceed with caution
- **SABAR**: Floor violated, stop and repair

### 4. Geometric Mean, Not Arithmetic
The 9-paradox APEX solver uses geometric mean (GM) for synthesis. GM punishes imbalance more than arithmetic mean. Target: GM >= 0.85, std dev <= 0.10.

### 5. Code-Level Floor Enforcement (Phoenix-72 Amendment)

Floors apply to **generated code**, not just statements:
=======
Never crash on import for optional deps.

### Code-Level Floor Enforcement
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c

| Floor | Code Smell | Fix |
|-------|------------|-----|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
<<<<<<< HEAD
| F3 | Contract mismatch, type lies | Use canonical interfaces |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F5 | Destructive defaults, no backup | Safe defaults, preserve state |
| F6 | Only happy path, cryptic errors | Handle edge cases, clear messages |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F8 | Bypasses governance, invents patterns | Use established systems |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

---

## Common Tasks

```bash
# Add new MCP tool
# 1. Add ToolDefinition in codebase/mcp/core/tool_registry.py
# 2. Create/update handler in codebase/mcp/tools/canonical_trinity.py
# 3. Add tests in tests/test_all_mcp_tools.py

# Add new floor validator
# 1. Create module in codebase/floors/fX_name.py
# 2. Export from codebase/floors/__init__.py
# 3. Wire into enforcement/floor_validators.py
# 4. Add tests in tests/constitutional/
```

---

**Version:** v55.1-TRANSITION
**Live:** https://arif-fazil.com
**Repo:** https://github.com/ariffazil/arifOS
=======
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

### APEX Solver
Uses geometric mean (not arithmetic) for 9-paradox synthesis. GM punishes imbalance more harshly. Target: GM ≥ 0.85, std dev ≤ 0.10.

---

## Adding New Components

### New MCP Tool
1. Add `@mcp.tool()` definition in `aaa_mcp/server.py`
2. Wire kernel logic via `core/` imports (not inline decision logic)
3. Add floor mapping in `get_tool_floors()` in server.py
4. Add tests in `tests/`

### New Constitutional Floor
1. Create module in `codebase/floors/fX_name.py`
2. Export from `codebase/floors/__init__.py`
3. Wire into `codebase/enforcement/floor_validators.py`
4. Add tests in `tests/constitutional/`

### New Core Organ
1. Create `core/organs/_X_name.py`
2. Import only from `core.shared.*` (no cross-organ deps)
3. Return ConstitutionalTensor with floor scores
4. Update `core/organs/__init__.py` exports
5. Add tests in `tests/core/`

---

## Known Gotchas

- **Namespace collision**: `mcp/` directory at repo root is Docker configs, NOT the SDK. Local code is `aaa_mcp/`. Never name a local package `mcp`.
- **Dual engine**: `codebase/agi/engine.py` (v52 compat) vs `engine_hardened.py` (v53.4 LIVE). The hardened version is the active one.
- **F4/F6 numbering**: Differs between CLAUDE.md and `constitutional_floors.py` (swapped in some docs). Verify against `aaa_mcp/server.py` floor mappings.
- **Windows environment**: Use PowerShell. `$env:` syntax breaks in nested `-Command` strings.
- **pyproject.toml packages**: Must NOT include `mcp*` (would re-shadow the SDK).
- **vault_seal**: `result["seal"]` KeyError is pre-existing in some code paths.
- **mcp_bridge.py**: Has `_measure_entropy()` Shannon function that is NOT wired to Step 4.

---

## Deployment

| Target | Command | Notes |
|--------|---------|-------|
| Local (stdio) | `python -m aaa_mcp` | Claude Desktop, Cursor IDE |
| Railway (SSE) | Auto-deploys from GitHub | `railway.toml`, port 8080 |
| VPS (Production) | `systemd aaa-mcp.service` | Docker: qdrant, openclaw, arifos |
| Docker | `docker build -t arifos . && docker run -p 8080:8080 arifos` | |

**Live endpoints:**
- Health: `https://arifosmcp.arif-fazil.com/health`
- MCP: `https://arifosmcp.arif-fazil.com/mcp`

**MCP config files:** `.mcp.json` (root), `.claude/mcp.json`, `.agents/mcp.json`

---

**Version:** v64.2.0-GAGI | **Repo:** https://github.com/ariffazil/arifOS
>>>>>>> 68c473264dad3e522261ce3c1431a646e6eaeb6c
