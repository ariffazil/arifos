# arifOS Agent Guide

## Project Overview

arifOS is a Constitutional AI Governance System built on the Model Context Protocol (MCP).
Python 3.12+ (Strictly required for MCP typing). Key architectural boundary: `core/` contains pure decision
logic with ZERO transport dependencies; `aaa_mcp/` is the MCP transport adapter with ZERO
decision logic. Never mix these layers.

### ⚠️ Critical Rule: Logging
**For STDIO-based servers:** NEVER use `print()` or write to `stdout`. Doing so will corrupt the JSON-RPC stream and break the MCP connection.
- ❌ **Bad:** `print("Starting server")`
- ✅ **Good:** `print("Starting server", file=sys.stderr)`
- ✅ **Good:** `logging.info("Starting server")` (ensure logger is configured for stderr)

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `core/` | Kernel — pure decision logic, stateless functions, no MCP/HTTP imports |
| `core/organs/` | 5-core organs: `_0_init.py`, `_1_agi.py`, `_2_asi.py`, `_3_apex.py`, `_4_vault.py` |
| `core/shared/` | Shared types (`types.py`), guards, floors |
| `aaa_mcp/` | MCP server adapter — transport only, calls into `core/` |
| `aclip_cai/` | 9-Sense Infrastructure Console & MCP Federation Hub |
| `aclip_cai/core/` | Sensory kernel: lifecycle, floor audits, vault logging, thermo-budgeting |
| `aclip_cai/dashboard/` | 9-Sense React dashboard (Sight, Hearing, Touch, etc.) |
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

1. **`core/` is pure:** No imports from `fastmcp`, `starlette`, `fastapi`, `uvicorn`, or any transport/HTTP library. It must remain a stateless decision kernel.
2. **`aaa_mcp/` is the brain adapter:** Transport only. No decision logic. Calls `core/` functions.
3. **`aclip_cai/` is the sensory adapter:** Transport + Observability. No core decision logic. Calls into `aclip_cai/core/` for infrastructure-specific audits.
4. **Do NOT shadow `mcp`:** The external SDK is `mcp`. Local modules must not use that name.
5. **SessionState is copy-on-write:** Never mutate session state in place.
6. **5-Organ Trinity (Public Contract):** `aaa_mcp` exposes 5 core organs (`init_session`, `agi_cognition`, `asi_empathy`, `apex_verdict`, `vault_seal`) + 4 utilities (`search`, `fetch`, `analyze`, `system_audit`). `aclip_cai` exposes 9 governed sensory tools. Both layers must maintain constitutional alignment (F1-F13) without leaking decision logic across boundaries.

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

## GOVERNANCE_MODES

- **STRICT (Default):** Complete floor enforcement. Hard floor violations return VOID.
- **BALANCED:** Complete enforcement, but soft floor thresholds are moderated.
- **PERMISSIVE:** Minimal enforcement (F9, F12 only). Primarily for development.
- **AUDIT:** Evaluation and logging only. No blocking.

## 888_HOLD & SABAR_72 — High-Stakes Governance

Constitutional governance requires mandatory pauses for high-risk and irreversible actions:

- **SABAR_72:** 72-hour cooling period for high-risk actions (F11 Authority). Stop and await human review.
- **888_HOLD:** Quarantine for irreversible operations pending explicit human ratification.

Stop and request explicit human approval before:
- Database operations (DROP, TRUNCATE, DELETE without WHERE)
- Production deployments
- Mass file changes (>10 files)
- Credential/secret handling
- Git history modification (rebase, force push)
- Bypassing constitutional floor failures (F1-F13)

## 📚 MCP Resources

- **Official Site:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Documentation:** [modelcontextprotocol.info/docs/](https://modelcontextprotocol.info/docs/)
- **Mirror (CN):** [mcpcn.com/en/docs/](https://mcpcn.com/en/docs/)
- **Anthropic Intro:** [anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
- **GitHub:** [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- **OpenAI/Codex:** [developers.openai.com/codex/mcp/](https://developers.openai.com/codex/mcp/)
- **LangChain Adapter:** [docs.langchain.com/oss/python/langchain/mcp](https://docs.langchain.com/oss/python/langchain/mcp)

Protocol: List consequences → State irreversibles → Ask "yes, proceed" → Wait for confirmation → Execute with logging.

See `.github/copilot-instructions.md` for GitHub Copilot-specific rules (v46 alignment,
stage gating, session data contracts, output format). That file is derivative guidance;
this file (`AGENTS.md`) and `pyproject.toml` are the canonical sources for build and style.

## MCP Protocol References

Canonical bookmarks for the Model Context Protocol — the wire standard this system is built on:

| Resource | URL |
|:---------|:----|
| **Main site & spec overview** | https://modelcontextprotocol.io |
| **Full documentation (EN)** | https://modelcontextprotocol.info/docs/ |
| **Full documentation (CN mirror)** | https://mcpcn.com/en/docs/ |
| **Anthropic intro & architecture** | https://www.anthropic.com/news/model-context-protocol |
| **GitHub org (spec, SDKs, servers)** | https://github.com/modelcontextprotocol |
| **OpenAI/Codex integration guide** | https://developers.openai.com/codex/mcp/ |
| **LangChain MCP adapter docs** | https://docs.langchain.com/oss/python/langchain/mcp |

> **F2 Truth note:** URLs may drift over time. Always verify against the GitHub org
> (`github.com/modelcontextprotocol`) as the ground-truth source for spec versions.
