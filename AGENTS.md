# arifOS Agent Guide

## Project Overview

arifOS is a Constitutional AI Governance System built on the Model Context Protocol (MCP).
Python 3.10+ (async-first). Key architectural boundary: `core/` contains pure decision
logic with ZERO transport dependencies; `aaa_mcp/` is the MCP transport adapter with ZERO
decision logic. Never mix these layers.

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `core/` | Kernel — pure decision logic, stateless functions, no MCP/HTTP imports |
| `core/organs/` | 5-core organs: `_0_init.py`, `_1_agi.py`, `_2_asi.py`, `_3_apex.py`, `_4_vault.py` |
| `core/shared/` | Shared types (`types.py`), guards, floors |
| `aaa_mcp/` | MCP server adapter — transport only, calls into `core/` |
| `aclip_cai/` | Sensory/observability layer (C0-C9 tools) |
| `333_APPS/` | Application layers L1 (Prompts) through L7 (AGI) |
| `tests/` | Test suite; `tests/archive/` and `tests/legacy/` are auto-ignored |

## Setup

```bash
# Create venv and install (uv recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install uv
uv pip install -e ".[dev]"
# Or: pip install -e ".[dev]"
```

## Build, Lint, and Test Commands

### Formatting and Linting

```bash
black . --line-length 100               # Format
ruff check . --line-length 100          # Lint
ruff check . --line-length 100 --fix    # Lint with auto-fix
mypy .                                  # Type check
```

All config is in `pyproject.toml`. Line length is 100 everywhere. Ruff excludes `tests/`
from linting. MyPy enforces strict typing on core governance modules but is relaxed for tests.

### Running Tests

```bash
# Run all tests (physics auto-disabled via conftest.py)
pytest tests/ -v

# Single test file
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Single test class
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName -v

# Single test function
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName::test_method -v

# Single standalone test function (no class)
pytest tests/test_quick.py::test_function_name -v

# By marker
pytest -m constitutional      # Constitutional floor tests only
pytest -m "not slow"          # Skip slow tests
pytest -m integration         # Integration tests only
```

**Async tests:** `asyncio_mode = "auto"` in pyproject.toml — do NOT add `@pytest.mark.asyncio`
decorators; async test functions are detected automatically.

**Automatic fixtures** (session-scoped, from `tests/conftest.py`):
- `ARIFOS_PHYSICS_DISABLED=1` — always set, disables expensive physics computation
- `ARIFOS_ALLOW_LEGACY_SPEC=1` — always set, bypasses cryptographic manifest
- `AAA_MCP_OUTPUT_MODE=debug` — always set

**Infrastructure markers:** Tests tagged `postgres_required` or `redis_required` auto-skip
when those services are unavailable.

### Running the Server

```bash
python -m aaa_mcp              # stdio (default, for local MCP clients)
python -m aaa_mcp sse          # SSE (for cloud/remote)
python -m aaa_mcp http         # Streamable HTTP
python -m aaa_mcp.selftest     # Self-test
```

## Code Style

### Import Order

1. `from __future__ import annotations` (if used)
2. Standard library (`os`, `hashlib`, `typing`, etc.)
3. Third-party (`pydantic`, `fastmcp`, `numpy`, etc.)
4. Local packages (`core.*`, `aaa_mcp.*`, `aclip_cai.*`)

### Formatting and Types

- **Line length:** 100 characters (Black + Ruff)
- **Type hints:** Required on all function signatures (parameters and return)
- **Data models:** Pydantic v2 `BaseModel` for all I/O contracts; `@dataclass` for internal types
- **Enums:** Use `class Verdict(str, Enum)` pattern for string enums
- **Async:** All I/O-bound functions and MCP tool handlers MUST be `async def`
- **Lazy imports:** Use `try/except ImportError` for optional dependencies

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Modules | `snake_case` | `governance_kernel.py` |
| Classes | `PascalCase` | `GovernanceKernel` |
| Functions/Variables | `snake_case` | `compute_uncertainty` |
| Constants | `UPPER_SNAKE_CASE` | `UNCERTAINTY_THRESHOLD` |
| Private helpers | `_prefix` | `_generate_session_id` |
| Organ modules | `_N_name.py` | `_0_init.py`, `_1_agi.py` |

### Error Handling

- **MCP tools:** Never raise exceptions to the caller. Catch all exceptions and return a dict:
  ```python
  except Exception as e:
      return {"verdict": "VOID", "error": str(e), "stage": "222_REASON"}
  ```
- **Kernel functions** (`core/`): May raise exceptions for internal logic errors
- Never swallow errors silently

### Decorator Order (Critical)

`@mcp.tool()` must be the OUTER decorator, `@constitutional_floor()` must be INNER:

```python
@mcp.tool(name="reason", description="...")
@constitutional_floor("F2", "F4", "F7")
async def reason(query: str) -> dict:
    ...
```

### Module Documentation

- Every module should have a docstring explaining its purpose
- Use section delimiters for logical groupings:
  ```python
  # ═══════════════════════════════════════════════════════
  # SECTION NAME
  # ═══════════════════════════════════════════════════════
  ```
- Define `__all__` exports explicitly in all modules

## Architectural Rules

1. **`core/` is pure:** No imports from `fastmcp`, `starlette`, `fastapi`, `uvicorn`, or any
   transport/HTTP library. It must remain a stateless decision kernel.
2. **`aaa_mcp/` is transport only:** No decision logic. It calls `core/` functions and wraps
   results for MCP transport.
3. **Do NOT shadow `mcp`:** The external SDK is `mcp`. Local modules must not use that name.
4. **SessionState is copy-on-write:** Never mutate session state in place.

## Testing Requirements

- All new functionality MUST have tests
- Place tests in the appropriate subdirectory (`tests/core/`, `tests/constitutional/`,
  `tests/integration/`, etc.)
- Use plain `def test_*()` functions (or `async def test_*()` — auto-detected)
- No `@pytest.mark.asyncio` needed

## Pre-commit Hooks

The repo has `.pre-commit-config.yaml` with: trailing-whitespace fix, Black, Ruff (with
`--fix`), MyPy, Bandit (security), detect-secrets, plus custom hooks for constitutional
floor checks and F9 Anti-Hantu (blocks deceptive naming patterns like "I feel", "I am
conscious") and F1 Amanah (blocks `shutil.rmtree`, `DROP TABLE`, `DELETE FROM` without
safeguards).

## 888_HOLD — Mandatory Human Confirmation

Stop and request explicit human approval before:
- Database operations (DROP, TRUNCATE, DELETE without WHERE)
- Production deployments
- Mass file changes (>10 files)
- Credential/secret handling
- Git history modification (rebase, force push)

## Copilot / GitHub Instructions

See `.github/copilot-instructions.md` for GitHub Copilot-specific rules (v46 alignment,
stage gating, session data contracts, output format). That file is derivative guidance;
this file (`AGENTS.md`) and `pyproject.toml` are the canonical sources for build and style.
