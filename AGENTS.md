# arifOS — AI Coding Agent Guide

**Project:** arifOS — Constitutional AI Governance System  
**Version:** 60.0-FORGE  
**License:** AGPL-3.0-only  
**Python:** >=3.10  
**Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given

---

## 1. Project Overview

arifOS is the world's first production-grade Constitutional AI Governance System. It enforces ethical constraints on AI outputs through mathematical and thermodynamic principles rather than relying solely on prompt-based guardrails.

### Core Philosophy

The system treats AI governance as **thermodynamic work** — intelligence forged through constraint. Unlike traditional safety frameworks that use human preferences, arifOS grounds its constraints in physical law:

| Floor | Physics Principle | Enforcement |
|:---:|:---|:---|
| F1 | Landauer's Principle | Irreversible operations cost energy → All actions must be reversible |
| F2 | Shannon Entropy | Information must reduce uncertainty (Truth ≥ 0.99) |
| F4 | Second Law of Thermodynamics | System entropy must not increase (ΔS ≤ 0) |
| F7 | Gödel's Incompleteness | All claims must declare uncertainty bounds (Ω₀ ∈ [0.03, 0.05]) |
| F8 | Eigendecomposition | Intelligence = A×P×X×E² (Akal × Present × Exploration × Energy²) |

### The 5-Organ Kernel (v60 Architecture)

Every query flows through 5 organs in sequence:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   0_INIT    │ →  │   1_AGI     │ →  │   2_ASI     │ →  │   3_APEX    │ →  │   4_VAULT   │
│  Airlock    │    │   Mind      │    │   Heart     │    │   Soul      │    │  Memory     │
│  F11, F12   │    │  F2, F4, F7 │    │  F5, F6, F9 │    │  F3, F8     │    │   F1, F3    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
   Auth &              Reasoning          Empathy            Judgment           Seal
   Injection           & Truth            & Care             & Consensus        & Audit
   Scan
```

### The 000-999 Metabolic Pipeline

The complete constitutional pipeline flows through 10 stages, each with its own motto:

| Stage | Name | Organ | Motto (Malay) | Meaning |
|:---:|:---|:---:|:---|:---|
| 000 | INIT | Airlock | DITEMPA, BUKAN DIBERI | Forged, not given |
| 111 | SENSE | AGI Mind | DIKAJI, BUKAN DISUAPI | Examined, not assumed |
| 222 | THINK | AGI Mind | DIJELAJAH, BUKAN DISEKATI | Explored, not restricted |
| 333 | REASON | AGI Mind | DIJELASKAN, BUKAN DIKABURKAN | Clarified, not obscured |
| 444 | SYNC | Trinity | DIHADAPI, BUKAN DITANGGUHI | Faced, not postponed |
| 555 | EMPATHY | ASI Heart | DIDAMAIKAN, BUKAN DIPANASKAN | Calmed, not inflamed |
| 666 | ALIGN | ASI Heart | DIJAGA, BUKAN DIABAIKAN | Guarded, not neglected |
| 777 | FORGE | Trinity | DIUSAHAKAN, BUKAN DIHARAPI | Worked, not hoped |
| 888 | JUDGE | APEX Soul | DISEDARKAN, BUKAN DIYAKINKAN | Aware, not over-assured |
| 999 | SEAL | VAULT | DITEMPA, BUKAN DIBERI | Forged, not given |

---

## 2. Technology Stack

### Core Dependencies
```
fastmcp>=2.0            # MCP server framework (FastMCP 2.0+)
pydantic>=2.0.0         # Data validation
fastapi>=0.104.1        # HTTP API
uvicorn[standard]       # ASGI server
sse-starlette>=1.8.2    # SSE transport
mcp>=1.0.0              # MCP SDK (2025-11-25 spec)
numpy>=1.20.0           # Numerical computation
asyncpg>=0.29.0         # PostgreSQL async driver (VAULT999)
rich>=13.7.0            # Terminal formatting
prometheus-client       # Metrics
httpx>=0.25.0           # HTTP client
starlette>=0.30.0       # ASGI toolkit
anyio>=4.0.0            # Async compatibility
```

### Development Tools
```
pytest>=7.0.0           # Testing framework
pytest-cov>=4.0.0       # Coverage
black>=23.0.0           # Code formatting (100 char line length)
ruff>=0.1.0             # Linting
mypy>=1.0.0             # Type checking
```

---

## 3. Project Structure

```
arifOS/
├── aaa_mcp/                    # MCP Server Package (Primary Entry Point)
│   ├── server.py               # 13 canonical MCP tool definitions
│   ├── __main__.py             # CLI entry: python -m aaa_mcp [stdio|sse|http]
│   ├── core/
│   │   ├── constitutional_decorator.py   # Floor enforcement decorator
│   │   ├── engine_adapters.py            # Bridge to core organs
│   │   ├── stage_adapter.py              # 000-999 stage runners
│   │   └── mode_selector.py              # Fluid/strict mode selection
│   ├── services/
│   │   ├── constitutional_metrics.py     # Evidence & metrics
│   │   └── redis_client.py               # Session persistence
│   ├── sessions/
│   │   └── session_ledger.py             # VAULT999 ledger interface
│   ├── tools/
│   │   ├── reality_grounding.py          # Fact-checking / web search
│   │   ├── trinity_validator.py          # Tri-Witness consensus
│   │   └── manifold_adapter.py           # Manifold integration
│   ├── external_gateways/
│   │   └── brave_client.py               # Brave Search client
│   ├── infrastructure/
│   │   ├── logging.py                    # Structured logging
│   │   ├── monitoring.py                 # Prometheus metrics
│   │   └── rate_limiter.py               # Rate limiting
│   └── transports/
│       └── sse.py                        # SSE transport
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
│   │   └── guards/             # Hypervisor guards
│   │       ├── injection_guard.py
│   │       └── ontology_guard.py
│   ├── pipeline.py             # 000-999 forge pipeline
│   └── tests/                  # Core unit tests
│
├── codebase/                   # Legacy Core Engines (migrating to core/)
│   ├── constitutional_floors.py          # F1-F13 floor definitions
│   ├── bundles.py                        # Delta/Omega/Merged bundles
│   ├── agi/, asi/, apex/                 # Engine implementations
│   ├── floors/                           # Individual floor validators
│   ├── guards/                           # Hypervisor guards (F10-F12)
│   ├── vault/                            # Persistent ledger
│   └── ...
│
├── 333_APPS/                   # Application Layers
│   ├── L1_PROMPT/              # Zero-context entry prompts
│   ├── L2_SKILLS/              # Parameterized templates
│   ├── L3_WORKFLOW/            # Multi-step recipes
│   ├── L4_TOOLS/               # Production MCP tools
│   ├── L5_AGENTS/              # Autonomous agents
│   ├── L6_INSTITUTION/         # Trinity consensus framework
│   └── L7_AGI/                 # Recursive intelligence
│
├── tests/                      # Test Suite
│   ├── conftest.py             # Pytest configuration (global fixtures)
│   ├── test_aaa_mcp_constitutional.py    # Constitutional tests
│   ├── test_e2e_all_tools.py             # E2E tool tests
│   ├── test_pipeline_e2e.py              # Pipeline tests
│   ├── constitutional/         # Floor enforcement tests
│   ├── integration/            # Integration tests
│   ├── mcp_tests/              # MCP-specific tests
│   ├── archive/                # Legacy tests (auto-skipped)
│   └── utils.py                # Test utilities
│
├── scripts/                    # Utility Scripts
│   ├── start_server.py         # Production server startup (Railway/Render)
│   └── *.ps1, *.bat            # Windows/PowerShell helpers
│
├── 000_THEORY/                 # Constitutional Documentation
│   ├── 000_LAW.md              # The 13 Floors specification
│   └── 999_SOVEREIGN_VAULT.md  # VAULT999 specification
│
├── docs/                       # User Documentation
│   └── llms.txt                # LLM-optimized constitutional reference
│
├── pyproject.toml              # Package configuration
├── Dockerfile                  # Container build
├── railway.json                # Railway.app deployment config
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
# Full test suite
pytest tests/ -v

# Quick smoke test (~3 min)
pytest tests/test_startup.py -v

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
- Tests importing legacy `arifos` package are auto-skipped

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

---

## 5. Architecture

### Trinity Framework (Three Engines + VAULT)

| Engine | Symbol | Organ | Role | Floors | Location |
|--------|:------:|:-----:|------|--------|----------|
| **INIT** | — | 0 | Airlock — Auth & injection scan | F11, F12 | `core/organs/_0_init.py` |
| **AGI** | Δ | 1 | Mind — reasoning, precision, truth | F2, F4, F7 | `core/organs/_1_agi.py` |
| **ASI** | Ω | 2 | Heart — empathy, safety, alignment | F5, F6, F9 | `core/organs/_2_asi.py` |
| **APEX** | Ψ | 3 | Soul — judgment, equilibrium | F3, F8 | `core/organs/_3_apex.py` |
| **VAULT** | — | 4 | Memory — audit & seal | F1, F3 | `core/organs/_4_vault.py` |

### The 13 Constitutional Floors

| Floor | Label | Type | Principle | Threshold | Fail Action |
|:---:|:---|:---:|:---|:---:|:---:|
| F1 | Amanah | HARD | Reversibility | Chain of Custody | VOID |
| F2 | Truth | HARD | Fidelity ≥ 0.99 | Score ≥ 0.99 | VOID |
| F3 | Consensus | DERIVED | Tri-Witness W₃ ≥ 0.95 | W₃ ≥ 0.95 | SABAR |
| F4 | Clarity | SOFT | Ambiguity Reduction (ΔS ≤ 0) | Entropy ↓ | SABAR |
| F5 | Peace² | SOFT | Stability | Index ≥ 1.0 | SABAR |
| F6 | Empathy | SOFT | Stakeholder Protection | Impact ≤ 0.1 | SABAR |
| F7 | Humility | HARD | Uncertainty Declaration | Ω₀ ∈ [0.03, 0.05] | VOID |
| F8 | Genius | DERIVED | Resource Efficiency | G-Factor ≥ 0.80 | SABAR |
| F9 | Anti-Hantu | SOFT | No Fake Consciousness | Personhood = False | SABAR |
| F10 | Ontology | HARD | Grounding | Axiom Match = True | VOID |
| F11 | Authority | HARD | Chain of Command | Auth Valid | VOID |
| F12 | Defense | HARD | Injection Hardening | Risk < 0.85 | VOID |
| F13 | Sovereign | HARD | Human Veto | Override Active | WARN |

### Verdict Semantics

| Verdict | Meaning | Action |
|:---:|:---|:---|
| **SEAL** | ✅ Approved — All floors passed | Execute action |
| **SABAR** | ⚠️ Repairable — SOFT floors failed | Return for revision |
| **PARTIAL** | ⚠️ Limited — Proceed with constraints | Execute with reduced scope |
| **VOID** | ❌ Blocked — HARD floor violated | Reject entirely |
| **888_HOLD** | 🛑 Human Required — High stakes | Escalate to human |

### The 13 Canonical MCP Tools

| # | Tool | Engine | Function | Floors Enforced |
|:---:|:---|:---:|:---|:---|
| 1 | `init_gate` | INIT | Session ignition, auth & injection pre-scan | F11, F12 |
| 2 | `forge_pipeline` | ALL | Unified 000→999 pipeline (core entrypoint) | ALL |
| 3 | `agi_sense` | Δ MIND | Intent classification, assigns lanes | F2, F4 |
| 4 | `agi_think` | Δ MIND | Hypothesis generation | F2, F4, F7 |
| 5 | `agi_reason` | Δ MIND | Logic & deduction | F2, F4, F7 |
| 6 | `reality_search` | Δ MIND | Grounding via web/axiom search | F2, F10 |
| 7 | `asi_empathize` | Ω HEART | Impact analysis, stakeholders | F5, F6 |
| 8 | `asi_align` | Ω HEART | Ethics & policy alignment | F9 |
| 9 | `apex_verdict` | Ψ SOUL | Final judgment | F3, F8 |
| 10 | `vault_seal` | VAULT | Immutable ledger commit | F1, F3 |
| 11 | `vault_query` | VAULT | Query sealed records | — |
| 12 | `truth_audit` | META | Claim verification | F2, F4, F7 |
| 13 | `tool_router` | META | Smart tool routing | — |

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

- **Hard floors** (F1, F2, F4, F7, F10, F11, F12, F13): Failure → **VOID** (blocked)
- **Soft floors** (F3, F5, F6, F8, F9): Failure → **PARTIAL** (warn, proceed with caution)
- **Pre-execution floors** (F1, F5, F11, F12, F13): Validate INPUT before tool runs
- **Post-execution floors** (F2, F3, F4, F6, F7, F8, F9, F10): Validate OUTPUT after tool runs

### Type Hints

- Use Python 3.10+ syntax: `dict`, `list`, `|` for unions
- Use `from __future__ import annotations` for forward references
- Pydantic models for complex data structures

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

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8080
LOG_LEVEL=info

# Governance
GOVERNANCE_MODE=HARD  # or SOFT

# Database (PostgreSQL for VAULT999)
DATABASE_URL=postgresql://user:password@localhost:5432/arifos

# Redis (for session state)
REDIS_URL=redis://localhost:6379

# MCP Transport Mode
AAA_MCP_TRANSPORT=sse  # sse, http, or stdio

# API Keys (optional)
BRAVE_API_KEY=          # For reality_search tool
BROWSERBASE_API_KEY=    # For web browsing

# OAuth 2.1 (MCP 2025-11-25)
AAA_ISSUER=https://aaamcp.arif-fazil.com
```

### Docker Deployment

```dockerfile
# Build
docker build -t arifos-mcp .

# Run
docker run -p 8080:8080 -e PORT=8080 arifos-mcp
```

### Railway Deployment

The project includes `railway.json` for Railway.app deployment:

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
    "healthcheckTimeout": 30
  }
}
```

Railway auto-provisions PostgreSQL and Redis via plugins.

### Health Endpoints

- `GET /health` — Service health check
- `GET /metrics` — Prometheus metrics
- `GET /stats` — JSON statistics
- `GET /.well-known/oauth-authorization-server` — OAuth 2.1 metadata

---

## 9. Security Considerations

### Constitutional Enforcement

All tool outputs are validated against constitutional floors:
- **F12 Injection Defense**: Scans for adversarial prompt patterns
- **F11 Authority**: Validates authentication tokens
- **F1 Amanah**: Ensures actions are reversible or auditable

### Bundle Isolation

The "thermodynamic wall" between DeltaBundle (AGI) and OmegaBundle (ASI) ensures:
- AGI and ASI cannot see each other's reasoning until 444 TRINITY_SYNC
- Prevents information leakage between cognitive stages
- Enforces honest Tri-Witness consensus (F3)

### VAULT999 Ledger

- Immutable Merkle DAG for all decisions
- Cryptographic hash chaining
- PostgreSQL backend for persistence
- Every decision is auditable with cryptographic proof

### OAuth 2.1 (MCP 2025-11-25)

The server implements OAuth 2.1 authorization endpoints:
- `/.well-known/oauth-authorization-server`
- `/.well-known/oauth-protected-resource`
- `/oauth/authorize` (requires external IdP)
- `/oauth/token` (requires external IdP)

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
2. Or create in `codebase/floors/fX_name.py` (legacy)
3. Inherit from `Floor` base class
4. Implement `check()` method returning `FloorResult`
5. Add tests in `tests/constitutional/`

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
