# AGENTS.md - arifOS Development Guide
Project: arifOS constitutional MCP server
Python: >=3.12 (runtime), tooling config targets py310+
Release baseline: 2026.2.23

This file guides agentic coding tools in this repository.
Primary goal: safe, reversible, test-backed changes that respect architecture boundaries.

## Source Of Truth
- PRIMARY: `AGENTS.md`, `pyproject.toml`, and repository code.
- SECONDARY: `.github/copilot-instructions.md` (integrated below).
- Cursor rules status: no `.cursorrules` and no `.cursor/rules/` found.

## Repository Layout
- `core/`: pure governance/kernel logic.
- `aaa_mcp/`: transport and MCP adapter layer.
- `aclip_cai/`: console/federation support.
- `tests/`: unit, integration, and constitutional tests.
- `spec/`: canonical governance specs, including v46 floors/stages.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install -e ".[dev]"
```
Fallback:
```bash
pip install -e ".[dev]"
```

## Build, Lint, and Typecheck
```bash
black . --line-length 100
ruff check . --line-length 100
ruff check . --line-length 100 --fix
mypy .
```
Notes:
- Black/Ruff line length is 100.
- Ruff excludes `tests/**` in current config.
- MyPy has stricter overrides for core governance modules.

## Test Commands (Single Test Emphasis)
Use these exact patterns:
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
Async policy:
- `asyncio_mode = "auto"`.
- Do not add `@pytest.mark.asyncio` unless explicitly required.

## Run Commands
```bash
python -m aaa_mcp
python -m aaa_mcp sse
python -m aaa_mcp http
python -m aaa_mcp stdio
python -m aaa_mcp.selftest
arifos serve --profile strict --metrics
```

## Code Style Guidelines

### Imports
- Order: standard library -> third-party -> local modules.
- Local module groups: `core.*`, `aaa_mcp.*`, `aclip_cai.*`.
- Do not shadow external SDK name `mcp`.
- Use lazy imports (`try/except ImportError`) for optional dependencies.

### Formatting and Types
- Keep lines <= 100 chars.
- Add type hints on function signatures in production code.
- Use Pydantic v2 `BaseModel` for external tool/API I/O contracts.
- Use `str`-backed enums for verdict-like state (`class Verdict(str, Enum)`).
- Prefer `async def` for I/O-bound operations.

### Naming
- Modules/functions/variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Private helpers: `_leading_underscore`.
- Organ files follow `_N_name.py` style (for example `_0_init.py`).

### Error Handling
- MCP-facing tools catch exceptions and return structured dict errors.
- Core functions may raise internal exceptions when appropriate.
- Never swallow errors silently.
Canonical MCP tool failure pattern:
```python
except Exception as e:
    return {"verdict": "VOID", "error": str(e), "stage": "222_REASON"}
```

### Decorator Order
- `@mcp.tool(...)` must be outermost.
- `@constitutional_floor(...)` must be inner.

### Module Hygiene
- Include module docstrings for non-trivial modules.
- Keep exports explicit with `__all__` where practical.
- Avoid hidden side effects, especially session state mutation.

## Architecture Constraints
1. `core/` must stay transport-agnostic (no FastAPI/Starlette/Uvicorn/FastMCP imports).
2. `aaa_mcp/` should remain transport glue, not governance decision logic.
3. SessionState is copy-on-write; do not mutate shared state in place.
4. In STDIO mode, never write logs/protocol data to stdout (`print()` is unsafe).

## Testing Requirements For Changes
- Every behavior change should add or update tests.
- Place tests in the appropriate `tests/` subtree.
- Run focused single tests first, then broader suites.

## OpenCode Session Lifecycle (Mandatory)
Session order for this repository:
1. Restore continuity from VAULT999.
2. Run `000 INIT` before planning or implementation.
3. Execute governed work with honest receipts/evidence.
4. Run `999 SEAL` before handoff, including continuity notes.
Hard rule: do not start directly at implementation stages without restore + init.

## 888 HOLD - Mandatory Human Confirmation
Trigger HOLD before:
- database-destructive operations
- production deployments
- mass file changes (>10 files)
- credential or secret handling
- git history modifications (rebase, force-push, destructive reset)
When triggered:
1. Declare: `888 HOLD - [trigger] detected`
2. List conflicts: PRIMARY vs SECONDARY vs TERTIARY
3. Re-check PRIMARY source(s)
4. Wait for explicit human approval

## Copilot and Cursor Rules
From `.github/copilot-instructions.md`:
- Canonical stage spine: `000 -> 444 -> 666 -> 888 -> 999`.
- Run 000 before actions and 999 before handoff.
- Cite PRIMARY canonical sources for constitutional claims (`AGENTS.md`, `spec/v46/*`).
- Preserve role separation (Architect != Engineer != Auditor != KIMI).
- Keep session data honest; never fabricate executed steps.
Cursor status:
- No `.cursorrules` or `.cursor/rules/` files are present.

## Practical Agent Workflow
1. Read target files and nearby tests first.
2. Implement the smallest safe change that solves the request.
3. Run a focused single test, then broader checks.
4. Report what changed and what was actually verified.
