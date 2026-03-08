# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Project:** arifOS — Constitutional AI Governance System (MCP Server)
**Package:** `arifos` v2026.3.1 | **Python:** >=3.12 | **License:** AGPL-3.0-only
**Full spec:** `docs/00_META/CLAUDE.md`

---

## Version Identity Rule (Persistent)

- arifOS naming in active docs/configs is **date-based**: `YYYY.MM.DD[-SUFFIX]`.
- Do not introduce software-style semantic tags (`vX.Y`, `vX.Y.Z`) in active architecture/seal labels.
- Historical sealed/archive records may retain their original labels.

---

## CRITICAL: No stdout in Tool Code

**NEVER** use `print()` or write to `stdout` in any tool implementation — it corrupts JSON-RPC/MCP streams.
Use `sys.stderr.write()` or `import logging; logger.error()` instead.

---

## Commands

```bash
# Install
pip install -e ".[dev]"

# Run MCP Server
python -m arifosmcp.runtime              # SSE (default, VPS/remote)
python -m arifosmcp.runtime stdio        # stdio (Claude Desktop, local agents)
python -m arifosmcp.runtime http         # Streamable HTTP at /mcp
python -m arifosmcp.transport                     # compat shim (also SSE)

# CLI entry points (from pyproject.toml)
arifos                                # canonical (same as python -m arifosmcp.runtime)
aaa-mcp                               # compat shim
aclip-cai health                      # ACLIP infrastructure CLI

# Tests
pytest tests/ -v                                         # full suite
pytest tests/ -v --cov=core --cov=arifosmcp.transport                # with coverage
pytest tests/test_quick.py -v                            # single file
pytest tests/test_core_foundation.py::test_name -v       # single test
pytest -m constitutional                                 # F1-F13 floor tests
pytest -m integration                                    # integration tests
pytest -m slow                                           # long-running tests
pytest tests/test_e2e_all_tools.py -v                    # E2E all tools
pytest tests/test_e2e_core_to_aaa_mcp.py -v             # E2E core→transport

# Async mode is `auto` — no @pytest.mark.asyncio needed on async test functions

# Format & Lint (100-char limit)
black arifosmcp.transport/ core/ arifosmcp.runtime/ arifosmcp.intelligence/ --line-length=100
ruff check arifosmcp.transport/ core/ arifosmcp.runtime/ arifosmcp.intelligence/ --fix

# Type check (strict on core/)
mypy core/ --ignore-missing-imports

# Docker
docker build -t arifos . && docker run -e PORT=8080 -p 8080:8080 arifos
```

---

## Architecture: Four-Layer Stack

```
core/              → KERNEL: pure decision logic, zero transport deps
arifosmcp.intelligence/         → INTELLIGENCE: triad backends + 9-sense tools
arifosmcp.transport/           → TRANSPORT ADAPTER: FastMCP surface, NO decision logic
arifosmcp.runtime/    → CANONICAL PyPI PACKAGE: external entry point
```

**Critical boundaries:**
- `core/` has **zero** transport dependencies (`fastmcp`, `fastapi`, `starlette` are banned)
- `arifosmcp.transport/` has **zero** decision logic — protocol only
- **Never** name a local module `mcp` — use `arifosmcp.runtime` or `arifosmcp.transport`

**Data flow:** `Client → arifosmcp.runtime → arifosmcp.transport/server.py (@mcp.tool) → arifosmcp.intelligence/triad/* → core/organs/* → core/shared/floors.py`

### Key Modules

| Module | Role |
|--------|------|
| `core/governance_kernel.py` | Unified Ψ state, thermodynamics |
| `core/shared/floors.py` | `THRESHOLDS` dict — **canonical** floor definitions |
| `core/organs/_0_init` → `_4_vault` | 5 enforcement organs (stages 000–999) |
| `arifosmcp.transport/server.py` | 13 MCP tools with `@mcp.tool()` decorators |
| `arifosmcp.intelligence/triad/` | Backend functions: `anchor, reason, integrate, respond, validate, align, forge, audit, seal` |
| `arifosmcp.runtime/governance.py` | 13-LAW catalog, tool-to-dial mappings |
| `core/kernel/constitutional_decorator.py` | Kernel-level floor enforcement |
| `arifosmcp.transport/core/constitutional_decorator.py` | Transport-level floor enforcement |

### Trinity Architecture (ΔΩΨ)

```
000_INIT → AGI(Δ) Mind [111-333] → ASI(Ω) Heart [555-666] → APEX(Ψ) Soul [888] → 999_VAULT
```

AGI and ASI bundles are **isolated** — they cannot see each other's reasoning until stage 444 (TRINITY_SYNC).

### 5-Organ Kernel (`core/organs/`)

| Organ  | Module        | Stages  | Actions                                |
|--------|---------------|---------|----------------------------------------|
| init   | `_0_init.py`  | 000     | `init`, `scan_injection`, `verify_auth` |
| mind   | `_1_agi.py`   | 111-333 | `sense`, `think`, `reason`             |
| heart  | `_2_asi.py`   | 555-666 | `empathize`, `align`                   |
| soul   | `_3_apex.py`  | 444-888 | `sync`, `forge`, `judge`               |
| memory | `_4_vault.py` | 999     | `seal`, `query`, `verify`              |

---

## 13 MCP Tools

Defined in `arifosmcp.transport/server.py`. Backend logic in `arifosmcp.intelligence/triad/`.

**Metabolic chain (000→999):** `anchor_session` → `reason_mind` → `recall_memory` → `simulate_heart` → `critique_thought` → `eureka_forge` → `apex_judge` → `seal_vault`

**Evidence tools (read-only):** `search_reality`, `fetch_content`, `inspect_file`, `audit_rules`, `check_vital`

All tools return: `{verdict, stage, session_id, floors, truth, next_actions}`
Verdicts: `SEAL` | `PARTIAL` | `SABAR` | `VOID` | `888_HOLD`

---

## Constitutional Floors (F1-F13)

Canonical source: `core/shared/floors.py` (`THRESHOLDS` dict). Hard floors → VOID. Soft floors → PARTIAL.

| Floor | Name                | Type   | Threshold  |
|-------|---------------------|--------|------------|
| F1    | Amanah (Reversibility) | Hard | LOCKED   |
| F2    | Truth               | Hard   | τ ≥ 0.99   |
| F3    | Tri-Witness         | Mirror | ≥ 0.95     |
| F4    | Clarity (ΔS)        | Hard   | ΔS ≤ 0     |
| F5    | Peace²              | Soft   | ≥ 1.0      |
| F6    | Empathy (κᵣ)        | Soft   | κᵣ ≥ 0.70  |
| F7    | Humility (Ω₀)       | Hard   | 0.03–0.05  |
| F8    | Genius (G)          | Mirror | G ≥ 0.80   |
| F9    | Anti-Hantu (C_dark) | Soft   | < 0.30     |
| F10   | Ontology            | Wall   | LOCKED     |
| F11   | Command Auth        | Wall   | LOCKED     |
| F12   | Injection Defense   | Hard   | < 0.85     |
| F13   | Sovereign           | Veto   | HUMAN      |

**Execution order:** F12→F11 (Walls) → AGI Floors (F1,F2,F4,F7) → ASI Floors (F5,F6,F9) → Mirrors (F3,F8) → Ledger

---

## Decorator Order (Critical)

```python
@mcp.tool()                    # OUTER — FastMCP registers this
@constitutional_floor("F2")   # INNER — enforcement runs at call time
async def my_tool(...):
```

If reversed, FastMCP registers the unwrapped function and floor enforcement never runs.

---

## Import Namespacing

- `arifosmcp.runtime.*` — canonical external package (PyPI surface)
- `arifosmcp.transport.*` — internal transport adapter
- `arifosmcp.intelligence.*` — intelligence layer (triad, tools, core)
- `core.*` — kernel (`from core.shared.physics import W_3`)
- `mcp.*` / `fastmcp.*` — external SDKs. **Never** shadow with local modules

---

## Key Gotchas

- **Stage 222 THINK is internal-only**: `think()` runs inside `reason_mind` — no external `@mcp.tool()`.
- **`seal_vault` is token-locked**: Pass `governance_token` from `apex_judge`. Missing/tampered token → VOID.
- **F4 (Clarity) is a Hard floor**: `ΔS > 0` → VOID (not PARTIAL). May cause new test failures.
- **`_GOVERNANCE_TOKEN_SECRET`**: Hardcoded in `arifosmcp.transport/server.py` for dev — must be env-var in production.
- **Two floor decorator layers**: `core/kernel/constitutional_decorator.py` (kernel) and `arifosmcp.transport/core/constitutional_decorator.py` (transport). Both exist.
- **`vault999.jsonl` is force-tracked**: Use `git add -f VAULT999/vault999.jsonl` for new entries.
- **`.mcp.json` at root is deprecated**: Active config is `.claude/mcp.json`.
- **`codebase/` is removed**: Deleted in v2026.2.15. All code is in `core/`, `arifosmcp.intelligence/`, `arifosmcp.transport/`.
- **`tests/archive/`**: ~100 legacy files with broken imports. Reference only.
- **`remote_inspection/`**: Cloned external repos (gitignored). Never commit.
- **APEX Solver**: Uses geometric mean (not arithmetic) for 9-paradox synthesis. Target: GM ≥ 0.85, std dev ≤ 0.10.
- **Source verification**: PRIMARY = `spec/*.json` canon docs → SECONDARY = `core/*.py`, `arifosmcp.transport/*.py` → TERTIARY = `docs/*.md` (may lag).

---

## Adding a New MCP Tool

1. Add `@mcp.tool()` in `arifosmcp.transport/server.py`
2. Create backend in `arifosmcp.intelligence/triad/`
3. Wire kernel logic via `core/` imports
4. Register floor mapping in `core/kernel/constitutional_decorator.py` `FLOOR_ENFORCEMENT` dict
5. Mirror in `arifosmcp.runtime/server.py` and add to `AAA_TOOLS`
6. Add tests in `tests/`

---

## Deployment

| Target | Command | Notes |
|--------|---------|-------|
| Local (stdio) | `python -m arifosmcp.runtime stdio` | Claude Desktop, Cursor IDE |
| VPS/Coolify (SSE) | `python -m arifosmcp.runtime` | Default transport, port 8080 |
| Docker | `docker build -t arifos . && docker run -p 8080:8080 arifos` | |

**Environment variables:** `HOST` (default `0.0.0.0`), `PORT` (default `8080`), `AAA_MCP_TRANSPORT` (default `sse`), `AAA_MCP_OUTPUT_MODE` (`user`/`debug`), `ARIFOS_PHYSICS_DISABLED` (`0`/`1`), `PPLX_API_KEY`, `BRAVE_API_KEY`

**MCP config files:** `.claude/mcp.json` (active), `.agents/mcp.json` (agent mode)

---

## 888_HOLD Triggers (Require Human Confirmation)

Database migrations, production deployments, credential handling, mass file ops (>10 files), git history modification, conflicting evidence across source tiers.

**Protocol:** List consequences → state irreversibles → ask "yes, proceed" → wait → execute with logging.
