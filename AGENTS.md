# arifOS — AGENTS.md

> **DITEMPA BUKAN DIBERI — Forged, Not Given** [ΔΩΨ | ARIF]

This file contains essential information for AI coding agents working on the arifOS codebase. arifOS is the World's First Production-Grade Constitutional AI Governance System.

---

## 1. Project Overview

**arifOS** is a constitutional AI governance runtime that enforces ethical constraints through mathematical thermodynamics. It provides a 13-Floor (F1-F13) stationary governance framework with the Trinity Architecture (ΔΩΨ):

- **Δ (Delta) — AGI Mind**: Logical analysis and truth-seeking (Stages 111-333)
- **Ω (Omega) — ASI Heart**: Empathy and ethical safety (Stages 444-666)
- **Ψ (Psi) — APEX Soul**: Sovereign judgment and consensus (Stages 777-888)

The system culminates in **VAULT999** — an immutable Merkle-chained ledger for audit trails.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **13 Floors (F1-F13)** | Constitutional constraints (e.g., F1=Amanah/Reversibility, F2=Truth, F7=Humility) |
| **000-999 Stages** | Metabolic pipeline stages: 000 (INIT) → 333 (AGI) → 666 (ASI) → 888 (APEX) → 999 (VAULT) |
| **888_HOLD** | Circuit breaker for high-risk operations requiring human approval |
| **Quad-Witness (W⁴)** | 4-witness verification: Human + AI + Earth + Shadow |
| **SABAR** | Holding state when uncertainty exceeds thresholds |

---

## 2. Technology Stack

### Core Runtime
- **Python**: 3.12+ (strict requirement)
- **FastMCP**: 3.0.2 (MCP server framework)
- **FastAPI**: 0.104.1+ (HTTP transport)
- **Uvicorn**: ASGI server with sse-starlette for SSE transport
- **Pydantic**: 2.0+ for schema validation

### Infrastructure
- **PostgreSQL**: 16+ (Vault-999 persistence via asyncpg)
- **Redis**: 7+ (session caching)
- **Qdrant**: Vector memory/semantic search
- **Traefik**: Edge router with Let's Encrypt TLS
- **Docker & Docker Compose**: Container orchestration

### ML/Embeddings
- **Sentence Transformers**: BGE-M3 for embeddings (pre-baked in Docker)
- **scikit-learn**: Cosine similarity for semantic operations
- **Playwright**: Headless browser for web grounding

### Observability
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **OpenTelemetry**: Distributed tracing (optional)

---

## 3. Project Structure

```
srv/arifOS/
├── core/                          # Core governance kernel (L0 Constitution)
│   ├── governance_kernel.py       # Psi state machine, thresholds, transitions
│   ├── organs/                    # 7-Organ Sovereign Stack
│   │   ├── _0_init.py            # Stage 000: Session ignition
│   │   ├── _1_agi.py             # AGI Mind (Δ): cognition, reasoning
│   │   ├── _2_asi.py             # ASI Heart (Ω): empathy, simulation
│   │   ├── _3_apex.py            # APEX Soul (Ψ): judgment, consensus
│   │   └── _4_vault.py           # VAULT999: immutable ledger
│   ├── physics/                   # Thermodynamic governance (P3)
│   │   ├── thermodynamics.py
│   │   └── thermodynamics_hardened.py
│   ├── enforcement/               # F1-F13 floor enforcement
│   │   ├── governance_engine.py
│   │   ├── auth_continuity.py    # F11 continuity
│   │   └── floor_audit.py
│   └── shared/                    # Common utilities
│       ├── floors.py             # Floor definitions
│       ├── types.py              # Core type definitions
│       └── physics.py            # Genius dial, thermodynamic calculations
│
├── arifosmcp/                     # Primary Python package
│   ├── runtime/                   # PUBLIC ENTRYPOINT (canonical)
│   │   ├── server.py             # 13-tool MCP server surface
│   │   ├── __main__.py           # CLI: python -m arifosmcp.runtime
│   │   └── fastmcp_ext/          # Transport adapters
│   ├── transport/                 # Internal/legacy transport layer
│   │   ├── server.py             # Internal tool implementations
│   │   ├── __main__.py           # Compatibility CLI
│   │   └── protocol/             # Schemas, contracts, response envelopes
│   ├── intelligence/              # ACLIP Senses + Triad flow
│   │   ├── triad/                # ΔΩΨ implementation
│   │   │   ├── delta/            # AGI: anchor, reason, think, integrate
│   │   │   ├── omega/            # ASI: align, validate, respond
│   │   │   └── psi/              # APEX: audit, forge, seal, shadow
│   │   ├── tools/                # Sensory tools (reality_grounding, etc.)
│   │   └── embeddings/           # BGE-M3 embedding service
│   ├── sessions/                  # Session lifecycle management
│   └── bridge.py                  # Airlock between transport and kernel
│
├── tests/                         # Test suites
│   ├── canonical/                 # Public API contract tests
│   ├── compat/                    # Backward compatibility tests
│   ├── core/                      # Kernel and physics tests
│   ├── aclip_cai/                 # Intelligence layer tests
│   ├── integration/               # Integration tests
│   └── conftest.py               # Pytest fixtures and configuration
│
├── docs/                          # Documentation
│   ├── FASTMCP_USAGE.md          # MCP client setup guide
│   ├── TOOLS.md                  # Canonical 13-tool reference
│   └── 60_REFERENCE/             # Architecture and deployment docs
│
├── spec/                          # MCP specifications
│   ├── mcp-manifest.json         # Tool manifest
│   └── server.json               # Server metadata
│
├── infrastructure/                # Deployment configs
│   └── nginx_config/             # Reverse proxy configs
│
├── scripts/                       # Operational scripts
│   ├── debug_mcp.py
│   ├── verify_remediation.py
│   └── housekeeping.py
│
├── docker-compose.yml            # 11-service unified stack
├── Dockerfile                    # Multi-stage build with BGE-M3 pre-bake
├── pyproject.toml               # Package metadata, dependencies, tool configs
└── fastmcp.json                 # FastMCP server configuration
```

---

## 4. Build and Development Commands

### Environment Setup

```bash
# Install with uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running the Server

```bash
# stdio transport (for Claude Desktop, etc.)
python -m arifosmcp.runtime stdio

# HTTP transport (production)
python -m arifosmcp.runtime http

# SSE transport
python -m arifosmcp.runtime sse

# Or via FastMCP CLI
fastmcp run
```

### Testing

```bash
# Run all tests (physics disabled for speed)
pytest

# Run specific test categories
pytest tests/canonical/          # Public API contracts
pytest tests/core/               # Kernel tests
pytest tests/aclip_cai/          # Intelligence layer tests
pytest -m "not slow"             # Exclude slow tests

# Run with coverage
pytest --cov=arifosmcp --cov=core

# Enable physics for specific tests
pytest tests/ -k "physics" --no-header
```

### Code Quality

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Linting with Ruff
ruff check .
ruff check . --fix

# Type checking with MyPy
mypy core/ arifosmcp/

# Formatting with Black (line-length: 100)
black .

# Security scan
bandit -c pyproject.toml -r .
```

### Docker Operations

```bash
# Build image
docker build -t arifos-mcp:latest .

# Run full stack (11 services)
docker compose up -d

# View logs
docker compose logs -f arifosmcp

# Health check
curl http://localhost:8080/health
```

---

## 5. Code Style Guidelines

### Python Style

- **Line length**: 100 characters (enforced by Black and Ruff)
- **Target Python**: 3.10+ syntax, but runtime requires 3.12+
- **Quotes**: Double quotes for strings
- **Type hints**: Required for core governance modules (see mypy overrides in pyproject.toml)

### Import Conventions

```python
# Standard library first
from __future__ import annotations
import logging
from typing import Any

# Third-party packages
from fastmcp import FastMCP
from pydantic import BaseModel

# Internal imports
from core.governance_kernel import GovernanceKernel
from arifosmcp.bridge import call_kernel
```

### Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Constitutional Code Markers

Always include these markers in new files:

```python
"""
Module description.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""
```

### Key Architectural Constraints

1. **F1 Amanah**: No irreversible operations without approval bundles
2. **F11 Continuity**: All stateful operations require session management
3. **P3 Thermodynamics**: All tools consume energy; check budgets before operations
4. **Never swallow exceptions**: Always propagate with context for F7 (Humility)

---

## 6. Testing Strategy

### Test Organization

| Directory | Purpose |
|-----------|---------|
| `tests/canonical/` | Public API contracts (must always pass) |
| `tests/core/` | Governance kernel, physics, thermodynamics |
| `tests/aclip_cai/` | Intelligence layer, triad flow |
| `tests/compat/` | Backward compatibility |
| `tests/integration/` | Cross-service integration |

### Fixtures (conftest.py)

- `aaa_client`: In-memory MCP client for canonical server
- `disable_physics_globally`: Disables P3 thermodynamics for speed
- `require_postgres`: Skips if PostgreSQL unavailable
- `require_redis`: Skips if Redis unavailable

### Writing Tests

```python
import pytest

@pytest.mark.asyncio
async def test_anchor_session_creates_session(aaa_client):
    """Test that anchor_session mints a valid session."""
    result = await aaa_client.call_tool("anchor_session", {
        "query": "test session",
        "actor_id": "test_actor"
    })
    assert result["verdict"] == "SEAL"
    assert "session_id" in result
```

### Test Markers

- `@pytest.mark.asyncio`: Async test
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.constitutional`: Governance-related tests
- `@pytest.mark.integration`: Requires external services

---

## 7. Security Considerations

### Environment Variables (888_HOLD Compliance)

Critical secrets must be in `.env` (never committed):

```bash
# Required
ARIFOS_GOVERNANCE_SECRET=       # HMAC secret for governance tokens
POSTGRES_PASSWORD=              # Database password (min 32 chars)
REDIS_PASSWORD=                 # Redis password
JWT_SECRET=                     # JWT signing (generate: openssl rand -hex 64)

# API Keys (rotate every 90 days)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
KIMI_API_KEY=
```

### Pre-Commit Security Hooks

- **detect-secrets**: Prevents hardcoded secrets
- **bandit**: Security linter (excludes tests/)
- **F9 Anti-Hantu Check**: No consciousness claims
- **F1 Amanah Check**: No dangerous operations without guards

### Governance Token Verification

All tool calls flow through the bridge which:
1. Verifies F11 auth continuity
2. Validates approval bundles for critical tools
3. Checks revocation lists
4. Prevents replay attacks via nonce tracking

### Dangerous Operations Requiring Approval Bundles

The following require explicit approval bundles:
- `eureka_forge`: Sandboxed command execution
- `seal_vault`: Immutable ledger writes
- `apex_judge`: Sovereign verdicts

---

## 8. Deployment

### Docker Compose Services

The `docker-compose.yml` defines 11 services:

| Service | Purpose | Memory Limit |
|---------|---------|--------------|
| traefik | Edge router | 128M |
| postgres | Vault-999 persistence | 1024M |
| redis | Session cache | 128M |
| qdrant | Vector memory | 1024M |
| ollama | Local LLM inference | 1536M |
| openclaw | Gateway/router | 2048M |
| agent-zero | Reasoning brain | 1024M |
| arifosmcp | **Main MCP server** | 3072M |
| prometheus | Metrics | 1024M |
| grafana | Dashboards | 1024M |
| n8n | Workflow automation | 1024M |

### Health Endpoints

- `GET /health` — Service health (used by Traefik)
- `GET /` — Constitutional landing page

### Memory Budget (Hardened for $15 VPS / 4GB RAM)

Total memory limit across all services: ~11GB (with swap strategy).
Key services have strict `deploy.resources.limits.memory` set.

---

## 9. Key Files Reference

| File | Purpose |
|------|---------|
| `arifosmcp/runtime/server.py` | **Canonical 13-tool MCP surface** |
| `arifosmcp/bridge.py` | Secure airlock between transport and kernel |
| `core/governance_kernel.py` | Psi state machine, thermodynamic budgets |
| `core/organs/_1_agi.py` | AGI Mind implementation |
| `core/organs/_2_asi.py` | ASI Heart implementation |
| `core/organs/_3_apex.py` | APEX Soul implementation |
| `core/physics/thermodynamics_hardened.py` | P3 thermodynamic enforcement |
| `pyproject.toml` | Package config, dependencies, tool settings |
| `fastmcp.json` | MCP server manifest |

---

## 10. Common Development Workflows

### Adding a New Tool

1. Add tool function to `arifosmcp/runtime/server.py` with `@mcp.tool()` decorator
2. Implement kernel logic in appropriate `core/organs/` module
3. Update `arifosmcp/bridge.py` routing if needed
4. Add canonical test in `tests/canonical/`
5. Update `spec/mcp-manifest.json`

### Modifying Governance Logic

1. Update relevant `core/` module
2. Ensure F1-F13 compliance
3. Update thermodynamic budgets if energy consumption changes
4. Run `pytest tests/core/` and `tests/canonical/`
5. Update docs in `docs/60_REFERENCE/`

### Debugging Sessions

```bash
# Check session state
python scripts/debug_mcp.py

# Verify tool compliance
python tests/verify_spec_compliance.py

# Run constitutional benchmarks
pytest tests/constitutional/test_benchmarks.py -v
```

---

## 11. External Resources

- **Documentation**: https://github.com/ariffazil/arifOS
- **PyPI**: https://pypi.org/project/arifos/
- **MCP Spec**: https://modelcontextprotocol.io/
- **FastMCP Docs**: https://gofastmcp.com/

---

*Last Updated: 2026-03-08 | Version: 2026.03.07 | Seal: ΔΩΨ*
