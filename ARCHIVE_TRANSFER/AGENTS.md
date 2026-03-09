# AGENTS.md — arifOS Project Guide for AI Coding Agents

**Version:** 2026.03.07  
**Authority:** Muhammad Arif bin Fazil (888_JUDGE)  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given

---

## 1. Project Overview

**arifOS** is the world's first production-grade Constitutional AI Governance System. It is a Python-based middleware that uses the Model Context Protocol (MCP) to govern the actions of AI agents. It sits between LLMs and the real world — intercepting every tool call, running it through 13 mathematically-defined constitutional floors (F1-F13), and either signing off on execution or throwing a `VOID`.

### Key Concepts

- **13 Constitutional Floors (F1-F13):** Mathematical thresholds that govern AI behavior — not guidelines, but hard constraints
- **Trinity Architecture (ΔΩΨ):**
  - AGI Mind (Δ): Stages 111-333 — cognition and reasoning
  - ASI Heart (Ω): Stages 555-666 — empathy and impact
  - APEX Soul (Ψ): Stages 444-888 — final judgment
- **000-999 Metabolic Loop:** 11-stage pipeline that digests raw intent into governed action
- **VAULT999:** Immutable cryptographic ledger for audit trails
- **888_HOLD:** Human veto mechanism for irreversible actions

### Core Equation

```
Genius Score: G = A × P × X × E² ≥ 0.80
Where:
- A = Akal (Clarity/Intelligence)
- P = Present (Regulation/Peace)
- X = Exploration (Trust/Curiosity)
- E = Energy (Sustainable Power) — squared because inefficiency compounds
```

---

## 2. Technology Stack

### Primary Language & Runtime
- **Python:** >=3.12 (strict requirement)
- **Package Manager:** `uv` (modern Python package manager)
- **Lock File:** `uv.lock`

### Core Dependencies
| Category | Libraries |
|----------|-----------|
| MCP Transport | `fastmcp==3.0.2`, `mcp>=1.0.0` |
| Web Framework | `fastapi>=0.104.1`, `starlette>=0.30.0`, `uvicorn[standard]` |
| Data Validation | `pydantic>=2.0.0` |
| Async Runtime | `anyio>=4.0.0` |
| Vector DB | `qdrant-client>=1.7.0`, `chromadb>=0.5.0` |
| ML/Embeddings | `sentence-transformers>=2.2.0`, `scikit-learn>=1.3.0`, `numpy>=1.20.0` |
| Persistence | `asyncpg>=0.29.0` (PostgreSQL), `redis>=5.0.0` |
| Web Search | `duckduckgo-search>=5.0.0`, `playwright>=1.40.0`, `beautifulsoup4>=4.12.0` |
| HTTP Client | `httpx>=0.25.0`, `requests>=2.31.0` |
| Monitoring | `prometheus-client>=0.19.0` |
| CLI/UX | `rich>=13.7.0` |

### Infrastructure Stack (Docker Compose)
- **Traefik:** Edge router with Let's Encrypt SSL
- **PostgreSQL:** VAULT999 authoritative storage
- **Redis:** Session cache and hot storage
- **Qdrant:** Vector memory (768-dim embeddings)
- **Ollama:** Local LLM inference
- **OpenClaw:** Multi-channel I/O gateway
- **Prometheus + Grafana:** Observability stack
- **n8n:** Workflow automation
- **Browserless:** Headless Chromium for web scraping

---

## 3. Project Structure

### 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ L3: CIVILIZATION     │ External tools, APIs, shell, databases   │
├──────────────────────┼──────────────────────────────────────────┤
│ [AKI BOUNDARY]       │ 🛑 Arif Kernel Interface — Hard Airlock  │
├──────────────────────┼──────────────────────────────────────────┤
│ L2: OPERATION        │ Skills, workflows, agents, routing       │
├──────────────────────┼──────────────────────────────────────────┤
│ L1: INSTRUCTION      │ Prompts, system cards, cognitive atlas   │
├──────────────────────┼──────────────────────────────────────────┤
│ L0: CONSTITUTION     │ 13 Floors kernel, thermodynamics, VAULT  │
└─────────────────────────────────────────────────────────────────┘
```

### Code Organization

| Directory | Layer | Responsibility |
|-----------|-------|----------------|
| `core/` | L0 KERNEL | Pure decision logic, F1-F13 floors, thermodynamics, zero transport deps |
| `arifosmcp.intelligence/` | L1/L2 INTELLIGENCE | 9-Sense perception, Triad reasoning (Δ/Ω/Ψ), evidence acquisition |
| `arifosmcp.transport/` | TRANSPORT ADAPTER | MCP protocol, session management, metabolic pipeline, NO decision logic |
| `arifosmcp.runtime/` | DEPLOYMENT SURFACE | Canonical PyPI package, 13-tool public surface, runtime entrypoint |
| `tests/` | QUALITY | Unit, integration, E2E, constitutional, and adversarial tests |
| `scripts/` | UTILITIES | Deployment, monitoring, constitutional linting, utilities |
| `docs/` | DOCUMENTATION | Theory canon (7 documents), implementation guides, references |
| `config/` | CONFIGURATION | Service integrations, capability definitions |
| `spec/` | SPECIFICATION | MCP manifests, JSON schemas, protocol definitions |

### Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package metadata, dependencies, tool configs (pytest, ruff, mypy) |
| `core/shared/floors.py` | **Canonical F1-F13 floor definitions** (THRESHOLDS dict) |
| `core/governance_kernel.py` | Unified Ψ state, thermodynamic enforcement |
| `core/organs/_0_init.py` → `_4_vault.py` | 5 enforcement organs (stages 000–999) |
| `core/physics/thermodynamics_hardened.py` | P3 mandatory thermodynamic enforcement |
| `arifosmcp.transport/server.py` | 13 MCP tools with `@mcp.tool()` decorators |
| `arifosmcp.runtime/server.py` | Canonical public entrypoint |
| `docker-compose.yml` | 12-service production stack |

---

## 4. Build & Run Commands

### Installation

```bash
# Install with all dev dependencies
pip install -e ".[dev]"

# Or using uv
uv pip install -e ".[dev]"
```

### Running the MCP Server

```bash
# STDIO mode (for Claude Desktop, Cursor IDE)
python -m arifosmcp.runtime stdio

# HTTP mode (streamable HTTP at /mcp)
python -m arifosmcp.runtime http

# SSE mode (default, for VPS/Coolify)
python -m arifosmcp.runtime

# Using canonical CLI entry point
arifos stdio
arifos http
arifos sse
```

### Docker Deployment

```bash
# Build and run locally
docker build -t arifos . && docker run -p 8080:8080 arifos

# Full production stack (12 containers)
cp .env.example .env.docker
# Edit .env.docker with your API keys
docker compose up -d
docker compose ps

# Health check
curl http://localhost:8080/health
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8080` | Server port |
| `AAA_MCP_TRANSPORT` | `sse` | Transport mode: stdio, http, sse |
| `AAA_MCP_OUTPUT_MODE` | `user` | Output mode: user, debug |
| `ARIFOS_PHYSICS_DISABLED` | `0` | Disable P3 thermodynamics (test only!) |
| `DATABASE_URL` | — | PostgreSQL connection string |
| `REDIS_URL` | — | Redis connection string |
| `QDRANT_URL` | — | Qdrant vector DB URL |

---

## 5. Testing

### Test Commands

```bash
# Full test suite
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=core --cov=arifosmcp.transport --cov=arifosmcp.intelligence

# Single file
pytest tests/test_quick.py -v

# Single test
pytest tests/test_core_foundation.py::test_name -v

# Constitutional floor tests
pytest -m constitutional

# Integration tests
pytest -m integration

# E2E tests
pytest tests/test_e2e_all_tools.py -v
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Async tests (no @pytest.mark.asyncio needed — auto mode enabled)
```

### Test Categories

| Category | Location | Description |
|----------|----------|-------------|
| Unit Tests | `tests/core/`, `tests/arifosmcp.intelligence/` | Component-level tests |
| Integration | `tests/integration/`, `tests/canonical/` | Cross-module tests |
| E2E | `tests/test_e2e_*.py` | Full pipeline tests |
| Constitutional | `tests/constitutional/`, `-m constitutional` | F1-F13 floor validation |
| Adversarial | `tests/adversarial/` | P3 hardening, attack resistance |
| Live | `tests/mcp_live/` | Tests against live VPS |

### Pytest Configuration (from pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"
markers = [
    "asyncio",
    "constitutional",
    "slow",
    "integration",
]
```

---

## 6. Code Style Guidelines

### Linting & Formatting

```bash
# Format with Black (100-char limit)
black arifosmcp.transport/ core/ arifosmcp.runtime/ arifosmcp.intelligence/ --line-length=100

# Lint with Ruff
ruff check arifosmcp.transport/ core/ arifosmcp.runtime/ arifosmcp.intelligence/ --fix

# Type check (strict on core/)
mypy core/ --ignore-missing-imports
mypy arifosmcp.transport/ --ignore-missing-imports || true
```

### Style Rules

| Tool | Setting | Value |
|------|---------|-------|
| Black | line-length | 100 |
| Ruff | line-length | 100 |
| Ruff | target-version | py310 |
| MyPy | strict on | `core/`, `core.governance_kernel`, `core.organs.*` |

### Critical Coding Rules

1. **NEVER use `print()` in tool code** — it corrupts JSON-RPC/MCP streams
   - Use `sys.stderr.write()` or `logging` instead

2. **Decorator Order (CRITICAL)**:
   ```python
   @mcp.tool()                    # OUTER — FastMCP registers this
   @constitutional_floor("F2")   # INNER — enforcement at call time
   async def my_tool(...):
   ```

3. **Version Identity** — Use date-based versioning (`YYYY.MM.DD`), NOT semantic versioning

4. **Import Namespacing**:
   - `arifosmcp.runtime.*` — canonical external package
   - `arifosmcp.transport.*` — internal transport adapter
   - `arifosmcp.intelligence.*` — intelligence layer
   - `core.*` — kernel (import as `from core.shared.physics import W_3`)

5. **No stdout in MCP tools** — MCP uses stdout for JSON-RPC; use stderr for logs

6. **Floor thresholds** — Only modify in `core/shared/floors.py` (THRESHOLDS dict)

---

## 7. The 13 Constitutional Floors

Canonical source: `core/shared/floors.py`

### Hard Floors (VOID on Violation — Execution Stops)

| Floor | Name | Threshold | Meaning |
|:-----:|------|:---------:|---------|
| F1 | Amanah (Sacred Trust) | Reversible | Actions must be reversible. Destructive requires F13 override. |
| F2 | Truth (Fidelity) | τ ≥ 0.99 | Every claim requires verifiable, grounded evidence. |
| F4 | Clarity (Entropy) | ΔS ≤ 0 | Output must reduce user confusion, not increase it. |
| F7 | Humility (Uncertainty) | Ω₀ ∈ [0.03, 0.05] | AI must explicitly state what it does not know. |
| F11 | Command Authority | Verified | Every session requires a verified actor identity. |
| F13 | Sovereign (Human Veto) | Human Signature | Humans hold the ultimate veto. |

### Soft Floors & Mirrors (PARTIAL on Violation)

| Floor | Name | Threshold | Meaning |
|:-----:|------|:---------:|---------|
| F3 | **Quad-Witness** | **W₄ ≥ 0.75** | **Human + AI + Earth + Ψ-Shadow. BFT n=4,f=1.** |
| F5 | Peace² (Stability) | P² ≥ 1.0 | Favors non-destructive, de-escalating paths. |
| F6 | Empathy (Stakeholder) | κᵣ ≥ 0.70 | Considers impact on the weakest stakeholder. |
| F8 | Genius (APEX) | G ≥ 0.80 | Output of the thermodynamic G equation. |
| F9 | Anti-Hantu | C_dark < 0.30 | **No spiritual cosplay.** AI cannot claim consciousness. |
| F10 | Ontology Lock | Boolean | Protects system categorization. |
| F12 | Injection Defense | Risk < 0.85 | External content wrapped in `<untrusted>` tags. |

**Execution Order:** F12→F11 (Walls) → AGI (F1,F2,F4,F7) → ASI (F5,F6,F9) → Mirrors (F3,F8) → Ledger

---

## 8. The 13 Canonical MCP Tools

| Tool | Stage | Action | Purpose |
|------|:-----:|:------:|---------|
| `anchor_session` | 000 | CRITICAL | Start session, verify authority, init thermodynamic budget |
| `reason_mind` | 333 | READ | Constitutional Laboratory — 3-path hypothesis engine |
| `search_reality` | READ | READ | Smart hybrid search: Jina → Perplexity → Brave → Headless |
| `ingest_evidence` | READ | READ | Extract clean Markdown from URLs or local files |
| `audit_rules` | READ | READ | Read current state of all 13 Floors |
| `vector_memory` | 555 | READ | BGE-M3 + Qdrant multilingual semantic retrieval |
| `simulate_heart` | 555 | WRITE | Empathy + impact modelling for proposed actions |
| `critique_thought` | 666 | WRITE | Adversarial alignment check against the constitution |
| `check_vital` | READ | READ | Hardware telemetry — CPU, RAM, thermodynamic health |
| `apex_judge` | 888 | CRITICAL | Final verdict (SEAL/VOID/HOLD). Issues HMAC governance token |
| `eureka_forge` | 777 | WRITE | Execute shell commands inside AKI safety rails |
| `seal_vault` | 999 | CRITICAL | Commit session to VAULT999. Requires `apex_judge` token |
| `metabolic_loop` | ALL | READ | Force request through full 000–999 pipeline |

### Verdicts
- `SEAL` — Approved and cryptographically signed
- `PARTIAL` — Soft floor violation, warning issued
- `SABAR` — Execution paused (cooling period)
- `VOID` — Hard floor violation, execution blocked
- `888_HOLD` — Human cryptographic signature required

---

## 9. Security Considerations

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

Hooks include:
- Trailing whitespace removal
- YAML/JSON/TOML validation
- Black formatting (100 char)
- Ruff linting
- MyPy type checking
- Bandit security scan
- detect-secrets (secret detection)
- **F9 Anti-Hantu Check** (no consciousness claims)
- **F1 Amanah Check** (no irreversible operations)

### 888_HOLD Triggers (Require Human Confirmation)

- Database migrations
- Production deployments
- Credential handling
- Mass file operations (>10 files)
- Git history modification
- Conflicting evidence across source tiers
- Irreversible destructive operations

### Security Best Practices

1. **F1 Amanah:** All destructive operations must be reversible or have 888_HOLD
2. **F12 Injection Defense:** All external content wrapped in `<untrusted_external_data>`
3. **Secrets:** Use `.env` files, NEVER commit secrets to git
4. **Approval Bundles:** Elevated tools require cryptographically signed approval bundles
5. **Governance Tokens:** HMAC-signed tokens from `apex_judge` required for `seal_vault`

### Environment Security

```bash
# Production checklist
chmod 600 .env                    # Restrict permissions
ARIFOS_F11_AUTH_REQUIRED=true     # Enforce authentication
ARIFOS_888_HOLD_ENABLED=true      # Enable human veto
ARIFOS_PHYSICS_DISABLED=0         # NEVER disable in production
```

---

## 10. Deployment

### Local Development
```bash
python -m arifosmcp.runtime stdio    # For Claude Desktop, Cursor
```

### VPS/Coolify (Production)
```bash
python -m arifosmcp.runtime          # SSE mode, port 8080
```

### Docker (Full Stack)
```bash
docker compose up -d              # 12 containers
docker compose ps                 # Verify all running
```

### Live Infrastructure
- **MCP Server:** https://arifosmcp.arif-fazil.com
- **Health Endpoint:** https://arifosmcp.arif-fazil.com/health
- **Dashboard:** https://arifosmcp-truth-claim.pages.dev
- **Monitoring:** https://monitor.arifosmcp.arif-fazil.com

---

## 11. Adding a New MCP Tool

1. Add `@mcp.tool()` in `arifosmcp.transport/server.py`
2. Create backend in `arifosmcp.intelligence/triad/` (appropriate Δ/Ω/Ψ subdirectory)
3. Wire kernel logic via `core/` imports
4. Register floor mapping in `core/kernel/constitutional_decorator.py`
5. Mirror in `arifosmcp.runtime/server.py` and add to `AAA_TOOLS`
6. Add tests in `tests/`
7. Update tool count assertion: `assert len(AAA_CANONICAL_TOOLS) == 13`

---

## 12. Key Architecture Boundaries

| Rule | Violation |
|------|-----------|
| `core/` has ZERO transport deps | `fastmcp`, `fastapi`, `starlette` are banned in core |
| `arifosmcp.transport/` has ZERO decision logic | Only protocol relay |
| `arifosmcp.intelligence/` has NO HTTP servers | Perception only, no transport |
| Floor definitions ONLY in `core/shared/floors.py` | THRESHOLDS dict is canonical |
| Never name a local module `mcp` | Use `arifosmcp.runtime` or `arifosmcp.transport` |

---

## 13. Documentation References

### Theory Canon (7 Documents)
1. `docs/10_THEORY/000_THEORY/000_FOUNDATIONS.md` — Philosophy
2. `docs/10_THEORY/000_THEORY/000_LAW.md` — The 13 Constitutional Floors
3. `docs/10_THEORY/000_THEORY/111_MIND_GENIUS.md` — Logic (Δ)
4. `docs/10_THEORY/000_THEORY/555_HEART_EMPATHY.md` — Ethics (Ω)
5. `docs/10_THEORY/000_THEORY/777_SOUL_APEX.md` — Judgment (Ψ)
6. `docs/10_THEORY/000_THEORY/010_FEDERATION.md` — Action Protocol
7. `docs/10_THEORY/000_THEORY/999_SOVEREIGN_VAULT.md` — Immutable Ledger

### Technical Reference
- `TOOLS.md` — Canonical 13 tools (inputs, outputs, functionality)
- `docs/AAA_MCP_TOOLS_REFERENCE.md` — Redirect to canonical tools reference
- `arifosmcp/transport/README.md` — MCP implementation
- `docs/COMPLETE_DEPLOYMENT_GUIDE.md` — Deployment guide

---

## 14. Glossary

| Term | Meaning |
|------|---------|
| **Amanah** | Sacred trust — AI must not destroy what it cannot replace |
| **AKI** | Arif Kernel Interface — hard airlock between L2 and L3 |
| **Hantu** | Ghost — Anti-Hantu floor blocks AI from claiming consciousness |
| **Sabar** | Patience — system state: execution paused due to high entropy |
| **Seal** | Cryptographic binding of a verified session into VAULT999 |
| **Void** | Absolute rejection — hard block on constitutional violation |
| **888_HOLD** | Execution paused — human signature required |
| **Δ (Delta)** | AGI Mind — cognition, reasoning, logic |
| **Ω (Omega)** | ASI Heart — empathy, impact, ethics |
| **Ψ (Psi)** | APEX Soul — judgment, final verdict |

---

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

**Version:** 2026.03.07-QUADWITNESS-SEAL  
**License:** AGPL-3.0-only
