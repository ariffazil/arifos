# AGENTS.md - arifOS Development Guide

Project: arifOS constitutional MCP server
Python: >=3.12 (runtime), tooling currently targets py310+ for lint/type configs
Release baseline: 2026.2.23

This file is for agentic coding tools working in this repository.
Primary goal: make safe, style-consistent changes that respect architecture boundaries.

## Source Of Truth

- Primary: this `AGENTS.md`, `pyproject.toml`, and in-repo code.
- Additional policy: `.github/copilot-instructions.md` (included below as actionable rules).
- Cursor rules check: no `.cursorrules` and no `.cursor/rules/` files were found.

## Repository Layout

- `core/`: pure governance/kernel logic.
- `aaa_mcp/`: MCP and HTTP/SSE transport adapter layer.
- `aclip_cai/`: 9-sense console/federation support.
- `tests/`: unit, integration, and constitutional tests.

## Project Overview

- arifOS is a constitutional AI governance system delivered as a Python MCP server.
- Runtime posture is SSE-primary with MCP/HTTP fallback and optional stdio for local tooling.
- Engineering priority is truthful, reversible, test-backed changes with explicit governance receipts.

## Current Runtime Surface (Truth)

- Unified MCP server currently registers 20 tools.
- MCP resources: `arifos://templates/full-context`, `arifos://schemas/tooling`.
- MCP prompts: `arifos.prompt.trinity_forge`, `arifos.prompt.anchor_reason`, `arifos.prompt.audit_then_seal`.
- Runtime default transport is SSE; HTTP `/mcp` is fallback; stdio is optional local mode.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install -e ".[dev]"
```

If `uv` is unavailable, use:

```bash
pip install -e ".[dev]"
```

## Build / Lint / Typecheck

```bash
black . --line-length 100
ruff check . --line-length 100
ruff check . --line-length 100 --fix
mypy .
```

Notes:
- Line length is 100.
- Ruff excludes `tests/**` via config.

## Test Commands

Use these exact patterns (especially for single-test execution):

```bash
pytest tests/ -v
pytest tests/test_file.py -v
pytest tests/test_file.py::TestClassName -v
pytest tests/test_file.py::TestClassName::test_method -v
pytest tests/test_file.py::test_function_name -v
pytest -m constitutional -v
pytest -m integration -v
pytest -m "not slow" -v
```

Async test policy: `asyncio_mode = "auto"`; avoid `@pytest.mark.asyncio` by default.

## Run Server / Health Checks

```bash
python3 -m aaa_mcp
python3 -m aaa_mcp sse
python3 -m aaa_mcp http
python3 -m aaa_mcp stdio
python3 -m aaa_mcp.selftest
```

Deployment health endpoint used by the project:

```bash
curl -sS https://arifosmcp.arif-fazil.com/health
```

## Code Style And Conventions

### Imports

1. `from __future__ import annotations` (if used)
2. Standard library
3. Third-party packages
4. Local modules (`core.*`, `aaa_mcp.*`, `aclip_cai.*`)

### Formatting And Types

- Use Black/Ruff defaults with 100-char lines.
- Add type hints on public and internal function signatures.
- Use Pydantic v2 `BaseModel` for API or I/O contracts.
- Use `str`-backed enums for verdict-like enums.
- Prefer `async def` for I/O-bound functions and tool handlers.

### Naming

- Modules/functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private helpers: `_leading_underscore`
- Organ module pattern: `_0_init.py`, `_1_agi.py`, etc.

### Error Handling

- MCP-facing tools should catch exceptions and return structured error dicts.
- Core kernel code may raise exceptions internally when appropriate.
- Never silently swallow errors.

MCP tool failure return pattern:

```python
except Exception as e:
    return {"verdict": "VOID", "error": str(e), "stage": "222_REASON"}
```

### Decorator Order

`@mcp.tool(...)` must be outermost and `@constitutional_floor(...)` must be inner.

## Hard Architectural Boundaries

1. `core/` must remain transport-agnostic (no FastAPI/Starlette/Uvicorn/FastMCP imports).
2. `aaa_mcp/` is transport glue and orchestration, not decision-theory logic.
3. Do not shadow external SDK name `mcp` with local modules/variables.
4. Session state must follow copy-on-write patterns (no hidden in-place mutation).
5. For STDIO mode, never write protocol logs to stdout (`print(...)` is unsafe there).

## Active Constraints And Guardrails

- Prefer minimal, reversible edits first; escalate only when necessary.
- Treat unknowns as unknowns (no fabricated status, metrics, or outputs).
- Trigger `888 HOLD` before irreversible or high-risk operations.
- Preserve lifecycle continuity notes so the next session can restart deterministically.

## OpenCode Lifecycle Contract (arifOS Overlay)

Required order for every OpenCode session in this repository:

1. `VAULT999 RESTORE` (load latest sealed continuity record)
2. `000 INIT` (repo analysis and deterministic initialization)
3. `WORK` (governed implementation and verification)
4. `999 SEAL` (close session with canonical continuity receipt)

Hard rule: do not begin directly at implementation stages without restore + init.

## Thermodynamic Governance Framing (Operational)

- `000 INIT` is the constitutional anchor: restore continuity, then constrain the session with `AGENTS.md` before implementation.
- During `WORK`, entropy can increase from code generation, but governance boundaries remain active.
- `999 SEAL` compresses the work window into a canonical continuity receipt stored in VAULT999.
- If a step is risky or hard to reverse, trigger `888 HOLD` and require explicit human approval.

Operational interpretation:

- `000 INIT`: reduce uncertainty early (`delta S << 0`) by loading prior continuity and active constraints.
- `WORK`: bounded change window (`delta S > 0`) with reversible-first edits and explicit receipts.
- `999 SEAL`: collapse session output into low-entropy handoff (`delta S < 0`) with path/time/session tag/files touched.

Principle: `Akal Memerintah, Amanah Mengunci`.

## Testing Requirements For New Work

- Every behavior change should include or update tests.
- Place tests in relevant folders under `tests/`.
- Prefer focused single-test runs during development, then run a wider suite.

## Pre-Commit And Security Hooks

This repository uses pre-commit checks (formatting, linting, typing, security, secrets).
Expect hooks such as Black, Ruff, MyPy, Bandit, and detect-secrets.
Do not bypass hooks unless explicitly instructed by a human maintainer.

## Governance Safety (888 HOLD)

Pause and require explicit human confirmation before:

- database-destructive operations
- production deployment actions
- mass edits affecting more than 10 files
- credential/secret handling
- git history rewrites (rebase, force-push, destructive reset)

When hold is triggered, explicitly state:
1) trigger,
2) conflicting sources (if any),
3) what was re-verified,
4) that human approval is required before continuing.

## Copilot/Cursor Rule Integration

From `.github/copilot-instructions.md`, agents should also enforce:

- Canonical stage spine: `000 -> 444 -> 666 -> 888 -> 999`.
- Run stage `000` before major action planning and `999` before handoff.
- Cite primary sources for constitutional claims (`AGENTS.md`, `spec/v46/*`).
- Maintain separation of powers (Architect vs Engineer vs Auditor vs KIMI roles).
- Keep session data honest; do not fabricate executed steps.

No Cursor-specific rules are currently present in this repo.

## Practical Agent Workflow

1. Read target files and neighboring tests first.
2. Make the smallest change that satisfies the request.
3. Run focused tests, then broader checks.
4. Report exactly what changed and what was verified.
