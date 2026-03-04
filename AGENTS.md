# AGENTS.md — arifOS Development Guide

**Project:** arifOS — Constitutional AI Governance System (Python MCP Server)  
**Python:** >=3.12 | **Version:** 2026.3.1  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given  

Guidance for agentic coding tools. Goal: safe, reversible, test-backed changes respecting architecture boundaries.

---

## Quick Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install uv && uv pip install -e ".[dev]"
```

---

## Build, Lint, and Format

```bash
black . --line-length 100               # Format
ruff check . --line-length 100          # Lint
ruff check . --line-length 100 --fix    # Auto-fix lint issues
mypy .                                  # Type check
```

- Ruff excludes `tests/**` and `archive/**` (see `pyproject.toml`).
- MyPy strict mode on: `core.governance_kernel`, `core.judgment`, `core.pipeline`, `core.organs.*`.

---

## Test Commands

```bash
pytest tests/ -v                                              # All tests
pytest tests/test_file.py -v                                  # Single file
pytest tests/test_file.py::TestClassName -v                   # Single class
pytest tests/test_file.py::TestClassName::test_method -v      # Single method
pytest tests/test_file.py::test_function_name -v              # Single function
pytest -m constitutional -v                                   # Constitutional tests
pytest -m integration -v                                      # Integration tests
pytest -m "not slow" -v                                       # Skip slow tests
pytest tests/test_mcp_quick.py -v                             # Quick smoke test
```

**Note:** `asyncio_mode = "auto"` — do NOT add `@pytest.mark.asyncio` decorators.

---

## Run the Server

```bash
python -m aaa_mcp              # stdio (default)
python -m aaa_mcp sse          # SSE transport
python -m aaa_mcp http         # Streamable HTTP
python -m aaa_mcp.selftest     # Self-test
arifos serve --profile strict  # Production mode
```

---

## Code Style Guidelines

### Import Order
1. Standard library (`os`, `typing`, etc.)
2. Third-party (`pydantic`, `fastmcp`, etc.)
3. Local packages (`core.*`, `aaa_mcp.*`)

**Do not shadow** the external SDK name `mcp`. Use lazy imports for optional deps.

### Formatting
- **Line length:** 100 characters (Black + Ruff)
- **Type hints:** Required on all function signatures
- **Data models:** Pydantic v2 `BaseModel`
- **Async:** All I/O-bound functions MUST be `async def`

### Naming Conventions
| Type | Convention | Example |
|------|-----------|---------|
| Modules | `snake_case` | `governance_kernel.py` |
| Classes | `PascalCase` | `GovernanceKernel` |
| Functions | `snake_case` | `compute_uncertainty` |
| Constants | `UPPER_SNAKE` | `UNCERTAINTY_THRESHOLD` |
| Private | `_prefix` | `_generate_session_id` |

### Error Handling
MCP tools catch exceptions and return structured dicts:
```python
except Exception as e:
    return {"verdict": "VOID", "error": str(e), "stage": "222_REASON"}
```

Core kernel functions may raise; never swallow errors silently.

### Decorator Order
```python
@mcp.tool(name="reason", description="...")      # OUTER
@constitutional_floor("F2", "F4", "F7")           # INNER
async def reason(query: str) -> dict: ...
```

---

## Architecture Constraints

1. **`core/` is pure:** No imports from `fastmcp`, `starlette`, `fastapi`, etc.
2. **`aaa_mcp/` is transport only:** No governance logic. Calls `core/` functions.
3. **SessionState is copy-on-write:** Never mutate in place.
4. **Do NOT shadow `mcp`:** External SDK is `mcp`. No local module uses that name.

---

## ACLIP/AAA Layer Map (Canonical)

Use this exact mental model when operating arifOS:

| Layer | Role | Interface |
|------|------|-----------|
| `aclip_cai` | ACLIP Console (ops layer) | 9 triad tools |
| `aaa_mcp` | Constitution engine | 13 canonical tools |
| `arifos_aaa_mcp` | Public external surface | same 13 tools (wrapped) |

Triad mapping for `aclip_cai`:

- `Delta` (Mind): `anchor`, `reason`, `integrate`
- `Omega` (Heart): `respond`, `validate`, `align`
- `Psi` (Soul): `forge`, `audit`, `seal`

Runtime expectation:

- ACLIP can run over stdio or network transport for agent ops.
- Constitutional checks still apply via kernel floors before high-risk actions.

---

## 🛑 888_HOLD — Mandatory Human Confirmation

Stop and await explicit approval for:

- **Destructive:** DB migrations, mass deletes (>10 files), state changes
- **Secrets:** API keys, JWTs, credential handling
- **Conflict:** τ < 0.99 or spec vs code mismatch
- **User Correction:** User disputes constitutional claim

**Action:** Declare trigger, list conflicts, re-read PRIMARY sources, await `"yes, proceed"`.

---

## Floor Violations Quick Reference

| Floor | Code Smell | Fix |
|-------|------------|-----|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F5 | Destructive defaults | Safe defaults, preserve state |
| F6 | Only happy path | Handle edge cases, clear messages |
| F7 | False confidence | Admit uncertainty, cap confidence |
| F9 | Deceptive naming | Honest names, transparent logic |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ARIF_SECRET` / `ARIF_JWT_SECRET` | Auth for SSE/HTTP |
| `BRAVE_API_KEY` / `OPENAI_API_KEY` | External tools |
| `DATABASE_URL` / `REDIS_URL` | Persistence |
| `AAA_MCP_OUTPUT_MODE` | `user` or `debug` |
| `ARIFOS_PHYSICS_DISABLED` | Skip thermo calc (testing) |
| `ARIFOS_ALLOW_LEGACY_SPEC` | Bypass spec gating (testing) |

---

## Workflow for Agents

1. Read target files and nearby tests first
2. Implement smallest safe change
3. Run focused single test, then broader suite
4. Report what changed and what was verified

**DITEMPA BUKAN DIBERI.**

---

## SEAL Progress Protocol (Required)

All agents operating in this repo (local or VPS) must track progress with a SEAL percentage.

- Start each task with `SEAL: 0%` and a clear target outcome.
- Update percent after each completed step (`10%`, `35%`, `70%`, etc.).
- End each response with `SEAL: <percent>% -> <next action>`.
- If blocked, do not loop; report blocker + default decision + one unblocking command.
- If scope changes, state `SEAL RESET: <old>% -> <new plan>`.

### Standard SEAL Gates

- `0-20%` Discovery: inspect state, constraints, risks
- `21-50%` Foundation: folders/config/env + path validation
- `51-75%` Build: implementation
- `76-90%` Verify: tests, health checks, permissions, logs
- `91-100%` Seal: final state + next single command

### Hard Stop Rules (No Chaos)

- Single source of truth for app code on VPS: `/srv/arifOS`
- No new symlinks unless user explicitly asks
- Master secrets file on VPS: `/home/ariffazil/xxx/.env`
- If duplicate app path appears, stop and consolidate before any new deploy

---

## Runtime Reality Notes (vps + local)

- Do not assume a fixed MCP tool count from theory docs; inspect runtime tools first.
- `stdio` transport is default stable for local clients.
- `sse` and `http` are allowed for VPS/public routing, but validate health before production traffic.
- Canonical hold verdict spelling is `888_HOLD`.
- Injection defense includes prompt override patterns, system-tag smuggling, and destructive command patterns.

### Required First-Step Check

Before any major task, report:

1. active repo path
2. active transport mode
3. runtime MCP server status
4. source-of-truth code path (`/srv/arifOS` on VPS)

*Last Updated: 2026-03-04*
