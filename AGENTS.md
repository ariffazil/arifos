# AGENTS.md — arifOS Agent Playbook

**Project:** `arifOS` — Constitutional AI Governance System  
**Package:** `arifos` | **Version:** 2026.3.1 | **Python:** >=3.12 | **License:** AGPL-3.0-only

> *Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

This file guides AI coding agents working in this repository. When sources conflict, instruction precedence is:  
1) `AGENTS.md` (this file)  
2) `CLAUDE.md` (repo root)  
3) `.github/copilot-instructions.md` (derivative guidance)

---

## Project Overview

arifOS is the world's first production-grade Constitutional AI Governance System — an **Intelligence Kernel** and **AI Control Plane** that sits between raw LLM reasoning engines and real-world actions. It enforces 13 mathematically-defined constitutional laws (Floors F1-F13) on every tool execution via the Model Context Protocol (MCP).

### Core Concept
- **What it is:** A constitutional decision kernel that governs tool execution for LLMs via MCP
- **What it isn't:** Not a model, not an agent, not a chatbot
- **What it guarantees:** A hardened L2-L5 stack with no irreversible action without explicit human approval

### The 13 Constitutional Floors (F1-F13)

| Floor | Name | Type | Threshold | Purpose |
|:---|:---|:---:|:---|:---|
| F1 | Amanah | HARD | LOCKED | Block irreversible actions |
| F2 | Truth | HARD | τ ≥ 0.99 | Factual fidelity |
| F3 | Tri-Witness | MIRROR | W³ ≥ 0.95 | Human × AI × Earth consensus |
| F4 | Clarity | HARD | ΔS ≤ 0 | Entropy reduction |
| F5 | Peace² | SOFT | P² ≥ 1.0 | Non-destructive power |
| F6 | Empathy | SOFT | κᵣ ≥ 0.70 | Protect weakest stakeholder |
| F7 | Humility | HARD | Ω₀ ∈ [0.03, 0.05] | Uncertainty band |
| F8 | Genius | MIRROR | G ≥ 0.80 | Governed intelligence |
| F9 | Anti-Hantu | SOFT | C_dark < 0.30 | No consciousness claims |
| F10 | Ontology | WALL | BOOLEAN | Category lock |
| F11 | CommandAuth | WALL | LOCKED | Verified identity |
| F12 | Injection | HARD | Risk < 0.85 | Prompt injection defense |
| F13 | Sovereign | VETO | HUMAN | Human final authority |

**Execution Order:** F12→F11 (Walls) → AGI Floors (F1,F2,F4,F7) → ASI Floors (F5,F6,F9) → Mirrors (F3,F8) → Ledger

### Trinity Architecture (ΔΩΨ)

The kernel processes decisions through three isolated engines:

```
000_INIT → AGI(Δ) Mind [111-333] → ASI(Ω) Heart [555-666] → APEX(Ψ) Soul [888] → 999_VAULT
```

- **Δ Delta (The Mind / AGI):** Truth, Logic, Causal tracing (F2, F4, F7, F8)
- **Ω Omega (The Heart / ASI):** Safety, Empathy, Anti-Deception (F1, F5, F6, F9)
- **Ψ Psi (The Soul / APEX):** Final verdict, human consensus, ledger sealing

---

## Repository Structure

### Four-Layer Architecture

```
core/              → KERNEL: Pure decision logic, zero transport dependencies
aclip_cai/         → INTELLIGENCE: Triad backends (Δ/Ω/Ψ) + 9-sense tools
aaa_mcp/           → TRANSPORT ADAPTER: FastMCP surface, protocol adapters
arifos_aaa_mcp/    → CANONICAL PyPI PACKAGE: External entry points
```

**Critical Boundaries:**
- `core/` has **zero** transport dependencies (`fastmcp`, `fastapi`, `starlette` are banned)
- `aaa_mcp/` has **zero** decision logic — protocol only
- **Never** name a local module `mcp` — this shadows the external SDK

### Key Modules

| Module | Role |
|--------|------|
| `core/governance_kernel.py` | Unified Ψ state, thermodynamics |
| `core/shared/floors.py` | `THRESHOLDS` dict — **canonical** floor definitions |
| `core/organs/_0_init.py` → `_4_vault.py` | 5 enforcement organs (stages 000-999) |
| `aaa_mcp/server.py` | 13 MCP tools with `@mcp.tool()` decorators |
| `aclip_cai/triad/` | Backend functions: anchor, reason, integrate, respond, validate, align, forge, audit, seal |
| `arifos_aaa_mcp/governance.py` | 13-LAW catalog, tool-to-dial mappings |
| `core/kernel/constitutional_decorator.py` | Kernel-level floor enforcement |

### Directory Layout

```
/srv/arifOS/
├── core/                    # Constitutional kernel (transport-agnostic)
│   ├── organs/              # 5-Organ stack (_0_init → _4_vault)
│   ├── shared/              # Floors, physics, guards, types
│   ├── kernel/              # Decorators, evaluators, constants
│   ├── physics/             # Thermodynamics module
│   └── tests/               # Kernel unit tests
├── aclip_cai/               # Intelligence layer (triad backends)
│   ├── triad/delta/         # AGI (Mind): anchor, reason, integrate
│   ├── triad/omega/         # ASI (Heart): align, respond, validate
│   ├── triad/psi/           # APEX (Soul): audit, forge, seal
│   ├── tools/               # Concrete tool implementations
│   └── embeddings/          # BGE semantic embeddings
├── aaa_mcp/                 # Transport adapter (FastMCP)
│   ├── server.py            # 13 canonical MCP tools
│   ├── external_gateways/   # Jina, Perplexity, Brave clients
│   ├── protocol/            # Response schemas, contracts
│   ├── sessions/            # Session management
│   └── vault/               # VAULT999 ledger interface
├── arifos_aaa_mcp/          # Canonical PyPI package
│   ├── __main__.py          # CLI entry point
│   ├── server.py            # Public server factory
│   └── fastmcp_ext/         # Transport extensions
├── tests/                   # Test suite
│   ├── conftest.py          # Pytest fixtures and config
│   └── *.py                 # Test modules
├── 000_THEORY/              # Canonical constitutional law documents
├── docs/                    # Documentation
├── deployment/              # Docker, Nginx, Prometheus configs
└── VAULT999/                # Immutable ledger storage
```

---

## Build, Run, and Development

### Installation

```bash
# Recommended (uv)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Alternative (pip)
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running the MCP Server

```bash
# SSE mode (default, for VPS/cloud)
python -m arifos_aaa_mcp
python -m arifos_aaa_mcp sse

# stdio mode (for Claude Desktop, Cursor)
python -m arifos_aaa_mcp stdio

# Streamable HTTP mode
python -m arifos_aaa_mcp http
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http

# Via canonical CLI entry point
arifos
arifos stdio
arifos http
```

### Docker

```bash
# Build and run
docker build -t arifos . && docker run -p 8080:8080 arifos

# Docker Compose (full stack with PostgreSQL, Redis)
docker compose -f docker-compose.quickstart.yml up -d
```

---

## Testing

### Running Tests

```bash
# Full test suite
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=core --cov=aaa_mcp --cov=aclip_cai

# Single test file
pytest tests/test_quick.py -v

# Single test function (primary pattern)
pytest tests/test_core_foundation.py::test_name -v

# Single class/method
pytest tests/test_file.py::TestClassName -v
pytest tests/test_file.py::TestClassName::test_method -v

# Marker subsets
pytest -m constitutional -v
pytest -m integration -v
pytest -m "not slow" -v

# E2E tests
pytest tests/test_e2e_all_tools.py -v
pytest tests/test_e2e_core_to_aaa_mcp.py -v
```

### Pytest Configuration

- `asyncio_mode = auto` — no `@pytest.mark.asyncio` needed on async functions
- Physics disabled by default in tests (`ARIFOS_PHYSICS_DISABLED=1`)
- Legacy spec bypass enabled (`ARIFOS_ALLOW_LEGACY_SPEC=1`)
- Archive/legacy tests excluded via `pytest_ignore_collect` in `conftest.py`

### Test Fixtures

```python
# In-memory MCP client
@pytest.fixture
async def aaa_client():
    from fastmcp import Client
    from arifos_aaa_mcp.server import create_aaa_mcp_server
    async with Client(create_aaa_mcp_server()) as client:
        yield client

# Database/Redis availability markers
postgres_required = pytest.mark.skipif(...)
redis_required = pytest.mark.skipif(...)
```

---

## Code Style Guidelines

### Formatting and Linting

```bash
# Format (100-character line limit)
black aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/ --line-length=100

# Lint
ruff check aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/
ruff check aaa_mcp/ core/ arifos_aaa_mcp/ aclip_cai/ --fix

# Type check (strict on core/)
mypy core/ --ignore-missing-imports
mypy .
```

### Style Rules

| Aspect | Rule |
|--------|------|
| Line length | 100 characters |
| Quote style | Double quotes |
| Import order | stdlib → third-party → local (Ruff/isort-compatible) |
| Naming (modules/funcs) | `snake_case` |
| Naming (classes) | `PascalCase` |
| Naming (constants) | `UPPER_SNAKE_CASE` |
| Internal helpers | Leading underscore `_helper` |

### Import Conventions

```python
# Correct namespace usage
from core.shared.physics import W_3
from aclip_cai.triad import anchor, reason
import aaa_mcp.server

# NEVER shadow external SDKs
import mcp          # External SDK — OK
import fastmcp      # External SDK — OK
# import mcp as local_module  # WRONG — never do this
```

### Critical: No stdout in Tool Code

**NEVER** use `print()` or write to `stdout` in any tool implementation — it corrupts JSON-RPC/MCP streams.

```python
# Wrong
print("debug info")  # CORRUPTS MCP STREAM

# Correct
import sys
sys.stderr.write("debug info\n")

# Or use logging
import logging
logger = logging.getLogger(__name__)
logger.error("debug info")
```

---

## MCP-Specific Conventions

### Decorator Order (CRITICAL)

```python
@mcp.tool()                    # OUTER — FastMCP registers this
@constitutional_floor("F2")   # INNER — enforcement runs at call time
async def my_tool(...):
    ...
```

**If reversed**, FastMCP registers the unwrapped function and floor enforcement never runs.

### Tool Response Contract

All tools return this envelope:

```python
{
    "verdict": "SEAL" | "PARTIAL" | "SABAR" | "VOID" | "888_HOLD",
    "stage": "000_INIT" | "111-444" | "555-666" | "777-888" | "999_VAULT",
    "session_id": str,
    "floors": {"passed": [], "failed": []},
    "truth": {"score": float, "threshold": float, "drivers": []},
    "next_actions": [],
    "payload": {...}  # Tool-specific data
}
```

### Amanah Handshake (Token Verification)

`apex_judge` signs a governance token that `seal_vault` must verify:

```python
# In apex_judge
governance_token = _build_governance_token(session_id, verdict)

# In seal_vault
token_valid, verified_verdict = _verify_governance_token(session_id, governance_token)
if not token_valid:
    return {"verdict": "VOID", ...}  # Tampered token
```

---

## Adding a New MCP Tool

1. Add `@mcp.tool()` in `aaa_mcp/server.py`
2. Create backend in `aclip_cai/triad/` (delta/, omega/, or psi/)
3. Wire kernel logic via `core/` imports
4. Register floor mapping in `core/kernel/constitutional_decorator.py` `FLOOR_ENFORCEMENT` dict
5. Mirror in `arifos_aaa_mcp/server.py` and add to `AAA_TOOLS`
6. Add tests in `tests/`

---

## 888_HOLD Triggers

Require explicit human confirmation before:

- Database migrations
- Production deployments
- Credential/secret handling
- Mass file operations (>10 files)
- Git history modification (rebase, force push)
- Conflicting evidence across source tiers

**Protocol:** List consequences → state irreversibles → ask "yes, proceed" → wait → execute with logging.

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `ARIFOS_GOVERNANCE_SECRET` | Recommended | auto-generated | Signs `governance_token` (HMAC-SHA256) |
| `DATABASE_URL` | Optional | SQLite fallback | PostgreSQL for VAULT999 ledger |
| `JINA_API_KEY` | Optional | — | Clean Markdown extraction |
| `PERPLEXITY_API_KEY` | Optional | — | Web search fallback |
| `BRAVE_API_KEY` | Optional | — | Web search fallback |
| `ARIFOS_ML_FLOORS` | Optional | `0` | Enable SBERT semantic scoring for F5/F6/F9 |
| `ARIFOS_PHYSICS_DISABLED` | Optional | `0` | Disable thermodynamic calculations |
| `AAA_MCP_OUTPUT_MODE` | Optional | `user` | `user` or `debug` output verbosity |

---

## Key Gotchas

1. **Stage 222 THINK is internal-only**: Runs inside `reason_mind` — no external `@mcp.tool()`
2. **`seal_vault` is token-locked**: Requires `governance_token` from `apex_judge`
3. **F4 (Clarity) is a Hard floor**: `ΔS > 0` → VOID (not PARTIAL)
4. **Two floor decorator layers exist**: `core/kernel/constitutional_decorator.py` (kernel) AND `aaa_mcp/core/constitutional_decorator.py` (transport)
5. **`codebase/` is removed**: Deleted in v2026.2.15 — all code is in `core/`, `aclip_cai/`, `aaa_mcp/`
6. **`tests/archive/`**: ~100 legacy files with broken imports — reference only
7. **APEX Solver**: Uses geometric mean (not arithmetic) for 9-paradox synthesis — target GM ≥ 0.85

---

## CI/CD and Deployment

### GitHub Actions Workflows

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Build, test, lint, type-check, coverage upload |
| `deploy-vps.yml` | Production deployment to VPS |
| `docker-publish.yml` | Build and push Docker images |
| `live_tests.yml` | Continuous live endpoint testing |
| `mcp-conformance.yml` | MCP protocol conformance tests |
| `secrets-scan.yml` | Security scanning |

### Pre-commit Hooks

```bash
# Install
pip install pre-commit
pre-commit install

# Run all hooks
pre-commit run --all-files
```

Hooks include: Black, Ruff, MyPy, Bandit, detect-secrets, and custom constitutional checks.

---

## Security Considerations

- **F12 Injection Defense**: All inputs scanned via `InjectionGuard`
- **F11 Command Auth**: Cryptographic identity verification
- **F1 Amanah**: Irreversible operations require explicit `confirm_dangerous=True`
- **Secret Management**: Use vault in production (HashiCorp Vault, AWS Secrets Manager)
- **Rotation**: Secrets must rotate minimum every 90 days
- **Least Privilege**: DB user should not be superuser

---

## References

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview and quick start |
| `CLAUDE.md` | Claude Code specific guidance |
| `QUICKSTART.md` | 5-minute setup guide |
| `000_THEORY/000_LAW.md` | Canonical constitutional law (F1-F13) |
| `docs/60_REFERENCE/ARCHITECTURE.md` | Trinity Logic, 7-Organ Stack, EMD Physics |
| `docs/60_REFERENCE/DEPLOYMENT.md` | VPS, Docker, scaling |
| `docs/60_REFERENCE/TOOLS_CANONICAL_13.md` | 14 canonical MCP tools |
| `pyproject.toml` | Package metadata, dependencies, tool config |

---

*Last updated: 2026-03-06*
