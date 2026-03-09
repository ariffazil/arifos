# AGENTS.md

Operational guide for coding agents in this repository.

## Source Priority

1. This file.
2. `pyproject.toml` tool configs.
3. `.github/copilot-instructions.md` (included below).

Rule discovery:
- Cursor rules not found (`.cursor/rules/` and `.cursorrules` are absent).
- Copilot rules found at `.github/copilot-instructions.md`.

## Setup

```bash
pip install -e ".[dev]"
pre-commit install
```

Environment notes:
- Runtime Python: `>=3.12`.
- Black/Ruff/Mypy configs target py310 compatibility syntax.

## Build and Run

Use canonical runtime entrypoints first:

```bash
python -m arifosmcp.runtime stdio
python -m arifosmcp.runtime sse
python -m arifosmcp.runtime http
```

Legacy/compat transport entrypoint (still valid in some docs/tests):

```bash
python -m arifosmcp.transport
python -m arifosmcp.transport sse
```

## Lint/Format/Type/Security

```bash
ruff check .
ruff check . --fix
black .
mypy core arifosmcp
bandit -c pyproject.toml -r .
pre-commit run --all-files
```

## Test Commands

Defaults from `tests/conftest.py`:
- `ARIFOS_PHYSICS_DISABLED=1`
- `ARIFOS_ALLOW_LEGACY_SPEC=1`
- `pytest` async mode is `auto`

Run all tests:

```bash
pytest
pytest tests -v
```

Run a single file:

```bash
pytest tests/canonical/test_runtime_server.py -v
```

Run one exact test (node id):

```bash
pytest tests/canonical/test_runtime_server.py::test_server_starts -v
```

Run by keyword or marker:

```bash
pytest -k "anchor_session and not slow" -v
pytest -m "constitutional" -v
```

Coverage:

```bash
pytest --cov=arifosmcp --cov=core --cov-report=term-missing
```

Enable full physics when needed:

```bash
# PowerShell
$env:ARIFOS_PHYSICS_DISABLED="0"; pytest tests/core -v

# bash/zsh
ARIFOS_PHYSICS_DISABLED=0 pytest tests/core -v
```

## Code Style Rules

Formatting/imports:
- Line length `100` (Black + Ruff).
- Ruff lint set: `E,F,I,UP,N,B`.
- Import order: standard lib, third-party, local (`core`, `arifosmcp`).
- Use double quotes.
- File/module names use `snake_case.py`.

Types:
- Add type hints in new/edited production code.
- Stricter typing applies in `core.governance_kernel`, `core.organs.*`, `core.shared.*`.
- Use explicit optionals (`X | None`), avoid implicit optional patterns.
- Never invent values to satisfy type checks.

Naming:
- Classes: `PascalCase`.
- Functions/variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Internal helpers: `_leading_underscore`.
- Use honest names; avoid deceptive/euphemistic naming.

Error handling:
- Do not swallow exceptions.
- Catch only when adding context or recovering safely.
- Preserve causality (`raise NewError(...) from e`).
- Prefer safe defaults and guard checks for risky paths.

Architecture:
- Runtime API surface: `arifosmcp/runtime/server.py`.
- Bridge/routing: `arifosmcp/bridge.py`.
- Governance/kernel logic belongs in `core/`, not thin transport wrappers.
- Keep state transitions explicit and immutable-friendly.

Testing:
- Place tests under `tests/` and name files `test_*.py`.
- Add focused unit tests plus integration coverage for behavior changes.
- Use `require_postgres`/`require_redis` fixtures for service-dependent tests.
- Do not re-enable `tests/archive` or `tests/legacy` unless explicitly asked.

## Copilot Guidance Included

From `.github/copilot-instructions.md`:
- Prefer local `arifosmcp.transport` imports when editing transport subsystem code.
- External SDK import is `mcp`; do not shadow it with local modules.
- Transport tool decorators: outer `@mcp.tool()`, inner governance decorator.
- Verify active tool definitions before edits:
  - `arifosmcp.transport.server`
  - `codebase/mcp/core/tool_registry.py` (if present in current branch)
- Use lazy imports for optional dependencies.
- Human authority is final for high-stakes operations.

If guidance conflicts, trust actual code + `pyproject.toml` + this file.

## Pre-Handoff Checklist

1. Run targeted tests (include at least one exact node-id test command).
2. Run lint + format checks.
3. Run mypy when type-sensitive files changed.
4. Summarize changed files and rationale.
5. Call out any checks you could not run and how to run them.

Last updated: 2026-03-08
