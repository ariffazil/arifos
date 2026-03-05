# AGENTS.md - arifOS Agent Playbook
Project: `arifOS` | Package: `arifos` | Python: `>=3.12`

This file guides agentic coding tools working in this repository.
Instruction precedence when sources conflict:
1) `AGENTS.md` (this file)
2) `CLAUDE.md` (repo root)
3) `.github/copilot-instructions.md` (derivative guidance)

## Repository Map
- Active implementation paths: `core/`, `aaa_mcp/`, `arifos_aaa_mcp/`, `aclip_cai/`.
- `core/` is governance/kernel logic and should stay transport-agnostic.
- `aaa_mcp/` is MCP transport/tool wiring, not core constitutional logic.
- `arifos_aaa_mcp/` is canonical package entry surface.
- Older references to `codebase/*` are legacy; prefer current paths above.

## Setup
```bash
# Recommended (uv)
uv venv
source .venv/Scripts/activate
uv pip install -e ".[dev]"

# Alternative
python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"
```

## Build / Run / Lint / Type Check
```bash
# Run server entry points
python -m arifos_aaa_mcp
python -m arifos_aaa_mcp stdio
python -m arifos_aaa_mcp http
python -m aaa_mcp

# Format and lint
black aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/ --line-length=100
ruff check aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/
ruff check aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/ --fix

# Type check
mypy core/ --ignore-missing-imports
mypy .
```

Lint/type notes:
- Black and Ruff use 100-char lines.
- Ruff rules include `E,F,I,UP,N,B` and excludes `tests/**`, `archive/**`.
- MyPy is stricter in `core.*` than in test modules.

## Test Commands (single test emphasized)
```bash
# Full suite
pytest tests/ -v

# Coverage run
pytest tests/ -v --cov=core --cov=aaa_mcp

# Single file
pytest tests/test_quick.py -v

# Single function (primary pattern)
pytest tests/test_core_foundation.py::test_name -v

# Single class and method
pytest tests/test_file.py::TestClassName -v
pytest tests/test_file.py::TestClassName::test_method -v

# Marker subsets
pytest -m constitutional -v
pytest -m integration -v
pytest -m "not slow" -v

# Quick smoke
pytest tests/test_mcp_quick.py -v
```

Pytest conventions:
- `asyncio_mode = auto` in config.
- Avoid adding `@pytest.mark.asyncio` unless a specific test requires it.
- Run narrow tests first, then broaden scope.

## Code Style

### Imports
- Order imports: standard library -> third-party -> local modules.
- Keep grouped import blocks clean (Ruff/isort-compatible).
- Never shadow external SDK namespaces, especially `mcp`.
- Use lazy optional imports for non-required dependencies.

### Formatting
- Line length: 100.
- Quote style: double quotes.
- Prefer focused, composable functions over large handlers.
- Add comments only when code intent is not obvious.
- In MCP tool code, never use `print()`/stdout output; use logging or stderr.

### Types
- Add type hints for new or changed public signatures.
- Prefer explicit return types on non-trivial functions.
- Use `pydantic.BaseModel` v2 for structured payloads where models are used.
- Minimize `Any`; do not loosen typing in `core/*` for convenience.

### Naming
- Modules/functions/variables: `snake_case`.
- Classes/exceptions: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Internal helpers: leading underscore.
- Use honest names; do not hide side effects with euphemistic names.

### Error Handling
- Do not swallow exceptions silently.
- Preserve exception context when re-raising (`raise ... from exc`).
- Core/kernel code may raise; transport layer maps errors for tool responses.
- Tool-level failures should return structured error payloads with verdict/stage context.

## MCP-Specific Conventions
- Decorator order is mandatory:
  1) `@mcp.tool(...)` outer
  2) constitutional decorator inner
- Reversing order can bypass enforcement at registration/runtime.
- Keep response contracts stable with existing tool schema expectations.

## Architecture Guardrails
- Keep layer boundaries intact:
  - `core/`: constitutional logic, no transport framework dependencies
  - `aaa_mcp/`: protocol adapters and MCP wiring
  - `aclip_cai/`: triad intelligence functions
  - `arifos_aaa_mcp/`: packaging and external entry points
- Prefer minimal, localized edits over broad refactors unless explicitly requested.
- Do not add new subsystem trees when current architecture already provides a place.

## Cursor and Copilot Rules
- Cursor rules check performed: no `.cursor/rules/` and no `.cursorrules` found at repo root.
- Copilot rules file exists: `.github/copilot-instructions.md`.
- Included Copilot requirements here:
  - 100-column Black/Ruff formatting
  - `mcp` namespace must remain unshadowed
  - `@mcp.tool()` outer + constitutional decorator inner
  - lazy imports for optional dependencies
  - high-risk actions require hold/confirmation behavior
- If Copilot guidance conflicts with current code layout (for example `codebase/*` paths), follow this file and `CLAUDE.md`.

## High-Risk Holds
Require explicit human confirmation before:
- credential/secret access or mutation
- destructive database or filesystem operations
- git history rewrites / force pushes
- production deployment actions
- mass edits across many files

## Agent Workflow
1) Read target files, related tests, and local config first.
2) Implement the smallest safe change matching the request.
3) Run a focused single test node first.
4) Run broader tests/lint/type checks as needed by scope.
5) Report exactly what changed and what was verified.

Last updated: 2026-03-05
