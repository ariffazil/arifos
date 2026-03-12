# AGENTS.md — arifOS Agent Protocol & Architecture

This guide defines the operational context for AI agents working within the arifOS ecosystem.

**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## Build, Test, and Lint Commands

```bash
# Setup
pip install -e ".[dev]"

# Tests
pytest tests/ -v                           # All tests
pytest tests/test_file.py -v               # Single test file
pytest tests/test_file.py::test_name -v    # Single test
pytest tests/ -v -k "keyword"              # By keyword

# Lint & Format
ruff check . --fix                         # Lint and auto-fix
ruff format .                              # Format
mypy .                                     # Type check

# Server
python -m arifosmcp.runtime                # SSE (HTTP)
python -m arifosmcp.runtime stdio          # stdio (Claude Desktop)

# Docker
make fast-deploy                           # Fast redeploy
make build && make deploy                  # Full deploy
```

---

## Directory Structure

```text
core/                        → KERNEL (decision logic, math)
├── governance_kernel.py    → Runtime state, transitions
├── judgment.py             → Decision interface
└── organs/                 → Trinity engines (AGI/ASI/APEX)

arifosmcp/
├── runtime/                → TRANSPORT HUB (FastMCP, zero logic)
├── intelligence/           → SENSES (Grounding, health)
└── transport/              → External gateways

tests/
├── conftest.py                           → Pytest fixtures
├── core/                                 → Core module tests
│   ├── kernel/                           → Kernel execution tests (NEW)
│   │   ├── test_engine_adapters.py       → InitEngine, AGIEngine, ASIEngine
│   │   └── test_stage_orchestrator.py    → 000-999 metabolic pipeline
│   └── test_sbert_floors.py              → F5/F6/F9 semantic classification
├── adversarial/                          → Judicial order tests
│   └── judicial_orders/
│       └── test_p0_orders.py             → P0 constitutional hardening
└── test_trace_replay.py                  → VAULT999 integrity tests
```

---

## Code Style Guidelines

### Python & Formatting
- Target Python 3.10+ (requires-python = ">=3.12")
- Line length: 100 characters
- Quotes: double, Indent: 4 spaces
- Modern type hints: `list[X]`, `dict[str, Any]`, `X | None`

### Imports
```python
from __future__ import annotations  # Always first

import stdlib
import third_party
from local import Something
```
- Group: stdlib → third-party → local (blank line between)
- Lazy imports for optional deps: try/except ImportError

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Error Handling
```python
@dataclass
class Result:
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
```
- Prefer result dataclass over exceptions
- Use `sys.stderr` for logging (stdout reserved for JSON-RPC)

---

## Architecture Rules

### Separation of Concerns
1. **Logic in `core/`** — Never add decision math to `runtime/`
2. **Transport in `runtime/`** — Hub acts as secure airlock
3. **Grounding in `intelligence/`** — Web search, filesystem, hardware

### The 13 Constitutional Floors (F1–F13)
Every action passes through floors. **HARD** violations trigger `VOID`:
- F1 Amanah: Reversibility & sacred trust
- F2 Truth: No hallucination, verified grounding
- F3 Witness: Quad-witness consensus
- F4 Clarity: Entropy reduction (ΔS ≤ 0)
- F5 Peace²: Lyapunov stability & safety margins
- F6 Empathy: Protect weakest stakeholder
- F7 Humility: Gödel uncertainty band (Ω₀)
- F8 Genius: Governed intelligence (G†)
- F9 Anti-Hantu: No consciousness claims
- F10 Ontology: Category lock (AI = tool)
- F11 Auth: Command authority verification
- F12 Injection: Defense & input validation
- F13 Sovereign: Human final authority / veto

### 888 HOLD Triggers
Human approval required: destructive DB ops, production deploys, mass changes (>10 files), credentials, git history.

### RuntimeEnvelope
Every tool returns: `metrics`, `trace`, `authority`, `payload`, `errors`, `meta`.

---

## Tool Pattern

```python
from fastmcp import FastMCP
mcp = FastMCP("arifOS-APEX-G")

@mcp.tool()
async def my_tool(query: str) -> dict[str, Any]:
    """Tool description."""
    return {"result": "..."}
```

---

## Pre-commit & Security

```bash
pre-commit run --all-files    # Manual run
```

Checks: whitespace, syntax, large files, private keys, format, lint, type check, security.

**Security:** Never commit secrets. Use `.env` files. Injection defense in `core/guards/`.

---

## Test Coverage Guidelines

### Current State (2026.03.12-FORGED)
- **Total Tests:** ~410 passing
- **Coverage:** ~64% (target: 80%)
- **Recent Forge:** +126 tests added (kernel + SBERT validation)

### Test Structure by Module
| Module | Coverage | Status | Test File |
|--------|----------|--------|-----------|
| `core/kernel/engine_adapters.py` | ~85% | ✅ Well-tested | `tests/core/kernel/test_engine_adapters.py` |
| `core/kernel/stage_orchestrator.py` | ~80% | ✅ Well-tested | `tests/core/kernel/test_stage_orchestrator.py` |
| `core/shared/sbert_floors.py` | ~75% | ✅ Well-tested | `tests/core/test_sbert_floors.py` |
| `core/kernel/evaluator.py` | 0% | 🔴 Needs tests | — |
| `core/kernel/heuristics.py` | 0% | 🔴 Needs tests | — |
| `core/kernel/init_000_anchor.py` | 0% | 🔴 Needs tests | — |

### Writing New Tests
```bash
# Run specific test file
pytest tests/core/kernel/test_engine_adapters.py -v

# Run with coverage
pytest tests/core/kernel/test_stage_orchestrator.py --cov=core.kernel.stage_orchestrator

# Run failing tests only
pytest tests/ --lf -v
```

---

**Version:** 2026.03.12-FORGED | **Status:** ACTIVE  
**Coverage:** ~64% (56% → 64%, +8pp) | **Tests:** ~410 passing (+73)
