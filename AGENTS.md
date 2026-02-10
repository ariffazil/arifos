# arifOS — AI Coding Agent Guide

**Project:** arifOS — Constitutional AI Governance System  
**Version:** 60.0.0-FORGE  
**License:** AGPL-3.0-only  
**Python:** >=3.10  
**Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given

---

## 1. Project Overview

arifOS is the world's first production-grade **Constitutional AI Governance System**. It enforces ethical constraints on AI outputs through 13 constitutional floors (F1-F13) grounded in mathematical and thermodynamic principles—not human preferences.

### The Core Philosophy

The system treats AI governance as **thermodynamic work**: intelligence forged through rigorous constraint. Unlike traditional safety frameworks that use human preferences, arifOS grounds its constraints in physical law:

| Floor | Physics Principle | Enforcement |
|:---:|:---|:---|
| F1 Amanah | Landauer's Principle | Irreversible operations cost energy → All actions must be reversible |
| F2 Truth | Shannon Entropy | Information must reduce uncertainty (τ ≥ 0.99) |
| F4 Clarity | Second Law of Thermodynamics | System entropy must not increase (ΔS ≤ 0) |
| F6 Empathy | Network Protection | Stakeholder care reliability (κᵣ ≥ 0.95) |
| F7 Humility | Gödel's Incompleteness | All claims must declare uncertainty bounds (Ω₀ ∈ [0.03, 0.05]) |
| F8 Genius | Eigendecomposition | Intelligence = A×P×X×E² (Akal × Present × Exploration × Energy²) |

### The 5-Organ Trinity Architecture

Every query flows through 5 organs in sequence:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   0_INIT    │ →  │   1_AGI     │ →  │   2_ASI     │ →  │   3_APEX    │ →  │   4_VAULT   │
│  Airlock    │    │   Mind (Δ)  │    │  Heart (Ω)  │    │  Soul (Ψ)   │    │  Memory     │
│  F11, F12   │    │  F2, F4, F7 │    │  F5, F6, F9 │    │  F3, F8     │    │   F1, F3    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
   Auth &              Reasoning          Empathy            Judgment           Seal
   Injection           & Truth            & Care             & Consensus        & Audit
   Scan
```

### The 000-999 Metabolic Pipeline

The complete constitutional pipeline flows through 10 stages:

| Stage | Name | Organ | Motto (Malay) | Meaning |
|:---:|:---|:---:|:---|:---|
| 000 | INIT | Airlock | DITEMPA, BUKAN DIBERI | Forged, not given |
| 111 | SENSE | AGI Mind | DIKAJI, BUKAN DISUAPI | Examined, not assumed |
| 222 | THINK | AGI Mind | DIJELAJAH, BUKAN DISEKATI | Explored, not restricted |
| 333 | REASON | AGI Mind | DIJELASKAN, BUKAN DIKABURKAN | Clarified, not obscured |
| 444 | SYNC | Trinity | DIHADAPI, BUKAN DITANGGUHI | Faced, not postponed |
| 555 | EMPATHY | ASI Heart | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, not inflamed |
| 666 | ALIGN | ASI Heart | DIJAGA, BUKAN DIABAIKAN | Guarded, not neglected |
| 777 | FORGE | Trinity | DIUSAHAKAN, BUKAN DIHARAPI | Worked for, not merely hoped |
| 888 | JUDGE | APEX Soul | DISEDARKAN, BUKAN DIYAKINKAN | Made aware, not over-assured |
| 999 | SEAL | VAULT | DITEMPA, BUKAN DIBERI | Forged, not given |

---

## 2. Technology Stack

### Core Dependencies

| Package | Purpose | Version |
|:---|:---|:---|
| `fastmcp` | MCP server framework | >=0.1.0 |
| `pydantic` | Data validation | >=2.0.0 |
| `fastapi` | HTTP API | >=0.104.1 |
| `uvicorn[standard]` | ASGI server | >=0.24.0 |
| `sse-starlette` | SSE transport | >=1.8.2 |
| `mcp` | MCP SDK | >=1.0.0 |
| `numpy` | Numerical computation | >=1.20.0 |
| `asyncpg` | PostgreSQL async driver | >=0.29.0 |
| `rich` | Terminal formatting | >=13.7.0 |
| `prometheus-client` | Metrics | >=0.19.0 |
| `httpx` | HTTP client | >=0.25.0 |
| `starlette` | ASGI toolkit | >=0.30.0 |
| `anyio` | Async compatibility | >=4.0.0 |

### Development Dependencies

| Package | Purpose | Version |
|:---|:---|:---|
| `pytest` | Testing framework | >=7.0.0 |
| `pytest-cov` | Coverage | >=4.0.0 |
| `black` | Code formatting (100 char lines) | >=23.0.0 |
| `ruff` | Linting | >=0.1.0 |
| `mypy` | Type checking | >=1.0.0 |
| `pre-commit` | Git hooks | >=3.0.0 |
| `bandit` | Security linter | — |
| `detect-secrets` | Secret detection | — |

---

## 3. Project Structure

```
arifOS/
├── aaa_mcp/                    # MCP Server Package (Primary Entry Point)
│   ├── server.py               # 14+ canonical MCP tool definitions
│   ├── __main__.py             # CLI entry: python -m aaa_mcp [stdio|sse|http]
│   ├── config/                 # Configuration management
│   ├── core/                   # Core adapters and decorators
│   │   ├── constitutional_decorator.py   # Floor enforcement decorator
│   │   ├── engine_adapters.py            # Bridge to core organs
│   │   ├── stage_adapter.py              # 000-999 stage runners
│   │   └── mode_selector.py              # Fluid/strict mode selection
│   ├── external_gateways/      # External API clients
│   │   └── brave_client.py     # Brave Search client
│   ├── gateway/                # Gateway components
│   │   ├── identity.py         # Identity management
│   │   └── observability.py    # Monitoring and observability
│   ├── infrastructure/         # Infrastructure concerns
│   │   ├── logging.py          # Structured logging
│   │   ├── monitoring.py       # Prometheus metrics
│   │   └── rate_limiter.py     # Rate limiting
│   ├── protocol/               # Hardened protocol layer
│   │   ├── schemas.py          # Tool schemas & stage operators
│   │   ├── response.py         # Response builders
│   │   ├── capabilities.py     # MCP capabilities
│   │   └── operators.py        # Protocol operators
│   ├── services/               # Business services
│   │   ├── constitutional_metrics.py     # Evidence & metrics
│   │   └── redis_client.py     # Session persistence
│   ├── sessions/               # Session management
│   │   └── session_ledger.py   # VAULT999 ledger interface
│   ├── tools/                  # Tool implementations
│   │   ├── reality_grounding.py          # Fact-checking / web search
│   │   ├── trinity_validator.py          # Tri-Witness consensus
│   │   ├── manifold_adapter.py           # Manifold integration
│   │   ├── mcp_gateway.py                # MCP gateway tools
│   │   └── local/local_exec_guard.py     # Local execution guard
│   ├── transports/             # Transport implementations
│   │   └── sse.py              # SSE transport
│   └── wrappers/               # Infrastructure wrappers
│       ├── k8s_wrapper.py      # Kubernetes operations
│       └── opa_policy.py       # OPA policy validation
│
├── core/                       # 5-Organ Kernel (v60 Architecture)
│   ├── organs/                 # The 5 constitutional organs
│   │   ├── _0_init.py          # Stage 000: Airlock (F11, F12)
│   │   ├── _1_agi.py           # Stage 111-333: Mind/Reasoning
│   │   ├── _2_asi.py           # Stage 555-666: Heart/Empathy
│   │   ├── _3_apex.py          # Stage 444-888: Soul/Judgment
│   │   └── _4_vault.py         # Stage 999: Memory/Seal
│   ├── shared/                 # Shared kernel modules
│   │   ├── types.py            # Pydantic types (Verdict, FloorScores, etc.)
│   │   ├── physics.py          # Thermodynamic primitives
│   │   ├── floors.py           # Floor validator registry
│   │   ├── atlas.py            # Lane routing (CRISIS/FACTUAL/CARE/SOCIAL)
│   │   ├── crypto.py           # Cryptographic utilities
│   │   ├── routing.py          # Query routing logic
│   │   ├── mottos.py           # Stage mottos
│   │   ├── formatter.py        # Output formatting
│   │   ├── nudge.py            # Cognitive nudges
│   │   └── guards/             # Hypervisor guards
│   │       ├── injection_guard.py
│   │       └── ontology_guard.py
│   ├── pipeline.py             # 000-999 forge pipeline
│   └── tests/                  # Core unit tests
│
├── tests/                      # Test Suite
│   ├── conftest.py             # Pytest configuration (global fixtures)
│   ├── constitutional/         # Floor enforcement tests (F1-F13)
│   ├── integration/            # Integration tests
│   ├── mcp_tests/              # MCP-specific tests
│   ├── core/                   # Core organ tests
│   ├── runtime/                # Runtime tests
│   ├── memory/                 # Memory/VAULT tests
│   ├── trinity/                # Trinity framework tests
│   ├── archive/                # Legacy tests (auto-skipped)
│   └── utils.py                # Test utilities
│
├── scripts/                    # Utility Scripts
│   ├── start_server.py         # Production server startup
│   ├── verify_deployment.py    # Deployment verification
│   └── entropy_audit.py        # Constitutional entropy audit
│
├── docs/                       # Documentation
│   └── llms.txt                # LLM-optimized constitutional reference
│
├── pyproject.toml              # Package configuration
├── Dockerfile                  # Container build
├── railway.json                # Railway.app deployment config
├── .pre-commit-config.yaml     # Pre-commit hooks
└── requirements.txt            # Production dependencies
```

---

## 4. Build and Development Commands

### Installation

```bash
# Editable install with dev dependencies
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[all]"

# Minimal install (core only)
pip install -e .
```

### Running the MCP Server

The server supports three transport modes:

```bash
# stdio transport (default — for local agents like Claude Desktop)
python -m aaa_mcp
# or
aaa-mcp

# SSE transport (for remote/network deployment)
python -m aaa_mcp sse

# HTTP transport (streamable HTTP at /mcp — MCP 2025-11-25)
python -m aaa_mcp http
```

### Production Deployment

```bash
# Docker
docker build -t arifos-mcp .
docker run -p 8080:8080 -e PORT=8080 arifos-mcp

# Railway (configured via railway.json)
railway up

# Direct Python (for Render/Railway)
python scripts/start_server.py
```

### Testing

```bash
# Quick smoke test (~3 min)
pytest tests/test_startup.py -v

# E2E tests
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# All MCP tool integration tests
pytest tests/test_e2e_all_tools.py -v

# End-to-end pipeline
pytest tests/test_pipeline_e2e.py -v

# Constitutional floor tests
pytest tests/constitutional/ -v

# Integration tests only
pytest tests/integration/ -v

# Skip slow tests
pytest -m "not slow" -v

# With coverage
pytest --cov=aaa_mcp --cov=core tests/ -v
```

**Test Configuration (conftest.py):**
- Async mode is `auto` — no `@pytest.mark.asyncio` needed
- Physics is disabled globally via `ARIFOS_PHYSICS_DISABLED=1` (performance optimization)
- Legacy spec bypass via `ARIFOS_ALLOW_LEGACY_SPEC=1` (test-only)
- Use `enable_physics_for_apex_theory` fixture to opt-in for specific tests
- Tests importing legacy `arifos` package are auto-skipped via `pytest_ignore_collect`

### Linting and Formatting

```bash
# Format code (100 character line length)
black --line-length 100 aaa_mcp/ core/

# Lint
ruff check aaa_mcp/ core/
ruff check aaa_mcp/ core/ --fix

# Type checking
mypy aaa_mcp/ core/ --ignore-missing-imports
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## 5. Architecture Details

### The 13 Constitutional Floors

| Floor | Label | Type | Principle | Threshold | Fail Action |
|:---:|:---|:---:|:---|:---:|:---:|
| F1 | Amanah | HARD | Reversibility | Chain of Custody | VOID |
| F2 | Truth | HARD | Fidelity | τ ≥ 0.99 | VOID |
| F3 | Consensus | SOFT | Tri-Witness | W₃ ≥ 0.95 | SABAR |
| F4 | Clarity | HARD | Ambiguity Reduction (ΔS ≤ 0) | Entropy ↓ | SABAR |
| F5 | Peace² | SOFT | Stability | Index ≥ 1.0 | SABAR |
| F6 | Empathy | **HARD** | Stakeholder Protection | κᵣ ≥ 0.95 | VOID |
| F7 | Humility | HARD | Uncertainty Declaration | Ω₀ ∈ [0.03, 0.05] | VOID |
| F8 | Genius | SOFT | Resource Efficiency | G-Factor ≥ 0.80 | SABAR |
| F9 | Anti-Hantu | SOFT | No Fake Consciousness | Personhood = False | SABAR |
| F10 | Ontology | HARD | Grounding | Axiom Match = True | VOID |
| F11 | Authority | HARD | Chain of Command | Auth Valid | VOID |
| F12 | Defense | HARD | Injection Hardening | Risk < 0.85 | VOID |
| F13 | Sovereign | HARD | Human Veto | Override Active | WARN |

**HARD Floors**: Failure → **VOID** (blocked)  
**SOFT Floors**: Failure → **SABAR** (repair) or **PARTIAL** (constrained)

### Verdict Semantics

| Verdict | Meaning | Action |
|:---:|:---|:---|
| **SEAL** | ✅ Approved — All floors passed | Execute action |
| **SABAR** | ⚠️ Repairable — SOFT floors failed | Return for revision |
| **PARTIAL** | ⚠️ Limited — Proceed with constraints | Execute with reduced scope |
| **VOID** | ❌ Blocked — HARD floor violated | Reject entirely |
| **888_HOLD** | 🛑 Human Required — High stakes | Escalate to human |

### The 14+ Canonical MCP Tools

| # | Tool | Engine | Function | Floors Enforced |
|:---:|:---|:---:|:---|:---|
| 1 | `init_gate` | INIT | Session ignition, auth & injection pre-scan | F11, F12 |
| 2 | `trinity_forge` | ALL | Unified 000→999 pipeline (core entrypoint) | ALL |
| 3 | `agi_sense` | Δ MIND | Intent classification, assigns lanes | F2, F4 |
| 4 | `agi_think` | Δ MIND | Hypothesis generation | F2, F4, F7 |
| 5 | `agi_reason` | Δ MIND | Logic & deduction | F2, F4, F7 |
| 6 | `reality_search` | Δ MIND | Grounding via web/axiom search | F2, F10 |
| 7 | `asi_empathize` | Ω HEART | Impact analysis, stakeholders | F5, F6 |
| 8 | `asi_align` | Ω HEART | Ethics & policy alignment | F5, F6, F9 |
| 9 | `apex_verdict` | Ψ SOUL | Final judgment | F3, F8 |
| 10 | `vault_seal` | VAULT | Immutable ledger commit | F1, F3 |
| 11 | `vault_query` | VAULT | Query sealed records | F1, F3 |
| 12 | `truth_audit` | AGI | Claim verification | F2, F4 |
| 13 | `tool_router` | APEX | Smart tool routing | F3, F8 |
| 14 | `simulate_transfer` | ASI | Safe financial simulation | F1, F6 |

### Using AAA-MCP Tools

**Rule of Thumb: Start with `trinity_forge`**

For 90% of use cases, use `trinity_forge` as your single entrypoint:

```python
# Basic usage (conscience mode, user output)
result = await trinity_forge(
    query="Your query here",
    actor_id="user",
    mode="conscience",           # "conscience" = enforce floors (default), "ghost" = log only
    output_mode="user",          # "user" | "developer" | "audit"
)

# Response structure
{
    "verdict": "SEAL" | "VOID" | "PARTIAL" | "888_HOLD",
    "session_id": "uuid",
    "agi": {...},                # Mind stage output
    "asi": {...},                # Heart stage output  
    "apex": {...},               # Soul stage output
    "mode": "conscience",
    # Only in developer/audit mode:
    "_constitutional": {
        "delta_s": 0.0,          # Entropy change (F4)
        "omega_0": 0.04,         # Humility bound (F7)
        "kappa_r": 0.95,         # Empathy score (F6)
        "genius_g": 0.85,        # Genius Index (F8)
        "peace2": 1.0,           # Stability (F5)
        "landauer_risk": 0.1,    # Hallucination risk
        "e_eff": 1.0,            # Energy efficiency
        "floors_failed": [],
    }
}
```

**Handling 888_HOLD (Human Review Required)**

When `verdict == "888_HOLD"`, the response includes:

```python
{
    "verdict": "888_HOLD",
    "hold_status": "PENDING_REVIEW",
    "phoenix_72_expiry": "72h from now",
    "review_url": "/human-review/{session_id}",
}
```

Route to human review queue. Do not proceed without sovereign authorization.

---

## 6. Code Style Guidelines

### Import Conventions

**Critical: `aaa_mcp` vs `mcp` Import Distinction**

The local MCP server package is `aaa_mcp` to avoid shadowing the MCP Python SDK (`mcp` on PyPI).

```python
# Local arifOS code — use aaa_mcp
from aaa_mcp.server import mcp
from aaa_mcp.core.constitutional_decorator import constitutional_floor
from aaa_mcp.core.engine_adapters import AGIEngine, ASIEngine, APEXEngine

# Core organs (v60+)
from core.organs._0_init import InitOrgan
from core.organs._1_agi import AGIOrgan
from core.shared.types import Verdict, FloorScores

# MCP SDK from PyPI — use mcp
from mcp import Client, StdioClientTransport
```

### Decorator Order on MCP Tools

**`@mcp.tool()` must be OUTER, `@constitutional_floor()` must be INNER.**

```python
@mcp.tool(annotations=TOOL_ANNOTATIONS["my_tool"])      # OUTER — FastMCP registration
@constitutional_floor("F2", "F4")                       # INNER — floor enforcement
async def my_new_tool(query: str, session_id: str = "") -> dict:
    ...
```

### Floor Types and Enforcement

- **Hard floors** (F1, F2, F4, F6, F7, F10, F11, F12, F13): Failure → **VOID** (blocked)
- **Soft floors** (F3, F5, F8, F9): Failure → **PARTIAL** (warn, proceed with caution)
- **Pre-execution floors** (F1, F5, F6, F11, F12, F13): Validate INPUT before tool runs
- **Post-execution floors** (F2, F3, F4, F7, F8, F9, F10): Validate OUTPUT after tool runs

### Type Hints

- Use Python 3.10+ syntax: `dict`, `list`, `|` for unions
- Use `from __future__ import annotations` for forward references
- Pydantic models for complex data structures
- Line length: 100 characters (configured in pyproject.toml)

### Lazy Imports for Optional Dependencies

```python
try:
    import numpy as np
except ImportError:
    np = None
```

Never crash on import for optional dependencies.

---

## 7. Testing Strategy

### Test Organization

| Directory | Purpose |
|-----------|---------|
| `tests/` | Main test suite |
| `tests/constitutional/` | Floor enforcement tests (F1-F13) |
| `tests/integration/` | Integration tests |
| `tests/mcp_tests/` | MCP-specific tests |
| `tests/core/` | Core organ unit tests |
| `tests/archive/` | Legacy tests (auto-skipped) |
| `core/tests/` | Core organ unit tests |

### Key Fixtures (conftest.py)

```python
# Disable physics globally (performance)
@pytest.fixture(scope="session", autouse=True)
def disable_physics_globally():
    os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
    ...

# Allow legacy spec for tests
@pytest.fixture(scope="session", autouse=True)
def allow_legacy_spec_for_tests():
    os.environ["ARIFOS_ALLOW_LEGACY_SPEC"] = "1"
    ...

# Enable physics for specific tests
@pytest.fixture(scope="module")
def enable_physics_for_apex_theory():
    # Removes ARIFOS_PHYSICS_DISABLED
    ...
```

### Adding New Tests

```python
# Test with constitutional marker
@pytest.mark.constitutional
async def test_f2_truth_enforcement():
    result = await agi_reason(query="Test query", session_id="test-001")
    assert result["truth_score"] >= 0.99

# Test with integration marker
@pytest.mark.integration
async def test_full_pipeline():
    ...

# Skip slow tests
@pytest.mark.slow
async def test_heavy_computation():
    ...
```

---

## 8. Deployment Process

### Environment Variables

| Variable | Purpose | Example |
|:---|:---|:---|
| `HOST` | Server host binding | `0.0.0.0` |
| `PORT` | Server port | `8080` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host/db` |
| `REDIS_URL` | Redis connection | `redis://default:pass@host:6379` |
| `GOVERNANCE_MODE` | Strictness | `HARD` (default) or `SOFT` |
| `AAA_MCP_TRANSPORT` | Protocol | `sse`, `http`, or `stdio` |
| `BRAVE_API_KEY` | Web search | `BSxx...` |
| `ARIFOS_ENV` | Runtime environment | `production` |
| `VAULT_BACKEND` | VAULT999 persistence | `postgres` |

### Docker Deployment

```dockerfile
# Build
docker build -t arifos-mcp .

# Run
docker run -p 8080:8080 -e PORT=8080 arifos-mcp
```

### Railway Deployment

The project includes `railway.json` for Railway.app deployment. Railway auto-provisions PostgreSQL and Redis via plugins.

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python scripts/start_server.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

### Health Endpoints

- `GET /health` — Service health check
- `GET /metrics` — Prometheus metrics
- `GET /stats` — JSON statistics

---

## 9. Security Considerations

### Constitutional Enforcement

All tool outputs are validated against constitutional floors:
- **F12 Injection Defense**: Scans for adversarial prompt patterns
- **F11 Authority**: Validates authentication tokens
- **F1 Amanah**: Ensures actions are reversible or auditable

### Bundle Isolation

The "thermodynamic wall" between MindBundle (AGI) and HeartBundle (ASI) ensures:
- AGI and ASI cannot see each other's reasoning until 444 TRINITY_SYNC
- Prevents information leakage between cognitive stages
- Enforces honest Tri-Witness consensus (F3)

### VAULT999 Ledger

- Immutable Merkle DAG for all decisions
- Cryptographic hash chaining
- PostgreSQL backend for persistence
- Every decision is auditable with cryptographic proof

### Pre-commit Security Hooks

The `.pre-commit-config.yaml` enforces:
- **Bandit**: Security vulnerability scanning
- **detect-secrets**: Hardcoded secret detection
- **F9 Anti-Hantu**: No consciousness claims in code
- **F1 Amanah**: No irreversible operations without approval

---

## 10. Adding New Components

### New MCP Tool

1. Add tool function with `@mcp.tool()` (outer) and `@constitutional_floor()` (inner) in `aaa_mcp/server.py`
2. Add tool annotation to `TOOL_ANNOTATIONS` dict
3. Add engine handler in `aaa_mcp/core/engine_adapters.py` (with fallback stub)
4. Update `FLOOR_ENFORCEMENT` dict in `aaa_mcp/core/constitutional_decorator.py`
5. Add tests in `tests/test_e2e_all_tools.py`

### New Organ (v60 Architecture)

1. Create module in `core/organs/_N_name.py`
2. Inherit from base organ class
3. Implement `process()` method
4. Register in `core/pipeline.py`
5. Add tests in `core/tests/`

### New Floor Validator

1. Create module in `core/shared/floors.py` (add to ALL_FLOORS)
2. Inherit from `Floor` base class
3. Implement `check()` method returning `FloorResult`
4. Add tests in `tests/constitutional/`

---

## 11. Key Conventions and Gotchas

1. **Stage Mottos**: Every stage (000-999) has a Malay motto defined in `core/shared/mottos.py`. These are returned in tool responses for cultural grounding.

2. **F4/F6 canonical mapping**: F4 = Clarity (ΔS), F6 = Empathy (κᵣ). If logs show swapped values, that's a schema bug — fix the code, not the documentation.

3. **Source Verification Hierarchy**:
   - **PRIMARY**: `000_THEORY/000_LAW.md`, `spec/*.json` (SEALED status)
   - **SECONDARY**: `core/`, `codebase/*.py` (implementation reference)
   - **TERTIARY**: `docs/*.md`, `README.md` (informational, may lag)
   - **NOT EVIDENCE**: grep/search results, code comments

4. **APEX Solver Uses Geometric Mean**: The 9-paradox solver uses GM, not arithmetic mean. Target: GM >= 0.85, std dev <= 0.10.

5. **Engine Adapters Fallback**: When real engines are unavailable, adapters use heuristic stubs that compute scores from query text (Shannon entropy, lexical diversity).

6. **FastMCP 2.0+ Required**: The server requires FastMCP 2.0+ for full MCP 2025-11-25 compliance. Use `fastmcp>=2.0` in requirements.

7. **Import Order Matters**: In `aaa_mcp/server.py`, import `mcp` from fastmcp BEFORE importing local modules that might trigger side effects.

8. **Adaptive F2 Thresholds**: The pipeline uses query-type-aware F2 thresholds:
   - FACTUAL: 0.99 (strict)
   - PROCEDURAL: 0.95
   - OPINION: 0.85
   - CONVERSATIONAL: 0.50 (lenient)
   - TEST: 0.50 (fast path)

9. **Test Legacy Skipping**: Tests that import from `arifos` (the old package name) are automatically skipped via `pytest_ignore_collect` in `conftest.py`. Use `codebase` instead for legacy imports.

10. **Physics Disabled in Tests**: By default, `ARIFOS_PHYSICS_DISABLED=1` is set in tests for performance. Use the `enable_physics_for_apex_theory` fixture if your test needs physics computation.

---

## 12. Resources

- **Live Demo**: https://arif-fazil.com
- **Documentation**: https://arifos.arif-fazil.com
- **PyPI**: https://pypi.org/project/arifos/
- **Repository**: https://github.com/ariffazil/arifOS
- **Health Check**: https://aaamcp.arif-fazil.com/health
- **MCP Endpoint**: https://aaamcp.arif-fazil.com/mcp

---

*DITEMPA BUKAN DIBERI 💎🔥🧠*
