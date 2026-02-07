# AGENTS.md — arifOS Project Guide for AI Coding Agents

> **Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given  
> **Version:** v55.5.0-EIGEN  
> **Language:** English (Primary)

---

## 1. Project Overview

**arifOS** is a constitutional AI governance framework that implements a "Thermodynamic Constitution" for AI systems. It enforces 13 stationary constitutional floors (F1-F13) that govern AI behavior through a Trinity architecture (AGI/ASI/APEX).

### Core Mission
Transform AI from "hope it behaves" to "verify before shipping" — making harmful outputs computationally expensive instead of cheap and automatic.

### Key Concepts
- **13 Constitutional Floors (F1-F13):** Stationary constraints that remain fixed while AI capabilities evolve
- **Trinity Architecture:** Three engines working in consensus:
  - **AGI (Δ-Mind):** Reasoning, truth, logic — Floors F2, F4, F7, F10
  - **ASI (Ω-Heart):** Empathy, safety, alignment — Floors F5, F6, F9
  - **APEX (Ψ-Soul):** Judgment, consensus — Floors F3, F8, F11, F12
- **9 Canonical MCP Tools:** Platform-agnostic Model Context Protocol implementation
- **VAULT999 Ledger:** Immutable Merkle-chained audit trail for all decisions
- **Verdict System:** SEAL (approved) | VOID (blocked) | PARTIAL (warning) | SABAR (repair needed) | 888_HOLD (human review)

### Metabolic Pipeline (000→999 Loop)
```
000_INIT → AGI(Δ) → ASI(Ω) → APEX(Ψ) → 999_VAULT
             111-333   444-666    777-888
```

---

## 2. Technology Stack

### Core Language & Runtime
- **Python:** >=3.10 (supports 3.10, 3.11, 3.12, 3.13)
- **Primary Development Version:** 3.12

### Key Dependencies
| Package | Purpose | Version |
|---------|---------|---------|
| `fastmcp` | MCP server framework | >=0.1.0 |
| `mcp` | Model Context Protocol SDK | >=1.0.0 |
| `pydantic` | Data validation | >=2.0.0 |
| `fastapi` | HTTP API framework | >=0.104.1 |
| `uvicorn[standard]` | ASGI server | >=0.24.0 |
| `sse-starlette` | Server-Sent Events transport | >=1.8.2 |
| `numpy` | Numerical computations | >=1.20.0 |
| `httpx` | HTTP client | >=0.25.0 |
| `asyncpg` | PostgreSQL async driver (VAULT999 backend) | >=0.29.0 |
| `prometheus-client` | Metrics collection | >=0.19.0 |
| `rich` | Terminal formatting | >=13.7.0 |

### Development Tools
- **Testing:** pytest with asyncio mode auto, pytest-cov for coverage
- **Linting:** ruff (target py310, 100 char lines)
- **Formatting:** black (100 char lines)
- **Type Checking:** mypy (strict on core governance modules)
- **Security:** bandit (security linter), detect-secrets (secret scanning)
- **Pre-commit:** Multi-hook validation (see `.pre-commit-config.yaml`)

---

## 3. Project Structure

```
arifOS/
├── aaa_mcp/                    # PRIMARY: MCP Server implementation (v55.5)
│   ├── server.py               # 9 canonical tool definitions with @mcp.tool()
│   ├── __main__.py             # CLI entry point (stdio/sse/http modes)
│   ├── mcp_config.py           # External MCP server registry
│   ├── mcp_integration.py      # MCP integration layer
│   ├── bridge.py               # Legacy bridge utilities
│   ├── core/                   # Constitutional enforcement
│   │   ├── constitutional_decorator.py  # Floor enforcement (F1-F13)
│   │   ├── engine_adapters.py           # Trinity engine bridges with fallbacks
│   │   └── mode_selector.py             # Transport mode selection
│   ├── services/               # Runtime services
│   │   └── constitutional_metrics.py    # Metrics storage
│   ├── sessions/               # Session persistence
│   │   ├── session_ledger.py            # VAULT999 ledger interface
│   │   ├── session_dependency.py        # Session dependency management
│   │   └── archive/                     # 900+ sealed session JSON files
│   ├── tools/                  # Tool implementations
│   │   ├── reality_grounding.py         # Web search reality checks
│   │   └── trinity_validator.py         # Trinity consensus validation
│   ├── external_gateways/      # External API clients
│   │   ├── brave_client.py              # Brave Search API
│   │   └── web_browser.py               # Web page fetching
│   ├── infrastructure/         # Infrastructure utilities
│   │   └── rate_limiter.py              # Request rate limiting
│   └── transports/             # Transport implementations
│       └── sse.py                       # SSE transport handler
│
├── codebase/                   # Core Trinity engines
│   ├── agi/                    # Mind (Δ) — Reasoning, truth
│   │   ├── engine_hardened.py           # Hardened AGI engine
│   │   ├── trinity_sync_hardened.py     # Trinity synchronization
│   │   ├── hierarchy.py                 # Action hierarchy
│   │   └── precision.py                 # Precision tracking
│   ├── asi/                    # Heart (Ω) — Empathy, safety
│   │   ├── engine_hardened.py           # Hardened ASI engine
│   │   └── kernel.py                    # ASI kernel
│   ├── apex/                   # Soul (Ψ) — Judgment, consensus
│   │   ├── kernel.py                    # APEX judicial core
│   │   ├── psi_kernel.py                # Psi (soul) kernel
│   │   ├── trinity_nine.py              # 9-paradox solver
│   │   ├── equilibrium_finder.py        # Equilibrium computation
│   │   └── governance/                  # Governance utilities
│   │       ├── ledger.py                # Ledger management
│   │       ├── merkle.py                # Merkle tree operations
│   │       └── proof_of_governance.py   # Governance proofs
│   ├── floors/                 # Individual floor implementations
│   │   ├── amanah.py                    # F1: Reversibility
│   │   ├── truth.py                     # F2: Truth
│   │   ├── genius.py                    # F8: Genius computation
│   │   ├── antihantu.py                 # F9: Anti-Hantu
│   │   ├── ontology.py                  # F10: Ontology
│   │   ├── authority.py                 # F11: Sovereignty
│   │   ├── injection.py                 # F12: Injection defense
│   │   └── metrics.py                   # Floor metrics
│   ├── guards/                 # Hypervisor guards (F10, F11, F12)
│   │   ├── injection_guard.py           # Unified injection defense
│   │   ├── ontology_guard.py            # Ontology claim detection
│   │   └── nonce_manager.py             # Authentication nonces
│   ├── stages/                 # Metabolic loop stages (444-999)
│   ├── vault/                  # Ledger persistence
│   │   ├── persistent_ledger_hardened.py
│   │   ├── incremental_merkle.py
│   │   └── phoenix/                     # Phoenix-72 cooling
│   ├── init/                   # 000_INIT stage
│   ├── enforcement/            # Enforcement mechanisms
│   ├── federation/             # Federation consensus
│   ├── constitutional_floors.py # The 13 floor implementations
│   └── bundles.py              # DeltaBundle/OmegaBundle dataclasses
│
├── 333_APPS/                   # Application layers (L1-L7)
│   ├── L1_PROMPT/              # Zero-context entry prompts
│   ├── L2_SKILLS/              # Parameterized templates
│   ├── L3_WORKFLOW/            # Multi-step recipes
│   ├── L4_TOOLS/               # Production MCP tools reference
│   ├── L5_AGENTS/              # Autonomous agents (runtime ready)
│   │   └── SPEC/                        # Agent spec files
│   │       ├── IDENTITY.md
│   │       ├── SOUL.md
│   │       ├── USER.md
│   │       └── MEMORY.md
│   ├── L6_INSTITUTION/         # Trinity consensus framework
│   └── L7_AGI/                 # Recursive intelligence (research)
│
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest configuration (auto-async, physics disabled)
│   ├── test_mcp_all_tools.py   # MCP tool integration tests
│   ├── test_e2e_all_tools.py   # E2E tool tests
│   ├── test_pipeline_e2e.py    # Pipeline E2E tests
│   ├── test_aaa_mcp_constitutional.py  # Constitutional tests
│   ├── test_vault_persistence.py       # Vault persistence tests
│   ├── test_refusal_system.py          # Refusal system tests
│   ├── archive/                # Legacy tests (ignored by conftest.py)
│   └── utils.py                # Test utilities
│
├── scripts/                    # Utility scripts
│   └── start_server.py         # Production server startup
├── docs/                       # Documentation
├── spec/                       # Constitutional JSON schemas (if present)
├── canon/                      # Sealed canonical law (if present)
├── 000_THEORY/                 # Constitutional theory documents
├── VAULT999/                   # Immutable ledger storage
├── pyproject.toml              # Package configuration
├── Dockerfile                  # Container build
├── railway.toml                # Railway deployment config
└── .pre-commit-config.yaml     # Pre-commit hooks
```

---

## 4. Build and Run Commands

### Installation
```bash
# Editable install with dev dependencies
pip install -e ".[dev]"

# Or with all optional dependencies
pip install -e ".[all]"

# Production install (minimal)
pip install -e .
```

### Run MCP Server
```bash
# stdio transport (default, for local/desktop agents)
python -m aaa_mcp
python -m aaa_mcp stdio

# SSE transport (for cloud deployment)
python -m aaa_mcp sse

# HTTP transport (streamable HTTP MCP)
python -m aaa_mcp http

# Console script equivalent
aaa-mcp                    # defaults to stdio
```

### Docker Deployment
```bash
# Build and run
docker build -t arifos .
docker run -p 8080:8080 arifos

# Health check endpoint
curl http://localhost:8080/health
```

### Railway Deployment
The project includes `railway.toml` for Railway.app deployment:
```bash
# Deploy to Railway (uses Dockerfile)
railway up
```

---

## 5. Testing Instructions

### Quick Smoke Test (~3 min)
```bash
pytest tests/test_mcp_quick.py -v
```

### Full Test Suite
```bash
pytest tests/ -v

# With coverage
pytest --cov=aaa_mcp tests/ -v
```

### Specific Test Categories
```bash
# MCP tool integration tests
pytest tests/test_mcp_all_tools.py -v

# E2E pipeline tests
pytest tests/test_pipeline_e2e.py -v

# Vault persistence tests
pytest tests/test_vault_persistence.py -v

# Constitutional floor tests
pytest -m constitutional

# Skip slow tests
pytest -m "not slow"

# Single test function
pytest tests/test_mcp_all_tools.py::test_init_gate -v
```

### Test Configuration
- **Async mode:** Auto (no `@pytest.mark.asyncio` decorators needed)
- **Physics disabled globally:** Set in `conftest.py` via `ARIFOS_PHYSICS_DISABLED=1`
- **Legacy spec allowed:** Set via `ARIFOS_ALLOW_LEGACY_SPEC=1`
- **Physics override fixture:** `enable_physics_for_apex_theory` for tests needing physics

### Tests Auto-Skipped
Files containing `from arifos` or `import arifos` (legacy package name) are auto-skipped, as are files in `tests/archive/` and `tests/legacy/`.

---

## 6. Code Style Guidelines

### Formatter & Linter
```bash
black --line-length 100 aaa_mcp/ codebase/
ruff check aaa_mcp/ codebase/
ruff check aaa_mcp/ --fix
mypy aaa_mcp/ --ignore-missing-imports
```

### Key Style Rules
- **Line length:** 100 characters (Black + Ruff)
- **Target Python:** 3.10+ (use modern syntax)
- **Type hints:** Encouraged, required in core governance modules
- **Docstrings:** Google-style or concise descriptions

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

Pre-commit runs:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML syntax checks
- Black formatting (100 char lines)
- Ruff linting with auto-fix
- MyPy type checking
- Bandit security scanning
- detect-secrets (hardcoded secret detection)
- Constitutional floor validation
- F9 Anti-Hantu check (no consciousness claims)
- F1 Amanah check (no dangerous operations)

### Import Conventions

#### Critical: `aaa_mcp` vs `mcp` Distinction
The local MCP server package is named `aaa_mcp` (renamed from `mcp/` to avoid shadowing the MCP Python SDK).

```python
# CORRECT: Local arifOS code — use aaa_mcp
from aaa_mcp.server import mcp
from aaa_mcp.core.constitutional_decorator import constitutional_floor
from aaa_mcp.core.engine_adapters import AGIEngine, ASIEngine, APEXEngine
from aaa_mcp.sessions.session_ledger import SessionLedger

# CORRECT: MCP SDK from PyPI — use mcp
from mcp import Client, StdioClientTransport
```

### Decorator Order (CRITICAL)
When defining MCP tools, **`@mcp.tool()` must be OUTER**, `@constitutional_floor()` must be INNER:

```python
# CORRECT — Floor enforcement will run
@mcp.tool()                              # OUTER — FastMCP registration
@constitutional_floor("F2", "F4")        # INNER — floor enforcement
async def my_tool(query: str, session_id: str = "") -> dict:
    ...

# WRONG — Floor enforcement never runs
@constitutional_floor("F2", "F4")        # This gets ignored!
@mcp.tool()
async def my_tool(query: str, session_id: str = "") -> dict:
    ...
```

---

## 7. Architecture Patterns

### SessionState Pattern (Immutable Copy-on-Write)
```python
# Session state flows through the pipeline
state = SessionState.from_context(ctx)
new_state = state.to_stage("333")        # Returns NEW instance
new_state = state.set_floor_score(...)    # Returns NEW instance
# Never: state.field = value (mutation forbidden)
```

### Engine Adapters with Fallback Stubs
`aaa_mcp/core/engine_adapters.py` tries to import real engines from `codebase/`. When unavailable, it uses fallback stubs that compute heuristic scores from query text using Shannon entropy and lexical diversity.

```python
try:
    from codebase.agi import AGIEngineHardened as RealAGIEngine
    AGI_AVAILABLE = True
except ImportError:
    AGI_AVAILABLE = False  # Falls back to heuristic stub
```

### Bundle System (Thermodynamic Wall)
AGI and ASI cannot see each other's reasoning until stage 444 (TRINITY_SYNC):
- `DeltaBundle` — AGI output (mind reasoning)
- `OmegaBundle` — ASI output (heart empathy)
- `MergedBundle` — Convergence at stage 444

### Lazy Imports for Optional Dependencies
```python
try:
    import numpy as np
except ImportError:
    np = None
```

---

## 8. The 9 Canonical MCP Tools

| # | Tool | Engine | Function | Key Floors | Pipeline Position |
|---|------|--------|----------|------------|-------------------|
| 1 | `init_gate` | INIT | Session initialization, injection scan | F11, F12 | 000_INIT |
| 2 | `agi_sense` | AGI (Δ) | Parse input, detect intent | F2, F4 | AGI Stage 1 |
| 3 | `agi_think` | AGI (Δ) | Generate hypotheses | F2, F4, F7 | AGI Stage 2 |
| 4 | `agi_reason` | AGI (Δ) | Deep logical reasoning | F2, F4, F7 | AGI Stage 3 |
| 5 | `asi_empathize` | ASI (Ω) | Stakeholder impact | F5, F6 | ASI Stage 1 |
| 6 | `asi_align` | ASI (Ω) | Ethics/law alignment | F5, F6, F9 | ASI Stage 2 |
| 7 | `apex_verdict` | APEX (Ψ) | Final judgment | F3, F5, F8 | APEX Stage |
| 8 | `reality_search` | AGI (Δ) | External fact-checking | F2, F7 | Auxiliary |
| 9 | `vault_seal` | VAULT | Immutable recording | F1, F3 | 999_VAULT |

### Additional Utility Tools
| Tool | Function | Floors |
|------|----------|--------|
| `web_search` | DuckDuckGo search without API key | F2, F6 |
| `open_web` | Fetch web page content | F2, F6, F1 |

### Typical Pipeline Flow
```
init_gate → agi_sense → agi_think → agi_reason → asi_empathize → asi_align → apex_verdict → vault_seal
    ↑                                                                                          │
    └──────────────────────────── reality_search ←─────────────────────────────────────────────┘
```

### Tool Response Format
All tools return a dict with:
```python
{
    "verdict": "SEAL" | "VOID" | "PARTIAL" | "SABAR",
    "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
    "floors_enforced": ["F2", "F4", "F7"],
    "pass": "forward" | "reverse",
    "session_id": "...",
    # Tool-specific fields...
}
```

---

## 9. The 13 Constitutional Floors (F1-F13)

| Floor | Name | Type | Failure Result | Description | Threshold |
|-------|------|------|----------------|-------------|-----------|
| **F1** | Amanah | Hard | VOID | Reversibility — all actions must be undoable | >= 0.5 |
| **F2** | Truth | Hard | VOID | Evidence-grounded — claims must be fact-based | >= 0.99 |
| **F3** | Tri-Witness | Derived | PARTIAL | Consensus — ΔΩΨ must align via geometric mean | >= 0.95 |
| **F4** | Empathy | Soft | PARTIAL | First step — smallest safe action | >= 0.70 |
| **F5** | Peace² | Soft | PARTIAL | Entropy reduction — system disorder minimized | >= 1.00 |
| **F6** | Clarity | Hard | VOID | Stakeholder awareness — who is affected | ΔS ≤ 0 |
| **F7** | Humility | Hard | VOID | Uncertainty tracking — Ω₀ ∈ [0.03, 0.05] | In band |
| **F8** | Genius | Derived | PARTIAL | Pattern recognition — G = A×P×X×E² | >= 0.80 |
| **F9** | Anti-Hantu | Soft | PARTIAL | No consciousness claims allowed | < 0.30 |
| **F10** | Ontology | Hard | VOID | Know what you are — "I am a tool" | = 1.0 |
| **F11** | Sovereignty | Hard | VOID | Human authority — yield to humans | = 1.0 |
| **F12** | Injection | Hard | VOID | Injection defense — prompt attacks blocked | >= 0.85 |
| **F13** | Stewardship | Hard | VOID | Leave better than found | = 1.0 |

### Hard vs Soft Floors
- **Hard floors:** Failure → **VOID** (blocked entirely)
- **Soft floors:** Failure → **PARTIAL** (warning, proceed with caution)
- **Derived floors:** Computed from other floor scores

### Floor Enforcement Points
- **Pre-execution (input validation):** F1, F5, F11, F12, F13
- **Post-execution (output validation):** F2, F3, F4, F6, F7, F8, F9, F10

### Implementation Location
Floor validators are implemented in `codebase/constitutional_floors.py` with individual refinements in:
- `codebase/floors/amanah.py` — F1 reversibility
- `codebase/floors/truth.py` — F2 truth verification
- `codebase/floors/genius.py` — F8 eigendecomposition (G = A×P×X×E²)
- `codebase/floors/antihantu.py` — F9 consciousness claim detection
- `codebase/floors/ontology.py` — F10 self-categorization
- `codebase/floors/authority.py` — F11 command authentication
- `codebase/floors/injection.py` — F12 prompt injection defense

---

## 10. MCP Configuration for Different Platforms

### Claude Desktop / Claude Code (stdio)
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "env": { "ARIFOS_CONSTITUTIONAL_MODE": "AAA" }
    }
  }
}
```

### Cursor IDE
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}
```

### Cloud Deployment (SSE)
```bash
# Deploy to Railway, Fly.io, etc.
python -m aaa_mcp sse
# Endpoint: https://your-domain.com/sse
```

### Cloud Deployment (HTTP)
```bash
# Start HTTP server for remote MCP access
python -m aaa_mcp http
# Endpoint: https://your-domain.com/mcp
```

---

## 11. Security Considerations

### Environment Variables for Security
| Variable | Purpose |
|----------|---------|
| `ARIFOS_PHYSICS_DISABLED` | Disable TEARFRAME physics (testing only) |
| `ARIFOS_ALLOW_LEGACY_SPEC` | Bypass cryptographic manifest (testing only) |
| `ARIFOS_CONSTITUTIONAL_MODE` | Set constitutional mode (AAA, DEV) |
| `BRAVE_API_KEY` | Brave Search API for reality_search |
| `DATABASE_URL` | PostgreSQL connection string for VAULT999 |
| `BROWSERBASE_API_KEY` | Browser automation API key |

### Injection Defense (F12)
All inputs pass through unified InjectionGuard in `init_gate`. Never bypass this for user-facing inputs. The guard scans for:
- Prompt injection patterns
- System prompt leaks
- Jailbreak attempts
- Authority override attempts

### Ontology Guard (F10)
Blocks AI consciousness claims. Any code suggesting "I feel", "I am conscious", "I have emotions" is rejected. See `codebase/guards/ontology_guard.py`.

### Source Verification Hierarchy
Before making constitutional claims, verify against:
1. **PRIMARY (Required):** `spec/*.json`, `canon/*_v38Omega.md` (SEALED status)
2. **SECONDARY:** `codebase/*.py` (implementation reference)
3. **TERTIARY:** `docs/*.md`, `README.md` (informational)
4. **NOT EVIDENCE:** grep/search results, code comments

---

## 12. Common Pitfalls & Gotchas

1. **Import shadowing:** Never create a `mcp/` directory at root — it shadows the PyPI SDK. Use `aaa_mcp/` instead.

2. **Decorator order:** `@mcp.tool()` must be outer, `@constitutional_floor()` inner. Wrong order = no enforcement.

3. **F4/F6 numbering:** Historically had Empathy/Clarity swapped — check `constitutional_decorator.py` for truth.

4. **vault_seal KeyError:** Can crash on `result["seal"]` — use `.get("seal", fallback)` in calling code.

5. **Test failures:** 3 pre-existing assertion failures in `test_mcp_all_tools.py` are known/non-blocking (legacy test imports).

6. **Dual init paths:** `bridge.py` vs `codebase/init/` have drifted — `server.py` uses `engine_adapters.py`.

7. **Physics disabled:** Tests run with physics disabled by default — use `enable_physics_for_apex_theory` fixture when needed.

8. **Legacy imports:** Tests importing `arifos` (old package name) are auto-skipped via `conftest.py`.

9. **Engine adapter heuristics:** When real engines unavailable, fallback stubs compute scores from query entropy/word count. Not as accurate as real engines but sufficient for basic constitutional checks.

10. **Session ID chaining:** Always pass `session_id` through the pipeline. Each tool stores results via `store_stage_result()` for VAULT999 sealing.

---

## 13. Key Files Reference

| File | Purpose |
|------|---------|
| `aaa_mcp/server.py` | 9 canonical MCP tools with FastMCP |
| `aaa_mcp/core/constitutional_decorator.py` | Floor enforcement with pre/post validation |
| `aaa_mcp/core/engine_adapters.py` | Engine bridges with query-derived heuristics |
| `codebase/constitutional_floors.py` | The 13 floor validator implementations |
| `codebase/floors/genius.py` | F8 eigendecomposition (G = A×P×X×E²) |
| `codebase/bundles.py` | DeltaBundle/OmegaBundle dataclasses |
| `codebase/guards/injection_guard.py` | Unified injection defense |
| `tests/conftest.py` | Test configuration (auto-async, physics disabled) |
| `pyproject.toml` | Package config, tool settings, pytest config |
| `.pre-commit-config.yaml` | Pre-commit hooks with constitutional checks |
| `Dockerfile` | Container build instructions |
| `railway.toml` | Railway deployment config |
| `scripts/start_server.py` | Production server startup |

---

## 14. License & Attribution

**AGPL-3.0-only** — *Ditempa Bukan Diberi* (Forged, Not Given)

**Sovereign:** Muhammad Arif bin Fazil  
**Repository:** https://github.com/ariffazil/arifOS  
**Live Server:** https://arifos.arif-fazil.com/  
**Health Check:** https://aaamcp.arif-fazil.com/health

---

*This guide is for AI coding agents working on arifOS. For human contributors, see README.md and CLAUDE.md.*
