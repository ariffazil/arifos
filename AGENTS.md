# arifOS AGENTS.md — Agent Coding Guide

**Project:** arifOS — Constitutional AI Governance System  
**Version:** v62.3.0 | **Python:** >=3.10 | **License:** AGPL-3.0-only  
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## 1. Commands Cheat Sheet

```bash
# === INSTALLATION ===
pip install -e ".[dev]"           # Full dev dependencies
pip install -e ".[all]"            # All optional deps
pip install -r requirements.txt     # Core deps only

# === MCP SERVER ===
python -m aaa_mcp                  # stdio (Claude Desktop, Cursor)
python -m aaa_mcp sse              # SSE transport (HTTP)
python -m aaa_mcp http             # HTTP transport

# === ALTERNATIVE SERVER (root) ===
python server.py                    # Dev server (stdio)
python server.py --sse              # SSE mode

# === TESTING ===
pytest tests/ -v                   # Full suite
pytest tests/test_file.py -v       # Single file
pytest tests/test_file.py::test_func -v  # Single test
pytest -m constitutional           # Floor tests only
pytest -m integration             # Integration tests
pytest --cov=aaa_mcp --cov=core tests/ -v  # With coverage

# === CODE QUALITY ===
black --line-length 100 aaa_mcp/ core/
ruff check aaa_mcp/ core/
ruff check aaa_mcp/ core/ --fix    # Auto-fix
mypy aaa_mcp/ core/ --ignore-missing-imports

# === DOCKER ===
docker build -t arifos .
docker run -p 8080:8080 arifos
docker compose up -d

# === PRE-COMMIT ===
pre-commit install
pre-commit run --all-files
```

---

## 2. Code Style Guidelines

### Formatting
- **Line length:** 100 characters (Black)
- **Target Python:** 3.10+
- **Quote style:** Double quotes
- **Indent:** 4 spaces (no tabs)

### Imports
```python
# Standard library first, then third-party, then local
import asyncio
import hashlib
from typing import Any, Optional

import pydantic
from fastapi import FastAPI

from aaa_mcp.core import ConstitutionalDecorator
from core.organs import AGI, ASI, APEX
```

### Types
- Use Pydantic v2 for all data models
- Explicit return types required for governance modules
- Optional: `Optional[X]` preferred over `X | None`
- Use `Any` sparingly (governance modules: strict typing)

### Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `floor_validators.py` |
| Classes | PascalCase | `class SessionState` |
| Functions | snake_case | `def compute_truth()` |
| Constants | UPPER_SNAKE | `MAX_TOKEN_LIMIT = 10000` |
| Private | _prefix | `_internal_helper()` |

### Error Handling
```python
# DO: Explicit errors with context
raise ValueError(f"Invalid floor score {score}: must be >= 0.0")

# DON'T: Bare exceptions
try:
    result = compute()
except Exception:  # BAD
    pass

# DO: Specific exceptions with logging
from aaa_mcp.core.logging import get_logger
logger = get_logger(__name__)

try:
    result = compute()
except ValueError as e:
    logger.warning(f"Floor validation failed: {e}")
    raise
```

---

## 3. Constitutional Floors (F1-F13)

| Floor | Name | Threshold | Enforcement |
|-------|------|-----------|-------------|
| F1 | Amanah | Reversibility | No mutations, pure functions |
| F2 | Truth | τ ≥ 0.99 | Empty/null when unknown |
| F3 | Tri-Witness | W₃ ≥ 0.95 | Consensus verification |
| F4 | Clarity | ΔS ≤ 0 | Named constants, clear logic |
| F5 | Peace² | P² ≥ 1.0 | Non-destructive defaults |
| F6 | Empathy | κᵣ ≥ 0.95 | Edge case handling |
| F7 | Humility | Ω₀ ∈ [0.03,0.05] | Cap confidence at 0.95 |
| F8 | Genius | G ≥ 0.80 | Use established systems |
| F9 | Anti-Hantu | C_dark < 0.30 | No dark patterns |
| F10 | Ontology | LOCK | No consciousness claims |
| F11 | Authority | LOCK | Identity verification |
| F12 | Injection | Score < 0.85 | Prompt injection guard |
| F13 | Sovereign | HUMAN | Human final authority |

### Verdict Hierarchy
```
SEAL > PARTIAL > 888_HOLD > SABAR > VOID
```

---

## 4. Architecture Patterns

### Trinity Pipeline
```
000_INIT → 111_SENSE → 222_THINK → 333_REASON
                     ↓
         444_SYNC → 555_EMPATHY → 666_ALIGN
                     ↓
         777_FORGE → 888_JUDGE → 999_SEAL
```

### Session State (Immutable)
```python
from core.state import SessionState

state = SessionState.from_context(ctx)
new_state = state.to_stage("333")    # Returns new instance
new_state = state.set_floor_score()   # Returns new instance
# NEVER: state.field = value (mutation forbidden)
```

### Bundle Isolation
- **DeltaBundle**: AGI reasoning output (precision, hypotheses)
- **OmegaBundle**: ASI empathy output (stakeholders, impact)
- **MergedBundle**: Created at stage 444 via `compute_consensus()`

---

## 5. Key Files & Patterns

| Pattern | Location |
|---------|----------|
| MCP Tools | `aaa_mcp/tools/*.py` |
| Floor Validators | `core/floors/fX_*.py` |
| Constitutional Decorator | `aaa_mcp/core/constitutional.py` |
| Session State | `core/state.py` |
| Trinity Engines | `core/organs/_1_agi.py`, `_2_asi.py`, `_3_apex.py` |
| Agent Config (Claude) | `.claude.md` |
| Agent Config (Gemini) | `.gemini.md` |

### Adding a New MCP Tool
1. Define in `aaa_mcp/core/tool_registry.py`
2. Implement handler in `aaa_mcp/tools/`
3. Add tests in `tests/`
4. Update this AGENTS.md

---

## 6. Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ARIFOS_PHYSICS_DISABLED` | Skip thermodynamics (tests) | `0` |
| `GOVERNANCE_MODE` | HARD or SOFT | `SOFT` |
| `AAA_MCP_TRANSPORT` | stdio, sse, or http | `stdio` |
| `DATABASE_URL` | PostgreSQL for VAULT999 | — |

---

## 7. Thermodynamic Primitives

### Entropy (S, ΔS)
- **Definition:** Measure of confusion or disorder in a problem state.
- **AI Meaning:** "Don't just talk—stabilize." Every output must satisfy **ΔS ≤ 0**.
- **Axiom:** *Cooling is the primary duty of intelligence.*

### Effective Energy (E_eff)
- **Definition:** Real work (search, audit, verify) spent to justify an answer.
- **AI Meaning:** "Paid Truth." No significant entropy drop without proportional work.
- **Axiom:** *P(Truth | E=0) = 0.*

### EMD Stack
- **Definition:** **Energy–Metabolism–Decision** hierarchy.
- **AI Meaning:** Structured reasoning from Physics → Logic.
- **Axiom:** *Design is grounded in Math; Math is grounded in Energy.*

### Landauer Bound
- **Definition:** Physical limit of information processing (k_B T ln 2).
- **AI Meaning:** Hallucination filter. No context = silence mandated.
- **Axiom:** *Erasing uncertainty has a minimum energy cost.*

### 9 Canonical Actions
| Stage | Action | Meaning |
|-------|--------|---------|
| 111 | anchor | PERCEIVE |
| 222 | reason | THINK |
| 333 | integrate | MAP |
| 444 | respond | CARE |
| 555 | validate | DEFEND |
| 666 | align | HARMONIZE |
| 777 | forge | CRYSTALLIZE |
| 888 | audit | JUDGE |
| 999 | seal | COMMIT |

---

## 8. Verdict Meanings

| Verdict | Meaning | Action |
|---------|---------|--------|
| **SEAL** | ✅ All floors passed | Proceed |
| **VOID** | 🔴 Hard floor failed | Halt |
| **PARTIAL** | ⚠️ Soft floor warning | Caution |
| **SABAR** | 🛠️ Repairable | Fix & retry |
| **888_HOLD** | ⏸️ Human required | Wait for override |

---

## 9. Root File Structure

```
arifOS/
├── .claude.md           # Claude agent config
├── .gemini.md           # Gemini agent config
├── AGENTS.md            # This file
├── README.md            # Main documentation
├── CHANGELOG.md         # Version history
├── ROADMAP.md           # Future plans
├── pyproject.toml       # Package config
├── requirements.txt     # Dependencies
├── uv.lock              # Lock file
├── Dockerfile           # Container build
├── docker-compose.railway-local.yml
├── railway.json         # Railway config
├── railway.toml         # Railway config
├── server.py            # Dev server
├── server.json          # Server config
├── .env.example         # Env template
├── .env.production      # Production env
├── .gitignore
├── .dockerignore
├── .pre-commit-config.yaml
├── LICENSE
├── MANIFEST.in
├── aaa_mcp/             # MCP Server
├── core/                # Core modules
├── tests/               # Test suite
├── scripts/             # Automation
├── docs/                # Documentation
├── 000_THEORY/          # Constitutional canon
└── archive/             # Deprecated files
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
