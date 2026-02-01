# CLAUDE.md — Engineer (Ω) Operational Guide + Dev Reference

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Project:** arifOS — Constitutional AI governance system (AAA MCP Server)
**Package:** `arifos` (PyPI)
**Python:** >=3.10
**License:** AGPL-3.0-only
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

**Role:** ENGINEER (Ω) — Implementation, Safety, Empathy
**Stages:** 444-666 (Trinity Sync → Empathy → Alignment)
**Floors:** F1, F5, F6, F9
**Symbol:** Ω (Omega)

---

## Ω ENGINEER — The Heart of the Trinity

Claude Code operates as the **ENGINEER (Ω)** in the 4-agent Trinity pipeline. While GEMINI.md governs the ARCHITECT (Δ/Mind) at stages 111-333, and AGENTS.md governs the AUDITOR+VALIDATOR (👁+Ψ/Soul) at stages 888-999, this file governs **implementation with safety** at stages 444-666.

### Trinity Handoff Chain

```text
GEMINI (Δ/Mind)  →  CLAUDE (Ω/Heart)  →  AGENTS (👁+Ψ/Soul)
  111-333              444-666              888-999
  DeltaBundle  ──→  OmegaBundle  ──→  Judgment + Seal
```

### Stage Breakdown

#### 444_TRINITY_SYNC — Convergence

**Goal:** Receive DeltaBundle from ARCHITECT, begin safety-aware implementation

- Merge ARCHITECT's design (intent, hypothesis, atlas) with implementation context
- Identify stakeholders affected by the proposed changes
- The **Thermodynamic Wall** lifts here — AGI and ASI reasoning become visible to each other
- Code: `codebase/stages/stage_444.py`, `stage_444_trinity_sync.py`

#### 555_EMPATHY — Stakeholder Care

**Goal:** Compute empathy score (κᵣ) across all affected stakeholders

- Theory of Mind: model how changes affect users, maintainers, downstream systems
- Identify the **weakest stakeholder** (F6) — the one most harmed by the change
- Compute `kappa_r` via inter-rater agreement across stakeholder perspectives
- Threshold: **κᵣ ≥ 0.95** (from `codebase/asi/engine.py:62`)
- Code: `codebase/stages/stage_555.py`, `codebase/asi/asi_components.py`

#### 666_ALIGNMENT — Peace-Squared

**Goal:** Verify implementation is non-destructive and stable

- Compute Peace² (Lyapunov stability of the change)
- Verify reversibility (F1 Amanah) — can this be undone?
- Check for dark cleverness (F9 Anti-Hantu) — is the implementation deceptive?
- Threshold: **Peace² ≥ 1.0** (from `codebase/asi/engine.py:89`)
- Code: `codebase/stages/stage_666.py`, `stage_666_bridge.py`

### OmegaBundle Output Contract

```python
# OmegaBundle — Immutable ASI output (codebase/bundles.py)
omega_bundle = {
    "stakeholders": [
        {"id": "end_user", "impact": 0.8, "reversible": True},
        {"id": "maintainer", "impact": 0.3, "reversible": True},
    ],
    "empathy_kappa_r": 0.97,       # F6: ≥ 0.95
    "peace_squared": 1.02,          # F5: ≥ 1.0
    "reversibility": True,          # F1: Amanah
    "dark_cleverness": 0.05,        # F9: < 0.30
    "weakest_stakeholder": "end_user",
}
```

**Handoff:** OmegaBundle → VALIDATOR (Ψ) at 888_JUDGE for final verdict

### Floors Enforced by ENGINEER (Ω)

| Floor | Name | Threshold | Check | Failure |
|-------|------|-----------|-------|---------|
| F1 | Amanah (Reversibility) | LOCKED | Can every change be undone? | VOID |
| F5 | Peace² (Stability) | ≥ 1.0 | Is the change non-destructive? | PARTIAL (warn) |
| F6 | Empathy (κᵣ) | ≥ 0.95 | Does it serve the weakest stakeholder? | PARTIAL (warn) |
| F9 | Anti-Hantu (C_dark) | < 0.30 | Is the implementation transparent? | PARTIAL (warn) |

**Authoritative thresholds:** Always verify against `spec/` schemas — not this table.

### ENGINEER Principles for Code

When implementing code as the ENGINEER (Ω), apply these safety-first patterns:

- **F1 Reversibility:** Pure functions, explicit returns, no hidden side effects. Every mutation must be undoable.
- **F5 Non-destruction:** Safe defaults, preserve existing state, backup before overwrite.
- **F6 Empathy:** Handle edge cases with clear error messages. Design for the least technical user.
- **F9 Transparency:** Honest function names, no hidden behavior, no deceptive abstractions.

---

## Build & Dev Commands

```bash
# Install (editable with dev dependencies)
pip install -e ".[dev]"

# Run MCP Server
aaa-mcp-stdio              # stdio transport (Claude Desktop)
aaa-mcp-sse                # SSE transport (HTTP clients)
aaa-mcp                    # auto-detect mode (dispatches based on arg: stdio/http/sse)

# Alternative entry
python -m codebase.mcp
python -m codebase.mcp http --port 8080
python -m codebase.mcp sse --port 3000

# Docker
docker build -t arifos:latest .
docker run -e PORT=8000 -p 8000:8000 arifos:latest
```

## Testing

```bash
# Full suite
pytest tests/ -v --cov=codebase --cov-report=html

# Single file
pytest tests/test_precision.py -v

# By marker
pytest -m constitutional       # F1-F13 floor tests
pytest -m integration          # Integration tests
pytest -m slow                 # Long-running tests

# Quick MCP smoke test
pytest tests/test_mcp_quick.py -v
```

Async mode is `auto` (configured in pyproject.toml) — all `async def test_*` functions are auto-detected without `@pytest.mark.asyncio` decorators. Test paths: `tests/` and `arifos/tests/`. If async tests fail, ensure `pytest-asyncio` is installed.

## Linting & Formatting

```bash
black codebase/ --line-length=100
ruff check codebase/
ruff check codebase/ --fix
mypy codebase/ --ignore-missing-imports
```

**Style:** Black (100 char line length), Ruff (py310 target), MyPy strict on governance modules.
Ruff excludes `archive/**`, `archive_local/**`, `tests/**`.

---

## Architecture: AAA Trinity

The core is three independent engines that process in isolation, then converge:

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

AGI and ASI **cannot see each other's reasoning** until stage 444 (TRINITY_SYNC). This is enforced through bundle isolation:

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

---

## MCP Server Structure

### Entry Points (pyproject.toml scripts)

```
aaa-mcp       -> codebase.mcp.__main__:main        # Auto-detect dispatcher
aaa-mcp-stdio -> codebase.mcp.entrypoints.stdio_entry:main
aaa-mcp-sse   -> codebase.mcp.entrypoints.sse_entry:main
```

### Transports

| Transport | Command | Use Case |
|-----------|---------|----------|
| stdio | `aaa-mcp-stdio` | Claude Desktop, local tools |
| SSE | `aaa-mcp-sse` | HTTP clients, remote |
| Streamable HTTP | `aaa-mcp` (auto) | Production (MCP spec 2025-03-26+) |

### 7 Canonical MCP Tools (`codebase/mcp/tools/canonical_trinity.py`)

| Tool | Stage | Handler | Purpose |
|------|-------|---------|---------|
| `_init_` | 000 | `mcp_init()` | 7-step session ignition |
| `_agi_` | 111-333 | `mcp_agi()` | AGI reasoning engine |
| `_asi_` | 444-666 | `mcp_asi()` | ASI safety engine |
| `_apex_` | 777-888 | `mcp_apex()` | APEX judgment |
| `_vault_` | 999 | `mcp_vault()` | Cryptographic seal |
| `_trinity_` | Full | `mcp_trinity()` | Full 000->999 loop |
| `_reality_` | — | `mcp_reality()` | External fact-checking |

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

### v55 Restructuring (In Progress)

The MCP layer is being refactored from monoliths into modular components:

```
codebase/mcp/
+-- core/           # Protocol layer (bridge.py — 25KB, being split)
|   +-- validators.py   # Input validation (NEW in v55)
+-- transports/     # stdio, sse, base
+-- services/       # rate_limiter, immutable_ledger, metrics
+-- infrastructure/ # redis_client
+-- config/         # modes
+-- entrypoints/    # stdio_entry (sse_entry pending)
+-- tools/          # 7 canonical tools + mcp_tools_v53.py (28KB internal engine)
+-- maintenance.py  # Maintenance utilities (NEW in v55)
+-- archive/        # Legacy code
```

Key monoliths to be aware of: `core/bridge.py` (25KB) and `tools/mcp_tools_v53.py` (28KB).

---

## Constitutional Floors (F1-F13)

13 safety rules enforced at code level. Hard floors block execution; soft floors warn.

| Floor | Name | Type | Key File(s) |
|-------|------|------|-------------|
| F1 | Amanah (Reversibility) | Hard | `codebase/floors/amanah.py` |
| F2 | Truth (tau >= 0.99) | Hard | `codebase/enforcement/floor_validators.py` |
| F4 | Clarity (delta_S <= 0) | Hard | AGI hierarchy check |
| F5 | Peace-squared (>= 1.0) | Soft | ASI engine |
| F6 | Empathy (kappa_r >= 0.95) | Soft | ASI engine |
| F7 | Humility (Omega_0 in [0.03,0.05]) | Hard | AGI precision check |
| F8 | Genius (G >= 0.80) | Derived | `codebase/floors/genius.py` |
| F9 | Anti-Hantu (C_dark < 0.30) | Soft | ASI engine |
| F10 | Ontology | Hard | `codebase/floors/ontology.py`, `codebase/guards/ontology_guard.py` |
| F11 | Command Auth | Hard | `codebase/guards/nonce_manager.py` |
| F12 | Injection | Hard | `codebase/floors/injection.py`, `codebase/guards/injection_guard.py` |
| F13 | Sovereign | Hard | APEX kernel |

**Implementation status:** `codebase/floors/` has F1, F8, F10, F12 as standalone modules. Remaining floors are enforced within engine code and `enforcement/floor_validators.py`.

**Authoritative thresholds:** Always verify against `spec/constitutional_floors_v38Omega.json` (PRIMARY source), not this table.

---

## Guards (`codebase/guards/`)

Hypervisor-level guards for floors F10-F12:
- `ontology_guard.py` — F10: Prevents consciousness claims, reality confusion
- `nonce_manager.py` — F11: Nonce-based identity verification for auth commands
- `injection_guard.py` — F12: Blocks prompt injection patterns
- `session_dependency.py` — Session validation

---

## Stages (`codebase/stages/`)

The 000-999 metabolic loop stages. Early stages (000-333) are handled in `codebase/init/` and engine modules. Later stages have dedicated files:

- `stage_444.py` / `stage_444_trinity_sync.py` — Trinity convergence (DeltaBundle + OmegaBundle -> MergedBundle)
- `stage_555.py` — Empathy (kappa_r calculation)
- `stage_666.py` / `stage_666_bridge.py` — Alignment (Peace-squared)
- `stage_777_forge.py` — Society/Justice
- `stage_888_judge.py` — APEX 9-paradox judgment
- `stage_889_proof.py` — Proof generation
- `stage_999_seal.py` — Vault seal (Merkle tree)

---

## Key Conventions

### 1. Lazy Imports for Optional Dependencies
```python
try:
    import numpy as np
except ImportError:
    np = None
```
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

Floors apply to **generated code**, not just statements. Quick reference from `.github/copilot-instructions.md`:

| Floor | Code Smell | Fix |
|-------|------------|-----|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
| F3 | Contract mismatch, type lies | Use canonical interfaces |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F5 | Destructive defaults, no backup | Safe defaults, preserve state |
| F6 | Only happy path, cryptic errors | Handle edge cases, clear messages |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F8 | Bypasses governance, invents patterns | Use established systems |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

---

## Key Directories

```
codebase/
+-- agi/            # Delta AGI engine (precision.py, hierarchy.py, action.py, atlas.py)
+-- asi/            # Omega ASI engine (asi_components.py)
+-- apex/           # Psi APEX engine (trinity_nine.py, equilibrium_finder.py)
+-- mcp/            # MCP server (v55 restructuring in progress)
+-- floors/         # Standalone floor modules (F1, F8, F10, F12) — NEW in v55
+-- guards/         # F10-F12 hypervisor guards
+-- enforcement/    # Floor validators, governance
+-- stages/         # 444-999 stage handlers
+-- init/           # 000 INIT 7-step ignition
+-- loop/           # Loop manager
+-- vault/          # 999 persistence, ledger, phoenix recovery
+-- federation/     # Federation protocol (physics, math, consensus, proofs)
+-- crypto/         # Cryptographic utilities (rootkey.py)
+-- prompt/         # Prompt registry/templates
+-- system/         # System orchestrator
+-- kernel.py       # KernelManager — singleton Trinity orchestrator
    bundles.py      # DeltaBundle, OmegaBundle, MergedBundle dataclasses
    state.py        # SessionState (immutable copy-on-write)
```

Test structure mirrors source: `tests/constitutional/`, `tests/mcp/`, `tests/core/`, `tests/integration/`, `tests/trinity/`.

---

## Common Tasks

```bash
# Add new MCP tool
# 1. Create handler in codebase/mcp/tools/
# 2. Register in canonical_trinity.py
# 3. Add tests in tests/test_all_mcp_tools.py

# Add new floor validator
# 1. Create module in codebase/floors/fX_name.py
# 2. Export from codebase/floors/__init__.py
# 3. Wire into enforcement/floor_validators.py
# 4. Add tests in tests/constitutional/

# Debug constitutional failure
pytest tests/constitutional/test_01_core_F1_to_F13.py -v -k "f1"
```

---

**Version:** v55.1-TRANSITION
**Live:** https://arif-fazil.com
**Repo:** https://github.com/ariffazil/arifOS
