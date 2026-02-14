# arifOS Agent Guide

**DITEMPA BUKAN DIBERI** — Forged, Not Given

This guide is for AI coding agents working on arifOS: Claude, Gemini, Codex, Kimi, OpenCode.

## Quick Reference

| Item | Value |
|------|-------|
| Language | Python 3.10+ (async-first) |
| Formatter | Black (100 char lines) |
| Linter | Ruff |
| Type Checker | MyPy |
| Test Runner | pytest (asyncio_mode = auto) |
| Framework | FastMCP 2.14+, FastAPI, Pydantic v2 |

## Build & Test Commands

```bash
# Install (with dev dependencies)
pip install -e ".[dev]"

# Run MCP Server
python -m aaa_mcp              # stdio mode (default)
python -m aaa_mcp sse          # SSE mode
python -m aaa_mcp http         # HTTP mode

# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_quick.py -v

# Run a single test function
pytest tests/test_e2e_core_to_aaa_mcp.py::test_function_name -v

# Run tests with coverage
pytest --cov=aaa_mcp --cov=core tests/ -v

# Quick smoke test
pytest tests/test_quick.py -v
```

## Code Quality Commands

```bash
# Format code
black --line-length 100 aaa_mcp/ core/

# Lint
ruff check aaa_mcp/ core/
ruff check --fix aaa_mcp/ core/  # auto-fix

# Type check
mypy aaa_mcp/ core/ --ignore-missing-imports

# Pre-commit (runs all checks)
pre-commit run --all-files
```

## Code Style Guidelines

### Imports

```python
# Standard library first, then third-party, then local
from __future__ import annotations

import os
import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from fastmcp import FastMCP

# Local imports: use explicit paths
from core.shared.types import AgiOutput, FloorScores, Verdict
from aaa_mcp.core.heuristics import compute_system_state
```

- Prefer `aaa_mcp` imports for MCP server code
- Prefer `core` imports for kernel/engine code
- External MCP SDK is `mcp` (do not shadow with local modules)
- Use lazy imports for optional dependencies: `try/except ImportError`

### Types & Models

```python
# Use Pydantic v2 models for data contracts
class FloorScores(BaseModel):
    f2_truth: float = Field(default=0.0, ge=0.0, le=1.0)
    f4_clarity: float = Field(default=0.0)
    model_config = ConfigDict(frozen=True)

# Use dataclasses for internal state
@dataclass
class SystemState:
    uncertainty: float
    risk: float
    profile: Profile

# Type hints are required for public functions
async def sense(query: str, session_id: str) -> Dict[str, Any]:
    ...
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `compute_floor_scores` |
| Classes | PascalCase | `GovernanceKernel` |
| Constants | UPPER_SNAKE | `TOOL_ANNOTATIONS` |
| Private | _prefix | `_extract_intent` |
| Modules | lowercase | `governance_kernel.py` |
| Organs | `_N_name.py` | `_1_agi.py`, `_2_asi.py` |

### Async Patterns

```python
# All I/O operations must be async
async def tool_function(query: str) -> Dict[str, Any]:
    result = await some_async_operation()
    return result

# Tests don't need @pytest.mark.asyncio (asyncio_mode = auto)
async def test_something():
    result = await my_async_function()
    assert result is not None
```

### Error Handling

```python
# Use explicit error types, not bare except
try:
    result = await risky_operation()
except FileNotFoundError:
    return {"error": "File not found", "verdict": "VOID"}
except ValueError as e:
    return {"error": str(e), "verdict": "PARTIAL"}

# For floor violations, return structured verdicts
if truth_score < 0.99:
    return {"verdict": "VOID", "failed_floor": "F2", "reason": "Truth below threshold"}
```

### Docstrings

```python
async def sense(query: str, session_id: str) -> Dict[str, Any]:
    """
    Stage 111: SENSE — The first touch of the Mind

    Parse raw query into structured intent using ATLAS routing.

    Args:
        query: Raw user query
        session_id: Constitutional session token

    Returns:
        Dict with lane, gpv, intent, floor_scores
    """
```

## Project Structure

```
arifOS/
├── aaa_mcp/           # MCP Server (wrapper layer)
│   ├── server.py      # 5 canonical tools
│   ├── core/          # Wrapper-specific code
│   └── capabilities/  # T6-T21 modules
├── core/              # Kernel (decision logic)
│   ├── organs/        # 5-organ implementations
│   │   ├── _0_init.py
│   │   ├── _1_agi.py  # Mind (111-333)
│   │   ├── _2_asi.py  # Heart (555-666)
│   │   ├── _3_apex.py # Soul (888)
│   │   └── _4_vault.py
│   ├── shared/        # Types, physics, floors
│   └── pipeline.py
├── tests/             # Test suite
└── VAULT999/          # Immutable ledger
```

## Tool Decorator Pattern

```python
@mcp.tool(name="init_session", description="000_INIT - Session ignition")
@constitutional_floor("F11", "F12")
async def init_session(query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    ...
```

Order: `@mcp.tool()` outer, `@constitutional_floor()` inner.

## Constitutional Verdicts

| Verdict | Meaning |
|---------|---------|
| `SEAL` | All floors pass — execute |
| `PARTIAL` | Soft floor warning — proceed with caution |
| `888_HOLD` | High-stakes — await human confirmation |
| `VOID` | Hard floor fail — blocked |
| `SABAR` | Stop, Acknowledge, Breathe, Adjust, Resume |

## 888_HOLD Triggers (Require Human Confirmation)

- Database migrations, DROP/TRUNCATE/DELETE
- Production deployments
- Mass file operations (>10 files)
- Credential/secret handling
- Git history modification (rebase, force push)

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection |
| `REDIS_URL` | Redis connection |
| `AAA_MCP_TRANSPORT` | stdio, sse, or http |
| `ARIFOS_PHYSICS_DISABLED` | Disable physics (tests) |
| `AAA_MCP_OUTPUT_MODE` | debug or production |

## Testing Notes

- Tests use `asyncio_mode = "auto"` — no need for `@pytest.mark.asyncio`
- Physics is disabled by default in tests (`ARIFOS_PHYSICS_DISABLED=1`)
- Legacy tests in `tests/archive/` and `tests/legacy/` are auto-skipped
- Use `conftest.py` fixtures for common setup

---

**Version:** v60.0-FORGE | **License:** AGPL-3.0-only
