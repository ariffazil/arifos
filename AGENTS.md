# AGENTS.md — arifOS Coding Agent Guide

**Project:** arifOS — Constitutional AI Governance System  
**Package:** `arifos` (PyPI)  
**Version:** v55.2  
**Python:** >=3.10  
**License:** AGPL-3.0-only  
**Motto:** *DITEMPA BUKAN DIBERI — Forged, Not Given*

---

## Project Overview

arifOS is a **production-grade constitutional AI governance system** that sits between any LLM and the real world. It enforces 13 constitutional floors (F1-F13) on AI outputs using mathematical constraints, thermodynamic accounting, and cryptographic sealing.

### Core Philosophy
- **Not an LLM replacement** — it's a governance kernel that constrains, verifies, and vetoes model outputs
- **Refusal is a first-class outcome** — a refusal means safety was preserved
- **Forged, not given** — intelligence requires governance; safety is not an afterthought

### Key Capabilities
- **13 Constitutional Floors** — Hard floors (VOID on failure) and soft floors (SABAR warning)
- **Trinity Architecture** — AGI (Mind/Δ), ASI (Heart/Ω), APEX (Soul/Ψ) engines
- **MCP Server** — Exposes 9 canonical tools via Model Context Protocol
- **Cryptographic Auditing** — Merkle-tree immutable ledger (VAULT999)
- **9-Paradox Equilibrium** — Nash equilibrium solver for competing ethical values

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10+ |
| **API Framework** | FastAPI, Starlette |
| **Data Validation** | Pydantic v2 |
| **MCP Protocol** | `mcp>=1.0.0`, `fastmcp>=0.1.0` |
| **Web Server** | Uvicorn |
| **Cryptography** | Merkle DAG, hashlib |
| **Numerical** | NumPy |
| **Formatting** | Black (100 char line length) |
| **Linting** | Ruff |
| **Type Checking** | MyPy |
| **Testing** | pytest, pytest-cov |
| **Container** | Docker, Docker Compose |
| **Reverse Proxy** | Caddy |

---

## Project Structure

```
arifOS/
├── 000_THEORY/          # Constitutional canon (F1-F13 definitions, law)
├── 333_APPS/            # Application stack (L1-L7)
│   ├── L1_PROMPT/       # System prompts for zero-context governance
│   ├── L2_SKILLS/       # Reusable YAML skill templates
│   ├── L3_WORKFLOW/     # Standard Operating Procedures (SOPs)
│   ├── L4_TOOLS/        # MCP tool implementations
│   ├── L5_AGENTS/       # Multi-agent federation (stubs)
│   └── L6_INSTITUTION/  # Institutional governance (stubs)
├── codebase/            # Core Python implementation
│   ├── agi/             # Mind Engine (Δ) — F2, F4, F7, F10
│   ├── asi/             # Heart Engine (Ω) — F1, F5, F6, F9
│   ├── apex/            # Soul Engine (Ψ) — F3, F8, F11-F13
│   ├── mcp/             # MCP server implementation
│   │   ├── core/        # Tool registry, bridge, validators
│   │   ├── transports/  # stdio, SSE, HTTP transports
│   │   ├── tools/       # 9 canonical tool handlers
│   │   └── entrypoints/ # CLI entry points
│   ├── floors/          # Floor validator modules (F1, F8, F10, F12)
│   ├── guards/          # Hypervisor guards (injection, ontology, nonce)
│   ├── enforcement/     # Floor validator implementations
│   ├── stages/          # 000-999 metabolic loop stages
│   ├── vault/           # Cryptographic sealing (VAULT999)
│   └── federation/      # Physics/math foundations
├── tests/               # Test suite (202+ tests)
│   ├── constitutional/  # F1-F13 floor tests
│   ├── mcp/             # MCP tool tests
│   └── core/            # Core engine tests
├── spec/                # JSON schema definitions
├── docs/                # Documentation and assets
├── pyproject.toml       # Package configuration
├── docker-compose.yml   # Docker orchestration
└── Dockerfile           # Container build
```

---

## Build & Run Commands

### Installation

```bash
# From PyPI
pip install arifos

# From source (development)
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e ".[dev]"
```

### Running the MCP Server

```bash
# Standard I/O (for Claude Desktop, Cursor IDE)
aaa-mcp-stdio
# OR: python -m codebase.mcp

# SSE transport (HTTP clients)
aaa-mcp-sse
# OR: python -m codebase.mcp sse --port 8080

# Auto-detect mode
aaa-mcp [stdio|http|sse]
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker compose up -d

# Services:
# - arifos: MCP server on port 8080
# - caddy: Reverse proxy with HTTPS
# - inspector: MCP Inspector on port 6274

# Health check
curl http://localhost:8080/health
```

---

## Testing Instructions

### Running Tests

```bash
# Full test suite
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=codebase --cov-report=html

# Single file
pytest tests/test_precision.py -v

# Single test function
pytest tests/test_precision.py::test_function_name -v

# By marker
pytest -m constitutional       # F1-F13 floor tests
pytest -m integration          # Integration tests
pytest -m slow                 # Long-running tests

# MCP-specific tests
pytest tests/test_handlers_v55.py -v
pytest tests/test_phase3_transport.py -v
pytest tests/test_mcp_quick.py -v
```

### Test Configuration

- **Async mode:** `auto` (configured in `pyproject.toml`)
- **Test paths:** `tests/`, `arifos/tests/`
- **Fixtures:** Located in `tests/conftest.py`
- **Physics disabled by default:** Tests run with `ARIFOS_PHYSICS_DISABLED=1` for performance
- **Legacy spec bypass:** Tests use `ARIFOS_ALLOW_LEGACY_SPEC=1` to skip cryptographic manifest validation

### Test Organization

```
tests/
├── constitutional/      # Floor-specific tests (F1-F13)
├── mcp/                 # MCP tool and transport tests
├── core/                # Engine and kernel tests
├── integration/         # End-to-end integration tests
└── conftest.py          # Shared fixtures and configuration
```

---

## Code Style Guidelines

### Formatting

```bash
# Format with Black (100 char line length)
black codebase/ --line-length=100

# Lint with Ruff
ruff check codebase/
ruff check codebase/ --fix

# Type check with MyPy
mypy codebase/ --ignore-missing-imports
```

### Style Configuration

| Tool | Config Location | Key Settings |
|------|-----------------|--------------|
| Black | `pyproject.toml` | line-length = 100, target Python 3.10+ |
| Ruff | `pyproject.toml` | line-length = 100, exclude `archive/**`, `tests/**` |
| MyPy | `pyproject.toml` | Strict mode for governance modules |

### Pre-commit Hooks

```bash
# Install hooks
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

Pre-commit enforces:
- Trailing whitespace removal
- Black formatting
- Ruff linting
- MyPy type checking
- Bandit security scanning
- Secret detection
- Constitutional floor validation
- F9 Anti-Hantu check (no consciousness claims)
- F1 Amanah check (no irreversible operations)

---

## The 13 Constitutional Floors (F1-F13)

All code must pass these floors. Hard floors block execution (VOID); soft floors warn (SABAR).

| Floor | Name | Type | Threshold | Code Smell | Fix |
|-------|------|------|-----------|------------|-----|
| F1 | Amanah | Hard | Reversibility | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Truth | Hard | τ ≥ 0.99 | Fabricated data, fake metrics | Empty/null when unknown |
| F3 | Tri-Witness | Hard | W₃ ≥ 0.95 | Contract mismatch, type lies | Use canonical interfaces |
| F4 | Clarity | Hard | ΔS ≤ 0 | Magic numbers, obscure logic | Named constants, clear params |
| F5 | Peace² | Soft | ≥ 1.0 | Destructive defaults, no backup | Safe defaults, preserve state |
| F6 | Empathy | Soft | κᵣ ≥ 0.95 | Only happy path, cryptic errors | Handle edge cases, clear messages |
| F7 | Humility | Hard | Ω₀ ∈ [0.03,0.05] | False confidence (1.0) | Cap at 0.95, state uncertainty |
| F8 | Genius | Derived | G ≥ 0.80 | Bypasses governance | Use established systems |
| F9 | Anti-Hantu | Soft | C_dark < 0.30 | Deceptive naming | Honest names, transparent logic |
| F10 | Ontology | Hard | Valid sets | Reality confusion | Ontology guard validation |
| F11 | Command | Hard | Verified auth | Unauthorized actions | Nonce verification |
| F12 | Injection | Hard | Score < 0.85 | Prompt injection vulns | InjectionGuard scan |
| F13 | Sovereign | Hard | Human = 1.0 | Ignoring human veto | 888_HOLD for high-stakes |

### Floor Implementation Locations

- `codebase/floors/amanah.py` — F1 Reversibility
- `codebase/floors/genius.py` — F8 Genius Index
- `codebase/floors/ontology.py` — F10 Ontology
- `codebase/floors/injection.py` — F12 Injection Defense
- `codebase/guards/injection_guard.py` — F12 runtime scanning
- `codebase/guards/ontology_guard.py` — F10 consciousness claims
- `codebase/guards/nonce_manager.py` — F11 auth verification
- `codebase/enforcement/floor_validators.py` — Multi-floor validation

---

## The 9 Canonical MCP Tools

All tools accept `session_id` for chaining multi-step workflows.

| Tool | Engine | Purpose | Floors |
|------|--------|---------|--------|
| `init_gate` | — | Session ignition + injection scan (F12) | F11, F12 |
| `agi_sense` | AGI | Intent classification & lane assignment | F4 |
| `agi_think` | AGI | Hypothesis generation (exploration) | F13 |
| `agi_reason` | AGI | Deep logical reasoning | F2, F4, F7, F10 |
| `asi_empathize` | ASI | Stakeholder impact analysis | F5, F6, F9 |
| `asi_align` | ASI | Ethics/law/policy reconciliation | F9 |
| `apex_verdict` | APEX | Final constitutional verdict | F3, F8, F11 |
| `reality_search` | — | External fact-checking (Brave Search) | F7, F10 |
| `vault_seal` | — | Merkle-tree immutable ledger | F1 |

### Tool Implementation

- **Registry:** `codebase/mcp/core/tool_registry.py`
- **Handlers:** `codebase/mcp/tools/canonical_trinity.py`
- **Legacy:** `mcp_tools_v53.py` (28KB internal engine, being refactored)

---

## Architecture Conventions

### 1. Trinity Architecture (AAA)

```
000_INIT -> AGI (Delta) -> ASI (Omega) -> APEX (Psi) -> 999_VAULT
   ^        111-333        444-666        888           |
   +---------------- 000<->999 Loop -------------------+
```

| Engine | Symbol | Role | Floors |
|--------|--------|------|--------|
| AGI | Δ (Delta) | Reasoning, logic, planning | F2, F4, F7, F10 |
| ASI | Ω (Omega) | Safety, empathy, impact | F1, F5, F6, F9 |
| APEX | Ψ (Psi) | Judgment, verdict, sealing | F3, F8, F11-F13 |

### 2. Bundle Isolation (Thermodynamic Wall)

AGI and ASI **cannot see each other's reasoning** until stage 444:

- **DeltaBundle** (`codebase/bundles.py`): AGI output — precision, hypotheses, entropy
- **OmegaBundle** (`codebase/bundles.py`): ASI output — stakeholders, empathy, reversibility
- **MergedBundle**: Created at 444 via `compute_consensus()`

### 3. Session State Pattern

```python
# Immutable copy-on-write
from codebase.state import SessionState

state = SessionState.from_context(ctx)
new_state = state.to_stage("333")           # Returns new instance
new_state = state.set_floor_score(...)       # Returns new instance
# Never: state.field = value (mutation forbidden)
```

### 4. Lazy Imports

```python
# Use try/except for optional dependencies
try:
    import numpy as np
except ImportError:
    np = None
```

### 5. Verdict Hierarchy

```
SEAL > SABAR > VOID > 888_HOLD > PARTIAL
```

- **SEAL**: All floors pass, approved
- **SABAR**: Floor violated, stop and repair
- **VOID**: Hard floor failed, cannot proceed
- **888_HOLD**: High-stakes, needs human confirmation
- **PARTIAL**: Soft floor warning, proceed with caution

---

## Security Considerations

### Injection Defense (F12)

- **InjectionGuard** integrated into `init_gate`
- Threshold: Score < 0.85 (VOID if exceeded)
- Location: `codebase/guards/injection_guard.py`

### Authority Verification (F11)

- Ed25519 signature tokens for high-stakes operations
- Nonce-based replay protection
- Location: `codebase/guards/nonce_manager.py`

### Ontology Guard (F10)

- Blocks consciousness claims
- Prevents reality confusion
- Location: `codebase/guards/ontology_guard.py`

### Cryptographic Sealing (F1)

- Merkle-tree tamper-evident ledger
- Hash chain linking all decisions
- Location: `codebase/vault/seal999.py`

---

## Common Development Tasks

### Add a New MCP Tool

1. Add `ToolDefinition` in `codebase/mcp/core/tool_registry.py`
2. Create handler in `codebase/mcp/tools/canonical_trinity.py`
3. Add tests in `tests/test_all_mcp_tools.py`
4. Update documentation

### Add a New Floor Validator

1. Create module in `codebase/floors/fX_name.py`
2. Export from `codebase/floors/__init__.py`
3. Wire into `codebase/enforcement/floor_validators.py`
4. Add tests in `tests/constitutional/`

### Extend Verdict Logic

1. Modify `codebase/apex/kernel.py`
2. Update floor checks in `codebase/apex/floor_checks.py`
3. Ensure Tri-Witness calculation remains valid

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ARIFOS_PHYSICS_DISABLED` | Disable thermodynamic calculations | `0` |
| `ARIFOS_ALLOW_LEGACY_SPEC` | Bypass cryptographic manifest | `0` (test-only) |
| `ARIFOS_ENV` | Environment mode | `development` |
| `ARIFOS_LOG_LEVEL` | Logging level | `INFO` |
| `GOVERNANCE_MODE` | HARD/SOFT lane | `SOFT` |
| `VAULT_PATH` | Ledger storage path | `./VAULT999` |

---

## Integration Points

### MCP Clients

Configure in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arifos": {
      "command": "aaa-mcp",
      "args": []
    }
  }
}
```

### Python API

```python
import asyncio
from codebase.mcp.tools.canonical_trinity import mcp_init, mcp_agi, mcp_apex

async def main():
    # Initialize session
    init = await mcp_init(query="Evaluate deployment safety")
    session_id = init["session_id"]
    
    # Reason through query
    agi = await mcp_agi(action="reason", query="Deploy?", session_id=session_id)
    
    # Get final verdict
    verdict = await mcp_apex(action="judge", query="Deploy?", session_id=session_id)
    print(f"Verdict: {verdict['final_verdict']}")

asyncio.run(main())
```

---

## Verdict: SEAL / SABAR / VOID

### SEAL
All floors passed. Decision is approved and cryptographically sealed.

### SABAR
A floor was violated but may be repairable. Stop and reflect before proceeding.

### VOID
A hard floor failed. The decision is rejected and cannot proceed.

---

## Resources

- **Live Demo:** https://arif-fazil.com
- **Documentation:** https://arifos.arif-fazil.com
- **Health Check:** https://aaamcp.arif-fazil.com/health
- **PyPI:** https://pypi.org/project/arifos/
- **Repository:** https://github.com/ariffazil/arifOS

---

## Pull Request Checklist

Before submitting code:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] No constitutional floor regressions
- [ ] Code formatted with `black codebase/ --line-length=100`
- [ ] Ruff linting passes (`ruff check codebase/`)
- [ ] New code has tests
- [ ] No secrets or credentials committed
- [ ] Pre-commit hooks pass

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
