# arifOS — AI Coding Agent Guide

**Project:** arifOS — Constitutional AI Governance System  
**Version:** 55.5.0-HARDENED  
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
| F2 | Shannon Entropy | Information must reduce uncertainty |
| F4/F6 | Second Law of Thermodynamics | System entropy must not increase (ΔS ≤ 0) |
| F7 | Gödel's Incompleteness | All claims must declare uncertainty bounds (Ω₀ ∈ [0.03, 0.05]) |
| F8 | Eigendecomposition | Intelligence = A×P×X×E² (Akal × Present × Exploration × Energy²) |

---

## 2. Technology Stack

### Core Dependencies
```
fastmcp>=0.1.0          # MCP server framework
pydantic>=2.0.0         # Data validation
fastapi>=0.104.1        # HTTP API
uvicorn[standard]       # ASGI server
sse-starlette>=1.8.2    # SSE transport
mcp>=1.0.0              # MCP SDK
numpy>=1.20.0           # Numerical computation
asyncpg>=0.29.0         # PostgreSQL async driver
rich>=13.7.0            # Terminal formatting
prometheus-client       # Metrics
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
├── aaa_mcp/                    # MCP Server Package (Primary)
│   ├── server.py               # 10 canonical tool definitions
│   ├── __main__.py             # CLI entry: python -m aaa_mcp [stdio|sse|http]
│   ├── core/
│   │   ├── constitutional_decorator.py   # Floor enforcement decorator
│   │   ├── engine_adapters.py            # Bridge to codebase engines
│   │   └── tool_registry.py              # Tool registration
│   ├── services/
│   │   ├── constitutional_metrics.py     # Metrics & evidence
│   │   └── redis_client.py               # Session persistence
│   ├── sessions/
│   │   └── session_ledger.py             # VAULT999 ledger
│   └── tools/
│       └── reality_grounding.py          # Fact-checking
│
├── codebase/                   # Core Engines (Internal)
│   ├── constitutional_floors.py          # F1-F13 floor definitions
│   ├── bundles.py                        # Delta/Omega/Merged bundles
│   ├── agi/                              # Δ MIND engine
│   ├── asi/                              # Ω HEART engine
│   ├── apex/                             # Ψ SOUL engine
│   ├── floors/                           # Individual floor validators
│   ├── guards/                           # Hypervisor guards (F10-F12)
│   └── vault/                            # Persistent ledger
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
│   ├── conftest.py             # Pytest configuration
│   ├── test_mcp_all_tools.py   # MCP integration tests
│   ├── test_pipeline_e2e.py    # End-to-end pipeline
│   └── constitutional/         # Floor enforcement tests
│
├── scripts/                    # Utility Scripts
│   ├── start_server.py         # Production server startup
│   └── *.ps1, *.bat            # Windows/PowerShell helpers
│
├── 000_THEORY/                 # Constitutional Documentation
│   ├── 000_LAW.md              # The 13 Floors specification
│   └── 999_SOVEREIGN_VAULT.md  # VAULT999 specification
│
└── docs/                       # User Documentation
    └── llms.txt                # LLM-optimized constitutional reference
```

---

## 4. Build and Development Commands

### Installation
```bash
# Editable install with dev dependencies
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[all]"
```

### Running the MCP Server
```bash
# stdio transport (default — for local agents like Claude Desktop)
python -m aaa_mcp
# or
aaa-mcp

# SSE transport (for remote/network deployment)
python -m aaa_mcp sse

# HTTP transport (streamable HTTP at /mcp)
python -m aaa_mcp http
```

### Testing
```bash
# Full test suite
pytest tests/ -v

# Quick smoke test (~3 min)
pytest tests/test_mcp_quick.py -v

# All MCP tool integration tests
pytest tests/test_mcp_all_tools.py -v

# End-to-end pipeline
pytest tests/test_pipeline_e2e.py -v

# Constitutional floor tests
pytest -m constitutional -v

# Integration tests only
pytest -m integration -v

# Skip slow tests
pytest -m "not slow" -v

# With coverage
pytest --cov=aaa_mcp tests/ -v
```

**Test Configuration:**
- Async mode is `auto` — no `@pytest.mark.asyncio` needed
- Physics is disabled globally via `conftest.py` (use `enable_physics_for_apex_theory` fixture to opt-in)
- Test files importing legacy `arifos` package are auto-skipped

### Linting and Formatting
```bash
# Format code (100 character line length)
black --line-length 100 aaa_mcp/

# Lint
ruff check aaa_mcp/
ruff check aaa_mcp/ --fix

# Type checking
mypy aaa_mcp/ --ignore-missing-imports
```

---

## 5. Architecture

### Trinity Framework (Three Engines)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  000_INIT   │ →  │  111-333    │ →  │  444-666    │ →  │  777-999    │
│   Ignition  │    │  Δ MIND     │    │  Ω HEART    │    │  Ψ SOUL     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     Auth &           Parse &            Stakeholder         Consensus
   Injection         Reasoning           Impact Analysis      & Seal
     Scan
```

| Engine | Symbol | Role | Floors | Location |
|--------|:------:|------|--------|----------|
| **AGI** | Δ | Mind — reasoning, precision, truth | F2, F4, F7, F10 | `codebase/agi/` |
| **ASI** | Ω | Heart — empathy, safety, alignment | F1, F5, F6, F9 | `codebase/asi/` |
| **APEX** | Ψ | Soul — judgment, equilibrium | F3, F8, F11, F12 | `codebase/apex/` |

### The 13 Constitutional Floors

| Floor | Label | Type | Principle | Threshold | Fail Action |
|:---:|:---|:---:|:---|:---:|:---:|
| F1 | Amanah | HARD | Reversibility | Chain of Custody | VOID |
| F2 | Truth | HARD | Fidelity ≥ 0.99 | Score ≥ 0.99 | VOID |
| F3 | Consensus | DERIVED | Tri-Witness W₃ ≥ 0.95 | W₃ ≥ 0.95 | SABAR |
| F4 | Clarity | HARD | Ambiguity Reduction | ΔS ≤ 0 | VOID |
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

### The 10 Canonical MCP Tools

| # | Tool | Engine | Function | Floors Enforced |
|:---:|:---|:---:|:---|:---|
| 1 | `init_gate` | INIT | Session ignition, auth & injection pre-scan | F11, F12 |
| 2 | `agi_sense` | Δ MIND | Intent classification, assigns HARD/SOFT lanes | F2, F4 |
| 3 | `agi_think` | Δ MIND | Hypothesis generation, explores solution space | F2, F4, F7 |
| 4 | `agi_reason` | Δ MIND | Logic & deduction, step-by-step reasoning | F2, F4, F7 |
| 5 | `reality_search` | Δ MIND | Grounding via web search & Axiom Engine | F2, F10 |
| 6 | `asi_empathize` | Ω HEART | Impact analysis, identifies vulnerable stakeholders | F5, F6 |
| 7 | `asi_align` | Ω HEART | Alignment check for ethics, law, and policy | F9 |
| 8 | `apex_verdict` | Ψ SOUL | Final judgment, synthesizes Truth+Safety | F2, F3, F8 |
| 9 | `vault_seal` | VAULT | Immutable ledger, cryptographic session commit | F1, F3 |
| 10 | `truth_audit` | META | Claim-level truth verification & audit | F2, F4, F7 |

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

# MCP SDK from PyPI — use mcp
from mcp import Client, StdioClientTransport
```

### Decorator Order on MCP Tools

**`@mcp.tool()` must be OUTER, `@constitutional_floor()` must be INNER.**

```python
@mcp.tool()                              # OUTER — FastMCP registration
@constitutional_floor("F2", "F4")        # INNER — floor enforcement
async def my_new_tool(input: str, session_id: str = "") -> dict:
    ...
```

### Floor Types and Enforcement

- **Hard floors** (F1, F2, F4, F7, F10, F11, F12, F13): Failure → **VOID** (blocked)
- **Soft floors** (F3, F5, F6, F8, F9): Failure → **PARTIAL** (warn, proceed with caution)
- **Pre-execution floors** (F1, F5, F11, F12, F13): Validate INPUT before tool runs
- **Post-execution floors** (F2, F3, F4, F6, F7, F8, F9, F10): Validate OUTPUT after tool runs

### SessionState Pattern (Immutable Copy-on-Write)

```python
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")       # Returns NEW instance
new_state = state.set_floor_score(...)   # Returns NEW instance
# Never: state.field = value (mutation forbidden)
```

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
| `tests/constitutional/` | Floor enforcement tests |
| `tests/mcp_tests/` | MCP tool-specific tests |
| `tests/integration/` | Integration tests |
| `tests/archive/` | Legacy tests (auto-skipped) |

### Test Configuration (conftest.py)

- **Physics disabled globally** via `ARIFOS_PHYSICS_DISABLED=1` (performance optimization)
- **Legacy spec bypass** via `ARIFOS_ALLOW_LEGACY_SPEC=1` (test-only)
- Use `enable_physics_for_apex_theory` fixture to opt-in for specific tests

### Adding New Tests

```python
# Test with constitutional marker
@pytest.mark.constitutional
async def test_f2_truth_enforcement():
    result = await agi_reason(query="Test query", session_id="test-001")
    assert result["truth_score"] >= 0.99
```

---

## 8. Deployment Process

### Docker Deployment

```dockerfile
# Build
docker build -t arifos-mcp .

# Run
docker run -p 8080:8080 -e PORT=8080 arifos-mcp
```

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
```

### Railway Deployment

The project includes `railway.json` and `railway.toml` for Railway.app deployment:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python -u scripts/start_server.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```

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

---

## 10. Adding New Components

### New MCP Tool

1. Add tool function with `@mcp.tool()` (outer) and `@constitutional_floor()` (inner) in `aaa_mcp/server.py`
2. Add engine handler in `aaa_mcp/core/engine_adapters.py` (with fallback stub)
3. Update `FLOOR_ENFORCEMENT` dict in `aaa_mcp/core/constitutional_decorator.py`
4. Add tests in `tests/test_mcp_all_tools.py`

### New Floor Validator

1. Create module in `codebase/floors/fX_name.py`
2. Export from `codebase/floors/__init__.py`
3. Wire into `codebase/enforcement/floor_validators.py`
4. Add tests in `tests/constitutional/`

---

## 11. Key Conventions and Gotchas

1. **F4/F6 canonical mapping**: F4 = Clarity (ΔS), F6 = Empathy (κᵣ). If logs show swapped values, that's a schema bug — fix the code, not the documentation.

2. **vault_seal KeyError**: Use `.get("seal", fallback)` to handle unexpected persistence backend formats.

3. **Source Verification Hierarchy**:
   - **PRIMARY**: `spec/*.json`, `canon/*_v38Omega.md` (SEALED status)
   - **SECONDARY**: `codebase/*.py` (implementation reference)
   - **TERTIARY**: `docs/*.md`, `README.md` (informational, may lag)
   - **NOT EVIDENCE**: grep/search results, code comments

4. **APEX Solver Uses Geometric Mean**: The 9-paradox solver uses GM, not arithmetic mean. Target: GM >= 0.85, std dev <= 0.10.

5. **Engine Adapters Fallback**: When real engines from `codebase/` are unavailable, adapters use heuristic stubs that compute scores from query text (Shannon entropy, lexical diversity).

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
