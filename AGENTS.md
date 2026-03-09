# AGENTS.md

Operational guide for coding agents operating in this repository.

## Source Priority

1. This file.
2. `pyproject.toml` configs.
3. `.github/copilot-instructions.md`.

*Note: Cursor rules (`.cursorrules`, `.cursor/rules/`) are absent. Fallback to Copilot guidance.*

## Setup & Environment

- **Python**: `>=3.12` (formatting targets `py310`).
- **Dependencies**: `pip install -e ".[dev]"`
- **Hooks**: `pre-commit install`

## Build & Run

Canonical runtime entrypoints:
```bash
python -m arifosmcp.runtime stdio
python -m arifosmcp.runtime sse
python -m arifosmcp.runtime http
```
Legacy transport (for specific docs/tests): `python -m arifosmcp.transport`

## Lint, Format & Type Checks

```bash
ruff check . --fix
black .
mypy core arifosmcp
bandit -c pyproject.toml -r .
pre-commit run --all-files
```

## Test Commands

**Crucial:** Agent handoffs must include targeted testing. Defaults: `pytest` async mode is `auto`.

- **All tests**: `pytest tests -v`
- **Single file**: `pytest tests/canonical/test_runtime_server.py -v`
- **Exact test (Node ID)**: `pytest tests/canonical/test_runtime_server.py::test_server_starts -v`
- **Keyword**: `pytest -k "anchor_session" -v`
- **Full physics**: `ARIFOS_PHYSICS_DISABLED=0 pytest tests/core -v`
- **Coverage**: `pytest --cov=arifosmcp --cov=core --cov-report=term-missing`

## Code Style & Conventions

- **Formatting**: Line length 100 (Black + Ruff). Use double quotes. File names `snake_case.py`.
- **Imports**: Group std lib, third-party, local (`core`, `arifosmcp`). Lazy import optional dependencies. Avoid shadowing the external `mcp` SDK with local files.
- **Types**: Explicit optionals (`X | None`). Stricter typing in `core.governance_kernel`, `core.organs.*`. Never invent values to satisfy types.
- **Naming**: `PascalCase` classes, `snake_case` functions/vars, `UPPER_SNAKE_CASE` constants. Use honest names; deceptive naming violates F9.
- **Error Handling**: Do not swallow exceptions. Catch only when adding context/recovering safely. Preserve causality (`raise NewError(...) from e`).
- **Architecture**: Transport/Runtime API surface lives in `arifosmcp/`. Governance/kernel logic belongs in `core/`. (Legacy `codebase/` and `arifos/` dirs have been removed).
- **Tooling**: Tool decorators require outer `@mcp.tool()` and inner `@constitutional_floor()`.

## 888 HOLD Discipline

**Mandatory HOLD** for high-stakes operations or evidence failures:
- DB drops, mass file changes (>10), credential handling, git history mods.
- User correction to constitutional claims, conflicting evidence (PRIMARY vs SECONDARY), or contradicting `grep` results.

**Action Sequence**:
1. Declare: "888 HOLD — [trigger type] detected"
2. List conflicts (PRIMARY vs SECONDARY).
3. Re-read PRIMARY sources (`spec JSON` or SEALED canon).
4. Await explicit human approval before proceeding.

## AClip Stage & Session Protocol (v46)

Canonical Stages: `000 → 444 → 666 → 888 → 999`
- Run `000` (ARCHITECT) before planning/action.
- Run `999` (SEAL/VOID) before handoff.

**Output Format** (Always display progress):
```text
[STAGE NNN] Stage Name
Status: [IN_PROGRESS | COMPLETE]
Floor Scores: F1=X F2=X ... F12=X
Verdict: [SEAL | PARTIAL | SABAR | VOID | 888_HOLD]
```

**Session Data Contract**:
Only include steps that *actually executed*. No fabricated steps.
```python
# CORRECT: Honest session structure
session_data = {"id": "uuid", "task": "...", "status": "mcp_direct", "steps": []}
```

## Floor Violations (Quick Fixes)

- **F1 Truth**: Mutates input, hidden side effects → Pure functions, explicit returns.
- **F2 Clarity**: Fabricated data, fake metrics → Empty/null when unknown.
- **F3 Stability**: Contract mismatch, type lies → Use canonical interfaces.
- **F5 Quality**: Destructive defaults, no backup → Safe defaults, preserve state.
- **F6 Empathy**: Only happy path, cryptic errors → Handle edge cases, clear messages.
- **F8 Tri-Witness**: Bypasses governance, invents patterns → Use established systems.
- **F9 Anti-Hantu**: Deceptive naming, hidden behavior → Honest names, transparent logic.

## Pre-Handoff Checklist

1. Run targeted exact node-id test commands.
2. Run `ruff` + `black`.
3. Run `mypy` for type-sensitive files.
4. Summarize changed files, rationale, and justify stage verdict.
