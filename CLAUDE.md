# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Project:** arifOS — Constitutional AI Governance System
**Package:** `arifos` v2026.2.22 (PyPI)
**Python:** >=3.12 | **License:** AGPL-3.0-only
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## ⚠️ Critical: Logging in MCP
For STDIO transport, writing to `stdout` will break the server.
- Use `sys.stderr` or a logging library configured for `stderr`.
- Never use naked `print()` calls in tool implementations.

---

## Build & Dev Commands

```bash
# Install (editable with dev dependencies)
pip install -e ".[dev]"

# Run MCP Server (3 transports)
python -m aaa_mcp              # stdio (default — Claude Desktop, local agents)
python -m aaa_mcp sse          # SSE (Railway, remote HTTP clients)
python -m aaa_mcp http         # Streamable HTTP at /mcp

# Alternative CLI entry points (from pyproject.toml [project.scripts])
aaa-mcp                        # same as python -m aaa_mcp
aclip-cai health               # ACLIP infrastructure CLI
aclip-server                   # ACLIP MCP server mode

# Docker
docker build -t arifos .
docker run -e PORT=8080 -p 8080:8080 arifos
```

## Testing

```bash
# Full suite
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=codebase --cov-report=html

# Single file / single test
pytest tests/test_quick.py -v
pytest tests/test_core_foundation.py::test_function_name -v

# By marker
pytest -m constitutional       # F1-F13 floor tests
pytest -m integration          # Integration tests
pytest -m slow                 # Long-running tests

# Quick MCP smoke test
pytest tests/test_quick.py -v

# E2E pipeline
pytest tests/test_e2e_all_tools.py -v
pytest tests/test_e2e_core_to_aaa_mcp.py -v
```

Async mode is `auto` in pyproject.toml — async test functions are auto-detected without `@pytest.mark.asyncio` decorators. Test paths: `tests/` and `arifos/tests/`.

## Linting & Formatting

```bash
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
├── governance_kernel.py → GovernanceKernel (unified Ψ state)
├── judgment.py          → judge_cognition, judge_empathy, judge_apex
├── pipeline.py          → Constitutional pipeline orchestrator (forge)
├── telemetry.py         → 30-day locked adaptation with drift tracking
├── shared/              → Foundation modules: physics, atlas, types, crypto,
│                          floors (ALL_FLOORS), routing, formatter, mottos, nudge
├── organs/              → 5 enforcement organs (_0_init → _4_vault)
└── asi/sbert_floors.py  → SBERT-based ASI floor scoring (F5, F6, F9)

aaa_mcp/                 → ADAPTER (transport only, NO decision logic)
├── server.py            → FastMCP server with 10 tools (@mcp.tool decorators)
├── __main__.py          → CLI entry: stdio/sse/http dispatcher
├── rest.py              → REST API bridge
├── core/                → constitutional_decorator, heuristics, engine_adapters, state
├── capabilities/        → t6_web_search (Brave Search)
├── integrations/        → Container tools (VPS only)
├── services/            → constitutional_metrics, redis_client
├── external_gateways/   → brave_client.py
└── vault/               → Audit logging adapter

codebase/                → LEGACY engine layer (still used by adapter)
├── agi/                 → AGI engine (engine.py contains AGIEngineHardened)
├── asi/                 → ASI engine (engine.py contains ASIEngineHardened)
├── apex/                → APEX kernel (APEXJudicialCore, 9-paradox solver)
├── init/                → mcp_000_init (canonical 7-step session init)
├── shared/
│   ├── floors/          → F1, F8, F10, F12 standalone floor modules
│   ├── guards/          → F10 ontology, F11 nonce, F12 injection guards
│   └── stages/          → 444-999 metabolic loop stages
└── vault/               → Merkle-tree immutable ledger

aclip_cai/               → 9-Sense Infrastructure Console & MCP Federation Hub
├── core/                → Lifecycle, Floor Audit, Vault Logger, Thermo-Budgeting
├── dashboard/           → React dashboard for 9 senses (Sight, Hearing, Touch, etc.)
├── config/              → Floor thresholds and tool specifications
└── scripts/             → Deployment and evaluation runners
333_APPS/                → 8-Layer Application Stack (L0 Kernel → L7 AGI)
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

**Bundle isolation**: AGI and ASI cannot see each other's reasoning until stage 444 (TRINITY_SYNC). DeltaBundle and OmegaBundle are immutable after creation.

### 5-Organ Kernel (`core/organs/`)

The kernel exposes actions through 5 organs, importable via `from core.organs import ...`:

| Organ | Module | Actions | Stages |
|-------|--------|---------|--------|
| init | `_0_init.py` | `init`, `scan_injection`, `verify_auth` | 000 |
| mind | `_1_agi.py` | `sense`, `think`, `reason` | 111-333 |
| heart | `_2_asi.py` | `empathize`, `align` | 555-666 |
| soul | `_3_apex.py` | `sync`, `forge`, `judge` | 444-888 |
| memory | `_4_vault.py` | `seal`, `query`, `verify` | 999 |

---

## 10 MCP Tools (v64.2 — "Hardened Skills")

All defined in `aaa_mcp/server.py` and federated via `aclip_cai/core/mcp_server.py` as canonical system calls:

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
| `trinity_forge` | 000-999 | F1-F13 (all) | Unified constitutional pipeline shortcut |

---

## Constitutional Floors (F1-F13)

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

**Floor enforcement code:** `aaa_mcp/core/constitutional_decorator.py` — wraps all MCP tools. F12 runs MANDATORY on all tools before anything else. Hard floor fail → VOID. Soft floor fail → PARTIAL. All pass → SEAL.

**Floor definitions:** `core/shared/floors.py` (ALL_FLOORS dict) is the canonical source. Standalone modules in `codebase/shared/floors/` (F1, F8, F10, F12).

---

## Key Conventions

### Import Namespacing
- `aaa_mcp.*` — local constitutional MCP code
- `mcp.*` — external MCP SDK (v1.26.0). **Never** shadow with local modules
- `core.*` — canonical kernel imports (`from core.shared.physics import W_3`)
- `core.organs` — organ actions (`from core.organs import sense, think, reason`)
- `codebase.*` — legacy engine layer (still functional)

### Decorator Order (Critical)
```python
@mcp.tool()                    # OUTER — FastMCP registers this
@constitutional_floor("F2")   # INNER — enforcement runs at call time
async def my_tool(...):
```
If reversed, FastMCP registers the unwrapped function and enforcement never runs.

### Lazy Imports for Optional Dependencies
```python
try:
    import numpy as np
except ImportError:
    np = None
```
Never crash on import for optional deps.

### Code-Level Floor Enforcement

| Floor | Code Smell | Fix |
|-------|------------|-----|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

### APEX Solver
Uses geometric mean (not arithmetic) for 9-paradox synthesis. GM punishes imbalance more harshly. Target: GM ≥ 0.85, std dev ≤ 0.10.

### Source Verification for Constitutional Claims
Before making constitutional claims, verify against PRIMARY sources:
1. **PRIMARY (Required):** `spec/*.json`, canon documents (SEALED status)
2. **SECONDARY:** `codebase/*.py` (implementation reference)
3. **TERTIARY:** `docs/*.md`, `README.md` (informational, may lag behind PRIMARY)

---

## Adding New Components

### New MCP Tool
1. Add `@mcp.tool()` definition in `aaa_mcp/server.py`
2. Wire kernel logic via `core/` imports (not inline decision logic)
3. Add floor mapping with `@constitutional_floor()` decorator
4. Add tests in `tests/`

### New Constitutional Floor
1. Create module in `codebase/shared/floors/fX_name.py`
2. Export from `codebase/shared/floors/__init__.py`
3. Register in `core/shared/floors.py` (ALL_FLOORS dict)
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
- **Engine consolidation**: `codebase/agi/engine.py` contains `AGIEngineHardened` (formerly separate `engine_hardened.py`, merged at v55.5). Same class, single file now.
- **F4/F6 numbering**: Differs between some docs and `constitutional_floors.py` (swapped in some places). Verify against `aaa_mcp/server.py` floor mappings as source of truth.
- **Windows environment**: Use PowerShell. `$env:` syntax breaks in nested `-Command` strings.
- **pyproject.toml packages**: Must NOT include `mcp*` (would re-shadow the SDK).
- **vault_seal**: `result["seal"]` KeyError is pre-existing in some code paths.
- **`.mcp.json` (root)**: Deprecated since v65.0 (empty `mcpServers`). Active config is `.claude/mcp.json`.
- **mcp_bridge.py**: Has `_measure_entropy()` Shannon function that is NOT wired to Step 4.

---

## 888_HOLD Triggers (High-Stakes Operations)

Require explicit user confirmation:

- **Database migrations** — Irreversible system changes
- **Production deployments** — Safety-critical operations
- **Credential/secret handling** — Identity verification required
- **Mass file operations (>10 files)** — Entropy management
- **Git history modification** — Remote authority required
- **User correction of constitutional claim** — Re-verify against PRIMARY sources
- **Conflicting evidence across source tiers** — Pause for consensus

**Protocol**: List consequences → State irreversibles → Ask "yes, proceed" → Wait for confirmation → Execute with logging.

---

## Deployment

| Target | Command | Notes |
|--------|---------|-------|
| Local (stdio) | `python -m aaa_mcp` | Claude Desktop, Cursor IDE |
| Railway (SSE) | Auto-deploys from GitHub | `railway.toml`, port 8080 |
| Docker | `docker build -t arifos . && docker run -p 8080:8080 arifos` | |

**Live endpoints:**
- Health: `https://arifosmcp.arif-fazil.com/health`
- MCP: `https://arifosmcp.arif-fazil.com/mcp`

**MCP config files:** `.claude/mcp.json` (active), `.agents/mcp.json` (agent mode)

---

## 📚 MCP Resources

- **Official Site:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Documentation:** [modelcontextprotocol.info/docs/](https://modelcontextprotocol.info/docs/)
- **Mirror (CN):** [mcpcn.com/en/docs/](https://mcpcn.com/en/docs/)
- **Anthropic Intro:** [anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
- **GitHub:** [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- **OpenAI/Codex:** [developers.openai.com/codex/mcp/](https://developers.openai.com/codex/mcp/)
- **LangChain Adapter:** [docs.langchain.com/oss/python/langchain/mcp](https://docs.langchain.com/oss/python/langchain/mcp)

---

**Version:** v64.2.0-GAGI | **Repo:** https://github.com/ariffazil/arifOS
