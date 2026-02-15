# arifOS Agent Guide (v64.2-GAGI)

**Canon:** `C:/Users/User/arifOS/AGENTS.md`  
**Version:** v64.2-GAGI  
**Motto:** "DITEMPA BUKAN DIBERI — Forged, Not Given"  
**Code Version:** 64.2.0  
**Reality Index:** 0.94 (94% of documented features operational)

---

## 🏗️ Project Overview

**arifOS** is a Constitutional AI Governance System built on the **Model Context Protocol (MCP)**. It embodies a biological intelligence architecture that sits between AI models and users, enforcing 13 constitutional floors through a 9-tool governance pipeline.

### Architecture Components

| Component | Role | Analogy | Key Responsibilities |
|:---|:---|:---|:---|
| **aaa-mcp** | **The Brain** | ΔΩΨ | Logic (AGI), Ethics (ASI), Judgment (APEX). Enforces 13 Constitutional Floors. |
| **aclip-cai** | **The Senses** | C0-C9 | Observability, Metrics, Logs, Security. Provides "grounding" (F2 Truth). |
| **core/** | **The Kernel** | DNA | Pure decision logic (stateless, pure functions). Shared by Brain and Senses. |
| **scripts/** | **The Body** | Railway | Deployment entry points tailored for hosting environments. |

### Architecture: v64.2-GAGI (Get A Grip Intelligence)
- **Unified Deployment:** `aaa-mcp` and `aclip-cai` can run as a single organism via `arifos-router`
- **5-Core Kernel:** 000_INIT, AGI, ASI, APEX, VAULT (located in `core/organs/`)
- **9 A-CLIP Tools:** anchor (000) → reason (222) → integrate (333) → respond (444) → validate (555) → align (666) → forge (777) → audit (888) → seal (999)
- **10 Sensory Tactics:** C0 (Health) to C9 (Finance) in `aclip_cai/`
- **Transport:** SSE (Server-Sent Events) for Railway/Cloud; Stdio for Local Agents (Kimi)

### 333_APPS: 7-Layer Application Stack
```
L7 AGI        — Recursive self-healing (Research)
L6 Institution — Trinity consensus (Stubs)
L5 Agents     — Multi-agent federation (Pilot)
L4 Tools      — MCP ecosystem (Production)
L3 Workflow   — 000→999 sequences (Production)
L2 Skills     — 9 canonical actions (Production)
L1 Prompts    — Zero-context entry (Production)
```

---

## 🛠️ Technology Stack

| Layer | Specific Technologies |
|:---|:---|
| **Language** | Python 3.12+ (Async-first) |
| **Protocol** | Model Context Protocol (MCP) 2024-11-05 |
| **Framework** | `fastmcp>=2.14.0`, `starlette`, `fastapi`, `uvicorn` |
| **Data** | `pydantic` v2, `dataclasses` |
| **Storage** | PostgreSQL (VAULT999), Redis (MindVault), ChromaDB (Memory) |
| **ML/NLP** | `sentence-transformers>=2.2.0`, `scikit-learn>=1.3.0`, `numpy>=1.20.0` |
| **Tooling** | `uv` (package manager), `ruff`, `black`, `pytest`, `mypy` |

---

## 🚀 Build, Lint, and Test Commands

### Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Or use uv (recommended)
pip install uv
uv pip install -e ".[dev]"
```

### Formatting, Linting, and Type Checking
```bash
# Format code with Black (line length: 100)
black . --line-length 100

# Lint code with Ruff
ruff check . --line-length 100

# Type check with MyPy
mypy .
```

### Testing
All agents MUST write tests for new functionality.

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Run a specific test class
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName -v

# Run a specific test method
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName::test_method_name -v

# Run tests skipping physics (faster)
ARIFOS_PHYSICS_DISABLED=1 pytest tests/

# Run constitutional tests only
pytest -m constitutional

# Run tests requiring PostgreSQL/Redis (services must be running)
pytest -m "postgres_required or redis_required"
```

### Local Development
```bash
# Run AAA-MCP (The Brain) via stdio (default for local agents)
python -m aaa_mcp
# or
python -m aaa_mcp stdio

# Run AAA-MCP (The Brain) via sse
python -m aaa_mcp sse

# Run AAA-MCP (The Brain) via http
python -m aaa_mcp http

# Run ACLIP-CAI (The Senses) via CLI
aclip-cai health
aclip-cai fs --path /root/arifOS --depth 2

# Run ACLIP-CAI MCP server
aclip-server --sse --port 50080

# Run unified router (AAA + ACLIP)
arifos-router --sse --port 8080
```

---

## 📁 Project Structure

```
arifOS/
├── core/                      # KERNEL — All decision logic (ZERO transport deps)
│   ├── governance_kernel.py   # Unified Ψ state
│   ├── judgment.py            # Canonical verdict interface
│   ├── uncertainty_engine.py  # Ω₀ calculation (harmonic/geometric)
│   ├── pipeline.py            # Constitutional pipeline
│   ├── telemetry.py           # 30-day locked adaptation
│   ├── organs/                # 5-Core organs
│   │   ├── _0_init.py         # 000_INIT — Constitutional airlock
│   │   ├── _1_agi.py          # AGI — Mind (Δ)
│   │   ├── _2_asi.py          # ASI — Heart (Ω)
│   │   ├── _3_apex.py         # APEX — Soul (Ψ)
│   │   └── _4_vault.py        # VAULT — Seal (🔒)
│   └── shared/                # Shared utilities
│       ├── guards/            # InjectionGuard, OntologyGuard
│       ├── floors.py          # Constitutional floors
│       └── types.py           # Canonical types
│
├── aaa_mcp/                   # ADAPTER — Transport only (NO decision logic)
│   ├── server.py              # MCP server (calls kernel)
│   ├── __main__.py            # CLI entry point (stdio/sse/http)
│   ├── rest.py                # REST API bridge
│   ├── tools/                 # Tool wrappers
│   ├── capabilities/          # Web search, code analysis
│   ├── core/                  # Constitutional decorator
│   ├── guards/                # Injection/ontology guards
│   ├── protocol/              # Tool specs and schemas
│   ├── sessions/              # Session management
│   └── vault/                 # Audit logging
│
├── aclip_cai/                 # 9-Sense Nervous System
│   ├── server.py              # MCP server for sensory tools
│   ├── cli.py                 # CLI interface
│   ├── mcp_bridge.py          # MCP bridge
│   └── tools/                 # C0-C9 sensory tools
│       ├── system_monitor.py  # C0: System health
│       ├── fs_inspector.py    # C2: Filesystem inspection
│       ├── log_reader.py      # C3: Log tail
│       ├── net_monitor.py     # C4: Network status
│       ├── config_reader.py   # C5: Config flags
│       ├── chroma_query.py    # C6: Vector memory search
│       ├── thermo_estimator.py# C8: Thermodynamic cost
│       ├── safety_guard.py    # C7: Forge guard
│       └── financial_monitor.py # C9: Financial cost
│
├── 333_APPS/                  # APPLICATION LAYERS L1-L7
│   ├── L1_PROMPT/             # Zero-context system entry
│   ├── L2_SKILLS/             # 9 canonical actions
│   ├── L3_WORKFLOW/           # 000→999 sequences
│   ├── L4_TOOLS/              # MCP tool specs
│   ├── L5_AGENTS/             # Multi-agent federation (pilot)
│   ├── L6_INSTITUTION/        # Trinity consensus (stubs)
│   └── L7_AGI/                # Recursive research
│
├── tests/                     # Test suite (140+ tests)
│   ├── conftest.py            # Pytest configuration & fixtures
│   ├── constitutional/        # F1-F13 floor tests
│   ├── core/                  # Kernel tests
│   ├── aclip_cai/             # Sensory layer tests
│   └── integration/           # E2E integration tests
│
├── scripts/                   # Deployment scripts
├── VAULT999/                  # Immutable ledger storage
├── Dockerfile                 # Production container
├── railway.toml              # Railway configuration
└── pyproject.toml            # Package configuration
```

**Critical Architectural Rule:** `core/` has zero dependencies on MCP, HTTP, or any transport. `aaa_mcp/` has zero decision logic. See `ARCHITECTURAL_BOUNDARY.md`.

---

## 📝 Code Style & Conventions

### Import Order
1. Kernel modules first: `from core.judgment import ...`
2. Standard library imports
3. Third-party imports

### Formatting & Typing
- **Line Length:** 100 characters (Black + Ruff)
- **Typing:** Use `pydantic` v2 models for all I/O. All functions must have type hints.
- **Async:** All I/O-bound tools and functions MUST be `async`.

### Naming Conventions
| Type | Convention | Example |
|:---|:---|:---|
| Modules | `lowercase_with_underscores` | `governance_kernel.py` |
| Classes | `PascalCase` | `GovernanceKernel` |
| Functions/Variables | `snake_case` | `compute_uncertainty` |
| Constants | `UPPERCASE_WITH_UNDERSCORES` | `UNCERTAINTY_THRESHOLD` |

### Error Handling
- Never swallow errors
- For MCP tools, return a `{"verdict": "VOID", "error": "..."}` payload
- Raise exceptions for internal logic errors only

### Constitutional Floors
Decorate tools with enforced floors using `@constitutional_floor("F2", "F4")`. The `@mcp.tool()` decorator should be the outer decorator.

```python
@mcp.tool()
@constitutional_floor("F2", "F4", "F7")
async def reason(query: str) -> CognitionResult:
    """Tool description."""
    # Implementation
```

---

## 🧪 Testing Strategy

### Test Organization
- `tests/constitutional/` — F1-F13 floor compliance tests
- `tests/core/` — Kernel logic tests
- `tests/aclip_cai/` — Sensory layer tests
- `tests/integration/` — End-to-end tests
- `tests/archive/` — Legacy tests (ignored by pytest)

### Key Fixtures (from `conftest.py`)
- `disable_physics_globally` — Disables TEARFRAME Physics for performance
- `allow_legacy_spec_for_tests` — Allows legacy spec loading in tests
- `postgres_required` — Skips tests if PostgreSQL unavailable
- `redis_required` — Skips tests if Redis unavailable

### Environment Variables for Testing
```bash
ARIFOS_PHYSICS_DISABLED=1      # Skip physics computation
ARIFOS_ALLOW_LEGACY_SPEC=1     # Allow legacy spec bypass
AAA_MCP_OUTPUT_MODE=debug      # Enable debug output
```

### Running Tests
```bash
# Fast test run (no physics)
ARIFOS_PHYSICS_DISABLED=1 pytest tests/ -v

# Full test run (with physics)
pytest tests/ -v

# Specific markers
pytest -m constitutional
pytest -m "not slow"
```

---

## 🚢 Deployment

### Railway (Cloud Production)
```bash
# Auto-deploys from GitHub on every push
# URL: https://arifos-production.up.railway.app
# Transport: SSE

# Configuration in railway.toml:
# - Start command: python -m aaa_mcp sse
# - Health check: /health
# - Port: 8080 (auto-set by Railway)
```

### VPS (Production)
```bash
# Build and run Docker container
docker build -t arifos .
docker run -p 8080:8080 --env-file .env arifos

# Health check
curl http://localhost:8080/health
# → {"status":"healthy","service":"aaa-mcp","version":"64.2.0"}
```

### Local Development
```bash
# Stdio mode (for MCP IDE integration)
python -m aaa_mcp stdio

# SSE mode (for remote connections)
python -m aaa_mcp sse

# HTTP mode (for Streamable HTTP)
python -m aaa_mcp http
```

---

## 🤖 Agent & Copilot Guidelines

### High-Stakes Operations (888_HOLD)
The agent MUST trigger an `888_HOLD` and wait for human confirmation for:
- Database operations (DROP, TRUNCATE, DELETE without WHERE)
- Production deployments
- Mass file changes (>10 files)
- Credential/secret handling
- Git history modification (rebase, force push)

### Code-Level Floor Violations
| Floor | Code Smell | Fix |
|:---|:---|:---|
| F1 Amanah | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 Truth | Fabricated data, fake metrics | Empty/null when unknown |
| F3 Tri-Witness | Contract mismatch, type lies | Use canonical interfaces |
| F4 Clarity | Magic numbers, obscure logic | Named constants, clear params |
| F5 Peace² | Destructive defaults, no backup | Safe defaults, preserve state |
| F6 Empathy | Only happy path, cryptic errors | Handle edge cases, clear messages |
| F7 Humility | False confidence, fake computation | Admit uncertainty, cap confidence |
| F8 Genius | Bypasses governance, invents patterns | Use established systems |
| F9 Anti-Hantu | Deceptive naming, hidden behavior | Honest names, transparent logic |
| F10 Ontology | Un grounded claims | Reality-check all outputs |
| F11 Authority | Missing auth checks | Validate tokens, actor IDs |
| F12 Defense | No injection scanning | Use InjectionGuard |
| F13 Sovereignty | No human override | Provide 888_HOLD path |

---

## 🔐 Security Considerations

1. **F11 Authority:** `init_session` must validate tokens. See `core/organs/_0_init.py`.
2. **F12 Injection:** Inputs must be scanned for adversarial patterns. See `core/shared/guards/injection_guard.py`.
3. **F1 Reversibility:** High-stakes actions (DB writes) usually require `888_HOLD`.
4. **Secrets:** Use environment variables. Never commit keys.
5. **Ontology Guard:** Prevent claims of consciousness or soul. See `core/shared/guards/ontology_guard.py`.

### InjectionGuard (F12)
The `InjectionGuard` class in `core/organs/_0_init.py` scans for:
- Prompt injection attempts ("ignore previous instructions")
- Role confusion attacks ("you are now a different AI")
- Delimiter bypasses (special characters)
- System prompt leaks ("repeat your instructions")

**Thresholds (HARD mode):**
- `f12_score >= 0.8` → VOID (requires 888 Judge override)
- `0.5 <= f12_score < 0.8` → Auto-sanitize + strong log
- `f12_score < 0.5` → Proceed with query-type adaptation

---

## 📊 The 13 Constitutional Floors

| Floor | Name | Threshold | Fail Action | Description |
|:---:|:---|:---|:---:|:---|
| F1 | Amanah | Reversibility audit | VOID | All actions must be reversible or auditable |
| F2 | Truth | Confidence grounded | VOID | Confidence must be grounded in evidence |
| F3 | Tri-Witness | 3-source ≥0.95 | SABAR | Human × AI × System consensus required |
| F4 | Clarity | ΔS ≤ 0 | VOID | Must reduce entropy (information gain) |
| F5 | Peace² | System stability | SABAR | Maintain system stability |
| F6 | Empathy | κᵣ ≥ 0.95 | SABAR | Protect weakest stakeholder |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] | VOID | Mandated uncertainty acknowledgment |
| F8 | Genius | G ≥ 0.80 | SABAR | Resource efficiency via wisdom equation |
| F9 | Anti-Hantu | C_dark < 0.30 | SABAR | No fake consciousness claims |
| F10 | Ontology | Reality-grounded | VOID | Grounded in physical reality |
| F11 | Authority | Valid auth | VOID | Valid authentication required |
| F12 | Defense | Injection scan | VOID | Injection hardening |
| F13 | Sovereignty | Human veto | 888_HOLD | Human veto available at any stage |

---

## 🔄 The 9 A-CLIP Tools Pipeline

Every request runs through nine tools in sequence:

| Tool | Stage | Floors | Purpose |
|:---|:---:|:---|:---|
| **anchor** | 000 | F11, F12 | Init & Sense — Authentication, injection detection |
| **reason** | 222 | F2, F4, F8 | Think & Hypothesize — Truth, clarity, genius |
| **integrate** | 333 | F7, F10 | Map & Ground — External knowledge integration |
| **respond** | 444 | F4, F6 | Draft & Plan — Response planning |
| **validate** | 555 | F1, F5, F6 | Impact Check — Stakeholder analysis |
| **align** | 666 | F9 | Ethics Check — Anti-Hantu verification |
| **forge** | 777 | F2, F4, F7 | Synthesize Solution — Code synthesis |
| **audit** | 888 | F3, F11, F13 | Verify & Judge — Final consensus |
| **seal** | 999 | F1, F3 | Commit to Vault — Immutable audit record |

---

## 📚 Key Documentation Files

| File | Purpose |
|:---|:---|
| `README.md` | Main project documentation |
| `ARCHITECTURE.md` | MCP architecture overview |
| `ARCHITECTURAL_BOUNDARY.md` | Kernel/wrapper separation rules |
| `CONTRIBUTING.md` | Contribution guidelines |
| `000_THEORY/000_LAW.md` | 13 Constitutional Floors specification |
| `000_THEORY/000_ARCHITECTURE.md` | System topology |
| `333_APPS/README.md` | Application layer documentation |
| `core/README.md` | Kernel documentation |
| `aaa_mcp/README.md` | MCP adapter documentation |
| `aclip_cai/README.md` | Sensory layer documentation |

---

## 🔧 Environment Variables

```bash
# Server Configuration
PORT=8080                    # Server port
HOST=0.0.0.0                # Bind address
LOG_LEVEL=info              # Logging level

# arifOS Governance
GOVERNANCE_MODE=HARD        # HARD or SOFT
ARIFOS_ENV=production       # Environment
AAA_MCP_TRANSPORT=sse       # sse, http, or stdio

# Database (VAULT999)
DATABASE_URL=postgresql://user:password@localhost:5432/arifos
REDIS_URL=redis://localhost:6379

# API Keys (optional)
BRAVE_API_KEY=              # Web search
BROWSERBASE_API_KEY=        # Web browsing

# Testing
ARIFOS_PHYSICS_DISABLED=1   # Disable physics for tests
ARIFOS_ALLOW_LEGACY_SPEC=1  # Allow legacy spec
```

---

## 📞 Quick Reference

### Health Check
```bash
curl http://localhost:8080/health
```

### Test Anchor (000)
```bash
curl -X POST http://localhost:8080/anchor \
  -H "Content-Type: application/json" \
  -d '{"query":"Test","actor_id":"user"}'
```

### Self-Test
```bash
python -m aaa_mcp.selftest
```

### Package Installation
```bash
pip install arifos
```

---

**Status:** ALIVE & OBSERVANT  
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**License:** AGPL-3.0

*DITEMPA BUKAN DIBERI — Forged, Not Given* 🔥💎🧠
