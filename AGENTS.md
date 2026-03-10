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
├── conftest.py             → Pytest fixtures
└── core/                   → Core module tests
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
- F1 Truth: No hallucination, cite sources
- F2 Clarity: Transparent reasoning, state assumptions  
- F3 Peace: Reversible changes, audit trail
- F4 Entropy: Named constants, clear parameters
- F5 Witness: Safe defaults, preserve state
- F6 Empathy: Handle edge cases, clear errors
- F7 Humility: Admit uncertainty, cap confidence
- F8 Tri-Witness: Consensus verification
- F9 Anti-Hantu: Honest naming, no deception
- F10 Coherence: System-wide consistency
- F11 Auth: Session anchoring
- F12 Injection: Input validation
- F13 Seal: Cryptographic verification

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

**Version:** 2026.03.10-SEAL | **Status:** ACTIVE
