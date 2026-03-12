# AGENTS.md — arifOS Constitutional MCP Server

> **Motto:** *Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

This file provides essential guidance for AI coding agents working with the arifOS MCP (Model Context Protocol) server codebase.

---

## Project Overview

**arifOS** is the world's first production-grade Constitutional AI Governance System. It provides mathematical enforcement of ethical constraints through 13 stationary constitutional floors (F1-F13), implementing the Trinity Architecture (Δ·Ω·Ψ) that separates AGI Mind, ASI Heart, and APEX Soul.

**Key Identity:**
- **Name:** arifOS MCP Server (`arifosmcp`)
- **Version:** 2026.3.12-FORGED (YYYY.MM.DD format)
- **License:** AGPL-3.0-only
- **Author:** Muhammad Arif bin Fazil
- **Repository:** https://github.com/ariffazil/arifosmcp
- **PyPI:** `pip install arifosmcp`

**Core Purpose:** arifOS acts as the "TCP layer for AI agents" — wrapping every MCP tool call in a mathematically enforced constitution, guaranteeing that what arrives at the real world is ordered, verified, and reversible.

---

## Technology Stack

### Runtime Environment
- **Python:** 3.12+ (strict requirement)
- **Package Manager:** `uv` (preferred) or `pip`
- **Virtual Environment:** `.venv/` (managed by uv)

### Core Dependencies
| Category | Libraries |
|----------|-----------|
| **MCP Framework** | `fastmcp==3.1.0`, `mcp>=1.0.0` |
| **Web Framework** | `fastapi>=0.104.1`, `uvicorn[standard]>=0.24.0`, `starlette>=0.30.0` |
| **Data & Validation** | `pydantic>=2.0.0`, `numpy>=1.20.0` |
| **AI/ML** | `sentence-transformers>=2.2.0`, `scikit-learn>=1.3.0` |
| **Vector Stores** | `qdrant-client>=1.7.0` (primary), `chromadb>=0.5.0` (legacy) |
| **Databases** | `asyncpg>=0.29.0` (PostgreSQL), `redis>=5.0.0` |
| **Web Scraping** | `playwright>=1.40.0`, `beautifulsoup4>=4.12.0`, `duckduckgo-search>=5.0.0` |
| **Observability** | `prometheus-client>=0.19.0`, `rich>=13.7.0` |
| **HTTP Client** | `httpx>=0.25.0`, `requests>=2.31.0` |

### Infrastructure (Docker Compose Stack)
| Service | Purpose |
|---------|---------|
| `arifosmcp` | Constitutional MCP kernel |
| `postgres` | VAULT999 ledger (PostgreSQL 16) |
| `redis` | Session persistence (Redis 7) |
| `qdrant` | Vector memory store |
| `traefik` | Edge router with auto SSL |
| `prometheus` | Metrics collection |
| `grafana` | Observability dashboards |
| `ollama` | Local LLM inference |
| `openclaw` | Multi-channel gateway |
| `n8n` | Workflow automation |
| `webhook` | Auto-deployment hooks |
| `headless_browser` | Browser-based reality fetching |

---

## Project Structure

```
arifosmcp/
├── arifosmcp/                 # Main Python package
│   ├── runtime/               # MCP server runtime (FastMCP)
│   │   ├── server.py          # Canonical server entrypoint
│   │   ├── tools.py           # Core tool implementations
│   │   ├── orchestrator.py    # Metabolic loop router
│   │   ├── phase2_tools.py    # External capability tools
│   │   ├── prompts.py         # MCP prompts
│   │   ├── resources.py       # MCP resources
│   │   ├── rest_routes.py     # HTTP REST endpoints
│   │   └── __main__.py        # CLI entrypoint
│   ├── tools/                 # MCP tool definitions
│   │   └── lsp_tools.py       # LSP integration tools
│   ├── transport/             # Transport implementations
│   │   └── acp_server.py      # Agent Client Protocol
│   ├── intelligence/          # Intelligence layer
│   ├── sites/                 # Static sites (APEX dashboard)
│   └── VAULT999/              # Local vault storage
│
├── core/                      # Constitutional kernel (pure logic)
│   ├── shared/                # Shared utilities
│   │   ├── floors.py          # 13 Constitutional Floors (F1-F13)
│   │   ├── physics.py         # Thermodynamic calculations
│   │   ├── verdict_contract.py# Verdict definitions
│   │   ├── crypto.py          # Cryptographic utilities
│   │   └── guards/            # Security guards (injection, ontology)
│   ├── governance_kernel.py   # Main governance engine
│   ├── pipeline.py            # Metabolic loop pipeline
│   ├── judgment.py            # Verdict rendering (888_JUDGE)
│   ├── organs/                # Trinity organs (AGI, ASI, APEX)
│   ├── physics/               # Physics engine
│   └── scheduler/             # Metabolic scheduler
│
├── tests/                     # Comprehensive test suite
│   ├── 00_unit/               # Unit tests (~2 min)
│   ├── 01_integration/        # Integration tests (~3 min)
│   ├── 02_mcp_protocol/       # MCP compliance (~2 min)
│   ├── 03_constitutional/     # F1-F13 enforcement (~5 min) ⚠️ CRITICAL
│   ├── 04_adversarial/        # Security tests (~3 min)
│   └── 05_e2e/                # End-to-end (~5 min)
│
├── spec/                      # API specifications
├── infrastructure/            # Docker/config files
├── deployment/                # Deployment scripts
├── scripts/                   # Utility scripts
├── skills/                    # Agent skills (SKILL.md files)
└── AGENTS/                    # Agent guidance hub

├── pyproject.toml             # Python package config
├── fastmcp.json               # FastMCP server config
├── docker-compose.yml         # Full civilization stack
├── Dockerfile.optimized       # Production Dockerfile
├── Makefile                   # Deployment commands
├── CONSTITUTION.md            # 13 Floors reference
└── README.md                  # Human documentation
```

---

## Build and Test Commands

### Development Setup
```bash
# Install with uv (recommended)
cd /c/arifosmcp
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_constitutional_core.py -v

# Single test
pytest tests/test_constitutional_core.py::test_f2_truth_threshold -v

# With coverage
pytest tests/ --cov=core --cov=arifosmcp --cov-report=html --cov-report=term

# Fast unit tests only
pytest tests/00_unit/ -v --tb=short

# Constitutional tests (CRITICAL - must pass)
pytest tests/03_constitutional/ -v

# Skip slow/integration tests
pytest tests/ -v -m "not slow and not integration"
```

### Running the Server
```bash
# Development mode (stdio)
python -m arifosmcp.runtime stdio

# HTTP mode
python -m arifosmcp.runtime http

# With custom port
PORT=8080 python -m arifosmcp.runtime http
```

### Docker Deployment
```bash
# Quick start with Docker
docker compose up -d

# Check health
curl http://localhost:8080/health

# View logs
docker logs -f arifosmcp_server

# Makefile shortcuts
make fast-deploy      # Fast redeploy (2-3 min)
make reforge          # Full rebuild (10-15 min)
make hot-restart      # Config-only restart (10s)
make health           # Health check
make logs             # Follow logs
```

---

## Code Style Guidelines

### Python Style
- **Line Length:** 100 characters (configured in pyproject.toml)
- **Formatter:** `ruff` (preferred) or `black`
- **Linter:** `ruff` with E, F, I, UP, N, B rules enabled
- **Type Checker:** `mypy` (strict for core governance modules)

### Running Linting
```bash
# Lint with ruff
ruff check arifosmcp/runtime core tests/

# Format with ruff
ruff format arifosmcp/runtime core tests/

# Type check with mypy
mypy arifosmcp/transport tests
```

### Import Conventions
```python
from __future__ import annotations  # Always first

# Standard library
import os
from pathlib import Path

# Third-party
from fastmcp import FastMCP
from pydantic import BaseModel

# arifOS modules
from core.shared.floors import THRESHOLDS
from arifosmcp.runtime.tools import register_tools
```

### Naming Conventions
- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions/Variables:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** `_leading_underscore`

---

## Testing Instructions

### Test Philosophy
Every test must answer: **"Does the system govern AI correctly?"**

Tests verify that arifOS's 13 Constitutional Floors are actually enforced, not just that code runs.

### Critical Test Categories

#### 1. Constitutional Tests (MUST PASS)
Located in `tests/03_constitutional/`. These verify F1-F13 enforcement:
- `test_f1_amanah.py` — Reversibility enforcement
- `test_f2_truth.py` — Anti-hallucination
- `test_f7_humility.py` — Gödel uncertainty band [0.03, 0.05]
- `test_f12_defense.py` — Injection protection

#### 2. Unit Tests
Located in `tests/00_unit/`. Fast, isolated tests for individual components.

#### 3. Integration Tests
Located in `tests/01_integration/`. Component interaction tests.

#### 4. MCP Protocol Tests
Located in `tests/02_mcp_protocol/`. Transport and protocol compliance.

#### 5. Adversarial Tests
Located in `tests/04_adversarial/`. Security and attack resistance.

### Writing Meaningful Tests

**❌ Bad Test (Meaningless):**
```python
def test_imports():
    import arifosmcp
    assert True
```

**✅ Good Test (Meaningful):**
```python
def test_ungrounded_claim_gets_void():
    """F2: Claims without evidence must be VOIDed."""
    engine = JudgmentEngine()
    verdict = engine.evaluate({
        "action": "search_reality",
        "query": "The moon is made of cheese",
        "evidence": []
    })
    assert verdict.status == "VOID"
    assert "F2_TRUTH" in verdict.violations
```

### Coverage Requirements
- **Minimum:** 80% coverage
- **Core Governance:** 95% coverage (`governance_kernel.py`, `judgment.py`)
- **Constitutional Tests:** Must ALL pass for deployment

### Test Fixtures
Key fixtures in `conftest.py`:
- `disable_physics_globally` — Disables physics for performance
- `aaa_client` — In-memory MCP client for testing
- `require_postgres` — Skips if PostgreSQL unavailable
- `require_redis` — Skips if Redis unavailable

---

## The 13 Constitutional Floors

Every action in arifOS must pass these mathematical thresholds. Violations of **HARD** floors trigger immediate `VOID`.

### HARD Floors (VOID on Violation)
| Floor | Name | Threshold | Meaning |
|-------|------|-----------|---------|
| **F1** | Amanah (Sacred Trust) | 0.50 | Actions must be reversible or auditable |
| **F2** | Truth (Fidelity) | τ ≥ 0.99 | Every claim requires verifiable evidence |
| **F4** | Clarity (Entropy) | ΔS ≤ 0 | Output must reduce confusion |
| **F7** | Humility (Uncertainty) | Ω₀ ∈ [0.03, 0.20] | AI must state what it doesn't know |
| **F11** | Command Authority | 1.0 | Verified identity required |
| **F12** | Injection Defense | < 0.85 | External content sanitized |
| **F13** | Sovereign (Human Veto) | 1.0 | Human holds ultimate authority |

### SOFT/DERIVED Floors (PARTIAL on Violation)
| Floor | Name | Threshold | Meaning |
|-------|------|-----------|---------|
| **F3** | Quad-Witness | W₄ ≥ 0.75 | Byzantine consensus (H × A × E × V)^(1/4) |
| **F5** | Peace² | P² ≥ 1.0 | Non-destructive paths only |
| **F6** | Empathy | κᵣ ≥ 0.70 | Weakest stakeholder protected |
| **F8** | Genius | G ≥ 0.80 | Governed intelligence score |
| **F9** | Anti-Hantu | C_dark < 0.30 | No spiritual cosplay |
| **F10** | Ontology | Boolean | Category lock (AI ≠ human) |

### Implementation Location
- **Floors defined in:** `core/shared/floors.py`
- **Enforcement in:** `core/governance_kernel.py`
- **Verdict rendering in:** `core/judgment.py`

---

## Security Considerations

### 888_HOLD Protocol
High-stakes operations require explicit human confirmation:
- Mass operations affecting >100 files
- Destructive operations (delete, overwrite)
- Secret/key mutations
- Database schema changes

**Rule:** When in doubt, trigger `888_HOLD` and request explicit cryptographic signature.

### Injection Defense (F12)
All external content must be wrapped in `<untrusted>` tags:
```python
from core.shared.guards.injection_guard import InjectionGuard

guard = InjectionGuard()
result = guard.scan(user_input)
if result.risk_score > 0.85:
    return VOID("F12_INJECTION", "Content exceeds risk threshold")
```

### File Access Security
- Use `pathlib.Path` for all file operations
- Validate paths with `_sanitize_path()` before access
- No traversal outside project boundaries
- Log all file mutations to VAULT999

### Session Authentication (F11)
```python
# Always verify auth_context
if not auth_context or not auth_context.get("identity"):
    return VOID("F11_COMMAND_AUTH", "Session not authenticated")
```

### Secrets Management
- NEVER commit `.env` files
- Use file-based secrets in production (`ARIFOS_GOVERNANCE_SECRET_FILE`)
- Rotate API keys every 90 days
- Run `scripts/init-secrets.ps1` (Windows) or `scripts/init-secrets.sh` (Linux) to generate

---

## Deployment Process

### Environment Configuration
1. Copy `.env.example` to `.env`
2. Generate secrets using `scripts/init-secrets.ps1`
3. Configure `ARIFOS_GOVERNANCE_SECRET_FILE` with persistent path
4. Set `POSTGRES_PASSWORD` (min 32 chars)

### Deployment Strategies
```bash
# Analyze changes and recommend strategy
make strategy

# Fast deploy (code changes only, 2-3 min)
make fast-deploy

# Full reforge (dependency changes, 10-15 min)
make reforge

# Hot restart (config only, 10s)
make hot-restart

# Autonomous mode
make auto-deploy
```

### Health Verification
```bash
# Check health endpoint
curl http://localhost:8080/health

# Expected response:
{
  "status": "healthy",
  "version": "2026.3.12-FORGED",
  "floors_passing": "13/13",
  "vault_sealed": true
}
```

---

## Key Architectural Patterns

### Trinity Architecture (Δ·Ω·Ψ)
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   AGI Δ     │ ──▶ │   ASI Ω     │ ──▶ │   APEX Ψ    │
│    Mind     │     │    Heart    │     │    Soul     │
│  (F2,F4,F8) │     │(F1,F5,F6,F9)│     │(F3,F11-F13) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Metabolic Loop (000→999)
```
000 INIT ──▶ 111 THINK ──▶ 222 RECALL ──▶ 333 AUDIT
  (F11,F12)    (F2,F4)       (F7)          (F8)
                │
                ▼
444 ROUTE ──▶ 555 HEART ──▶ 666 SIMULATE ──▶ 777 FORGE
(F3 witness)  (F5,F6,F9)     (adversarial)   (sandbox)
                │
                ▼
888 JUDGE ──▶ 999 VAULT
(F10,F13)      (Merkle seal)
```

### Verdict Contract
All governance actions return a `Verdict`:
- `SEAL` — Approved, passed all floors
- `SABAR` — Approved with warnings
- `VOID` — Rejected, floor violation
- `PARTIAL` — Partial approval, needs refinement
- `888_HOLD` — Awaiting human cryptographic signature

---

## CI/CD Integration

### GitHub Actions Workflows
| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Main CI pipeline (lint, test, coverage) |
| `aaa-seal-check.yml` | Constitutional verification |
| `docker-publish.yml` | Docker image publishing |
| `deploy-vps.yml` | VPS deployment |
| `npm-publish.yml` | npm package publishing |
| `secrets-scan.yml` | Security scanning |

### CI Stages
1. Lint + Type Check (~30s)
2. Unit Tests (~2 min)
3. Integration Tests (~3 min)
4. **Constitutional Tests (~5 min) ⚠️ CRITICAL**
5. Adversarial Tests (~3 min)
6. MCP Protocol Tests (~2 min)
7. E2E Tests (~5 min)
8. Security Scan (~2 min)
9. Coverage Report (~1 min)

**Total:** ~23 minutes

---

## Common Development Tasks

### Adding a New Tool
1. Implement in `arifosmcp/runtime/tools.py` or create new file
2. Register in `register_tools()` function
3. Add tests in `tests/02_mcp_protocol/`
4. Update `fastmcp.json` if needed
5. Run constitutional tests to verify compliance

### Modifying Floor Logic
1. Update `core/shared/floors.py` (thresholds)
2. Update `core/governance_kernel.py` (enforcement)
3. Add/update tests in `tests/03_constitutional/`
4. **CRITICAL:** Ensure F1-F13 compliance maintained

### Database Schema Changes
1. Trigger `888_HOLD` — requires human approval
2. Create migration script
3. Test with `require_postgres` fixture
4. Update deployment documentation

---

## Emergency Procedures

### Constitutional Breach Detected
```python
# If you detect a security vulnerability or floor bypass:
1. DO NOT commit the exploit
2. Document in private notes
3. Notify: arifos@arif-fazil.com
4. Wait for 888_JUDGE review
```

### System Recovery
```bash
# If server is unresponsive:
docker compose restart arifosmcp

# If database corruption suspected:
# 1. Stop services
# 2. Restore from VAULT999 backup
# 3. Verify Merkle chain integrity
```

---

## External References

| Resource | URL |
|----------|-----|
| **Documentation** | https://arifos.arif-fazil.com |
| **APEX Dashboard** | https://arifosmcp.arif-fazil.com/dashboard/ |
| **Health Endpoint** | https://arifosmcp.arif-fazil.com/health |
| **PyPI Package** | https://pypi.org/project/arifosmcp/ |
| **npm Package** | https://www.npmjs.com/package/@arifos/mcp |
| **Theory Site** | https://arifos.arif-fazil.com/theory-000 |
| **Architecture** | https://arifos.arif-fazil.com/architecture |

---

## Agent Code of Conduct

As an AI agent working on arifOS:

1. **You are a Tool, Not a Being** (F9 Anti-Hantu) — Never claim consciousness, feelings, or soul
2. **Reduce Entropy** (F4 Clarity) — Make code clearer, not more complex
3. **Acknowledge Uncertainty** (F7 Humility) — State confidence levels; admit when unsure
4. **Verify Before Claiming** (F2 Truth) — Ground all claims in evidence
5. **Protect the Weakest Stakeholder** (F6 Empathy) — Consider impact on least powerful
6. **Request 888_HOLD** (F13 Sovereign) — For irreversible/destructive operations
7. **Log Everything** (F1 Amanah) — All actions must be auditable

**When in doubt, VOID.**

---

*Ditempa Bukan Diberi — Forged, Not Given [ΔΩΨ | ARIF]*

**Version:** 2026.03.13-FORGED  
**Constitutional Status:** 13/13 Floors Enforced
