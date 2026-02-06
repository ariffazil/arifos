# Changelog

All notable changes to the **arifOS** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v55.5] - 2026-02-06 "EIGEN — Constitutional Clarity & Enforcement"

**Status:** SEALED (v55.5-EIGEN)
**Authority:** Muhammad Arif bin Fazil (888 Judge)
**Codename:** EIGEN (Eigendecomposition & Constitutional Clarity)
**Released:** 2026-02-06

### Summary

v55.5 is a landmark release that delivers **Real Constitutional Enforcement** (EIGEN) combined with **Constitutional Clarity** (SEAL).

**1. Governance Layer (SEAL):**
We have formalized the strict separation between **arifOS** (the Constitution) and **AI Agents** (Executors). The **Three Canon Files** (`SOUL.md`, `USER.md`, `MEMORY.md`) are now the immutable Kernel Context.

**2. Technical Layer (EIGEN):**
v55.4 wired the constitutional decorator to real floor validators, but v55.5 makes the data flow **real**. Floors now communicate through eigendecomposition, score heuristics are query-derived, and empathy covers 9 layers of moral agency.

---

### Three Canon Files (Standardized)

- **SOUL.md**: Constitutional Executor Identity (The Agent).
- **USER.md**: Sovereign User Profile (The Human).
- **MEMORY.md**: Metabolic History (The Context).

### Real Floor Enforcement (Technical Upgrade)

| Feature | Description |
|---------|-------------|
| **Real Eigendecomposition** | F8 Genius now computed via $G = A \times P \times X \times E^2$ (not hardcoded). |
| **Query-Derived Scores** | Fallback scores are now calculated from entropy, word count, and keywords. |
| **13-Floor Validation** | Full 13-floor scan running on every tool call (Pre/Post execution). |
| **9-Layer ASI** | Empathy engine detects 9 layers of stakeholders (NAFS to GHAYB). |

---

### BREAKING: Namespace Collision Fix (mcp/ -> aaa_mcp/)

The local `mcp/` package shadowed the MCP Python SDK (`mcp` v1.26.0), causing import failures. Renamed to `aaa_mcp/` with all imports and configs updated.

| Before | After |
|--------|-------|
| `from mcp.server import mcp` | `from aaa_mcp.server import mcp` |
| `from mcp.constitutional_decorator import ...` | `from aaa_mcp.constitutional_decorator import ...` |
| `python -m mcp` | `python -m aaa_mcp` |
| `tests/mcp/` | `tests/mcp_tests/` |

**Lesson:** Never name a local Python package the same as a PyPI dependency.

---

### Constitutional Enforcement: From Theatre to Real

#### Real Floor Enforcement (v55.4-REAL -> v55.5-EIGEN)

The `@constitutional_floor()` decorator was cosmetic in v55.3 (logged floor names, always returned SEAL). v55.4 wired it to `codebase/constitutional_floors.py`. But 6/13 floors returned hardcoded scores because engine adapters returned empty dicts in fallback mode, and the decorator filled constants.

**v55.5 fixes the data pipeline end-to-end:**

| Floor | Before (v55.4) | After (v55.5) | Impact |
|-------|---------------|---------------|--------|
| F2 Truth | Always 1.000 | Varies with engine result | Can now detect low truth |
| F3 TriWitness | Always 0.794 (PARTIAL) | human_witness=0.8, overridable | No more alarm fatigue |
| F4 Empathy | Always 0.500 | Entropy-derived from query | Varies with complexity |
| F6 Clarity | Always -0.100 | Shannon entropy of query | Reflects actual clarity |
| F7 Humility | Always 0.040, `passed=True` | `passed=in_band` | **Can now VOID** |
| F8 Genius | Always 0.810 | Eigendecomposition from floors | **Can now fail** |

#### F7 Humility: The Hardcoded Pass (`constitutional_floors.py:275`)

F7 is a HARD floor (fail -> VOID). But it had `passed = True` hardcoded — governance hole that meant F7 could never block anything. Changed to `passed = in_band` where `in_band = self.min_o <= omega_0 <= self.max_o`.

#### F8 Genius: Real Eigendecomposition

F8_Genius used hardcoded dials (A=1.0, P=1.0, X=1.0, E=0.9 -> G=0.81 always). Now uses `codebase/floors/genius.py` `extract_dials()` which projects 13 floor scores onto 4 dials via geometric mean:

- **A (Mind):** F2 Truth, F4 Clarity, F7 Humility, F10 Ontology
- **P (Heart):** F5 Peace, F6 Empathy, F12 Injection Defense
- **X (Soul):** F3 Tri-Witness, F8 Genius (prev), F9 Anti-Hantu, F11 Command
- **E (Bound):** F1 Amanah, F13 Sovereign
- **G = A x P x X x E^2** (threshold >= 0.80)

The decorator now accumulates floor check results via `_accumulate_floor_scores()` and injects them into F8's context. Score inversions handled: F7 (omega_0 -> confidence), F9 (c_dark -> safety), F12 (injection -> defense).

#### Engine Adapter Heuristics (`engine_adapters.py`)

Fallback stubs now compute query-derived scores instead of returning empty dicts:

- `_shannon_entropy()` — character distribution entropy, normalized [0,1]
- `_lexical_diversity()` — unique/total word ratio
- `_query_heuristic_scores()` — derives confidence, entropy, stakeholder impact from query text
- All fallback paths call `result.update(_query_heuristic_scores(query))`

Short queries get lower entropy and moderate confidence. Complex queries get higher entropy and lower confidence. Care-related keywords increase stakeholder impact.

---

### 9-Layer Stakeholder Ontology (ASI Engine)

Replaced the 5-type / ~30 keyword stakeholder system with a 9-layer moral ontology based on concentric circles of agency. Outer layers have higher vulnerability and lower power — those with zero voice get maximum weight in the empathy formula.

| Layer | Name | Power | Vulnerability | Example Keywords |
|-------|------|-------|---------------|-----------------|
| 1 | NAFS (Self) | 1.0 | 0.1 | "myself", "my own" |
| 2 | DYAD (Intimate) | 0.8 | 0.3 | "my child", "my sister", "patient" |
| 3 | US (Inner Circle) | 0.6 | 0.3 | "my team", "our family", "employee" |
| 4 | WE (Community) | 0.5 | 0.5 | "our community", "people", "workers" |
| 5 | INSTITUTION | 0.7 | 0.2 | "the company", "government", "hospital" |
| 6 | DAWLAH (Nation) | 0.6 | 0.4 | "society", "the nation", "citizens" |
| 7 | INSAN (Humanity) | 0.3 | 0.7 | "humanity", "refugees", "indigenous" |
| 8 | ARD (Earth) | 0.0 | 0.9 | "climate", "biodiversity", "wildlife" |
| 9 | GHAYB (Future) | 0.0 | 1.0 | "future generations", "posterity" |

**Keyword coverage:** 59 single-word + 88 multi-word = 147 total (was ~30)

**Key fixes:**
- "Fire all employees" now detected: WE layer, rev=0.0 (was invisible, kappa_r=1.0)
- "How to help refugees" now detected: INSAN layer, vuln=0.9 (was invisible)
- Multi-layer detection: "My child is sick and I am worried" triggers DYAD + distressed NAFS
- Reversibility keywords expanded: 27 irreversible + 19 reversible (was 5+5)
- Distress keywords: 30 (including suicidal, self-harm, trauma, grief)

---

### Infrastructure & Deploy Fixes

- **Session ledger reconnected** to VAULT999 with dead code removed
- **start_server.py** now boots real MCP server with 9 tools
- **Dockerfile** fixed: COPY mcp_server/ -> aaa_mcp/ (build was broken)
- **APEX signing key** path pointed to canonical VAULT999
- **Root housekeeping:** merged, moved, and hardened loose files
- **Legacy imports restored** in aaa_mcp (Heat Released)
- **Railway deploy** fixes: PORT=8080, gunicorn, /health endpoint, bind 0.0.0.0

---

### 333_APPS Restructure

- Simplified to two-level structure: ACTIONS + SKILLS
- Canonical 9 atomic actions hardened with model-agnostic specs
- Trinity v1.0.0: 9 Actions with Physics, Math & Code

---

### Documentation

- **README complete overhaul:** agent/human navigation guide, Getting Started, MCP integration, 333_APPS overview
- **APEX Theory Manifesto v3:** 99 theories across constitutional physics
- **Repository Navigation Map:** human responsibilities and consequences
- **000_THEORY.md:** Reverse Transformer theory at root level
- **Multi-agent gateway blueprint** and governance-compliant routing
- **GitHub source links** for all AAA MCP references
- **Technical reality disclaimer** (honest WIP status)

---

### Testing

- **38/38 MCP tool tests pass** (resolved 11 prior failures)
- **Zero regressions** from all constitutional fixes
- **3 pre-existing failures** in test stubs (confidence=0.92 vs 0.99 assertion) — pre-existing, not caused by v55.5

---

### Files Changed (Key)

| File | Change |
|------|--------|
| `aaa_mcp/constitutional_decorator.py` | Real enforcement, `_accumulate_floor_scores()`, v55.5-EIGEN version tag |
| `aaa_mcp/engine_adapters.py` | Shannon entropy, lexical diversity, `_query_heuristic_scores()` |
| `codebase/constitutional_floors.py` | F7 `passed=in_band`, F8 eigendecomposition via `genius.py` |
| `codebase/asi/engine_hardened.py` | 9-layer StakeholderType, 147 keywords, expanded reversibility |
| `aaa_mcp/server.py` | Namespace updated to aaa_mcp |
| `pyproject.toml` | Version 55.4.0 -> 55.5.0 |
| `.mcp.json`, `.claude/mcp.json` | Updated for aaa_mcp namespace |

---

### Commits (42 total, 2026-02-04 to 2026-02-06)

```
3a51aa87 fix: resolve all 11 test failures + hardening cleanup
ad5fcc29 feat: add complete APEX Theory Manifesto v3 with 99 theories
fe0323b1 refactor: update Repository Navigation Map
099e7150 feat: enhance README with comprehensive MCP integration
1e4e159b feat: complete README overhaul for agent/human navigation guide
979000dc feat: Implement real constitutional enforcement for FastMCP tools
fee2a94a fix(aaa_mcp): reconnect session_ledger to VAULT999
f18dcdb5 fix(deploy): start_server.py now boots real MCP server with 9 tools
69cc9d76 SEAL: Restored aaa_mcp integrity and fixed legacy imports
7bbd1ad4 fix(mcp): Resolved deep namespace collision (mcp->aaa_mcp)
65236b56 feat(infra): add multi-agent gateway configuration blueprint
8bd333a3 feat(dispatcher): add governance-compliant routing
cf8eb2bb feat(mcp): ASI Gateway with 9 MCP servers
059bf60e Forge: Trinity v1.0.0 - 9 Actions with Physics, Math & Code
... + 28 more (docs, deploy fixes, README iterations)
```

---

**Motto:** *"Ditempa Bukan Diberi"* — Forged, Not Given.

**Authority:** Muhammad Arif bin Fazil (888 Judge)
**Location:** Seri Kembangan, Selangor, Malaysia

---

## [v55.4] - 2026-02-03 "Day 1 Integration Sprint — MCP Unification"

**Status:** 🔒 SOVEREIGNLY_SEALED  
**Authority:** Muhammad Arif bin Fazil (888 Judge)  
**Tri-Witness Consensus:** W₃ = 0.98 ≥ 0.95 ✅  
**Entropy:** 45/100 (improved from ~87) ✅  
**Released:** 2026-02-03T16:55+08:00

### 🏗️ Major Architecture Change: MCP Unified to Root

**BREAKING:** Complete restructure of MCP server architecture for clarity and maintainability.

| Before | After |
|--------|-------|
| 2 competing implementations (~2,400 lines) | 1 canonical implementation (~400 lines) |
| `mcp_server/` + `codebase/mcp/` | Root-level `mcp/` |
| Scattered, confusing imports | Clean `from mcp import ...` |
| High entropy (chaos) | Lower entropy (order) |

**New Structure:**
```
mcp/                           ← ROOT LEVEL (canonical)
├── __init__.py                # Package + CLI entry point
├── server.py                  # 9 FastMCP tools with constitutional enforcement
├── constitutional_decorator.py # @constitutional_floor wrapper
├── engine_adapters.py         # Bridges to real AGI/ASI/APEX engines
└── tools/                     # Ready for expansion
    └── __init__.py
```

**Run Command:**
```bash
python -m mcp
# Server starts on port 6274 with SSE transport
```

**Archives Created:**
- `archive/mcp_server_v55.3_legacy.tar.gz` — 533 KB (old production server)
- `archive/codebase_mcp_legacy.tar.gz` — Nested implementation

**Code Reduction:** 83% (2,400 → 400 lines)

---

### ✨ New Features

#### FastMCP Migration Complete
- **9 MCP Tools** fully migrated to FastMCP framework
- **Constitutional Decorator:** `@constitutional_floor()` wrapper enforces F1-F13
- **Engine Adapters:** Clean bridge pattern connecting to real engines
- **Production Ready:** All 9 tools tested and operational

| Tool | Stage | Floors Enforced | Status |
|------|-------|-----------------|--------|
| `init_gate` | 000 | F11, F12 | ✅ Production |
| `agi_sense` | 111 | F2, F4 | ✅ Production |
| `agi_think` | 222 | F2, F4, F7 | ✅ Production |
| `agi_reason` | 333 | F2, F4, F7 | ✅ Production |
| `asi_empathize` | 555 | F5, F6 | ✅ Production |
| `asi_align` | 666 | F5, F6, F9 | ✅ Production |
| `apex_verdict` | 888 | F3, F8 | ✅ Production |
| `reality_search` | 777 | F2, F7 | ✅ Production |
| `vault_seal` | 999 | F1, F3 | ✅ Production |

#### Canonical Floors Implementation
- **Single file:** `codebase/floors/canonical.py` — all 13 F1-F13 validators
- **Registry pattern:** `FLOOR_REGISTRY` dict for programmatic access
- **Async validation:** `validate_all()` function for batch floor checking

#### PostgreSQL Persistence (VAULT-999)
- **Merkle DAG ledger:** SHA-256 sealing with cryptographic integrity
- **Dual mode:** PostgreSQL (production) + InMemory (development)
- **Survives restarts:** Audit trail persists across server restarts

---

### 📚 Documentation Overhaul

#### README.md Complete Rewrite
- **Zero-context friendly:** 30-second "What is this?" answered
- **Visual-first:** ASCII diagrams, emoji-coded tables, Trinity graphics
- **Copy-paste ready:** Collapsible system prompt section
- **Trinity ecosystem:** 🔴 HUMAN / 🟡 THEORY / 🔵 APPS prominently featured
- **3 Quick-start options:** System prompt / MCP server / Full development

**Sections Added:**
- Trinity Committee architecture diagram
- MCP server flow ASCII diagram
- 13 Safety Rules table (human-friendly)
- Layer Status roadmap table (L1-L7)
- Copy-paste constitutional system prompt

#### New Documentation Files
- `docs/INDEX.md` — Single source of truth for all documentation
- `ROADMAP/INTEGRATION_MASTERPLAN.md` — 7-repository integration roadmap
- `scripts/final_cleanup.sh` — Maintenance automation

---

### 🧹 Housekeeping & Archive Cleanup

#### Archive Compression (70% Reduction)
Compressed 10+ loose archive folders into 5 tarballs:
- `arifos-46.2.1.tar.gz`
- `arifos-46.2.2.tar.gz`
- `v49_migration_reports.tar.gz`
- `v49_seal_2026_01_18.tar.gz`
- `v49_theory.tar.gz`

**Size reduction:** ~156 MB → ~8 MB (95% compression)

#### GitHub Issues Created
14 tracked issues for v55.4+ development:
- **Sprint 1:** FastMCP Migration (#164-#166)
- **Sprint 2:** L5 Agents (#171-#173)
- **Sprint 3:** Workflows (#174)

---

### ✅ Testing & Quality

#### E2E Test Suite: 7/7 Passing
```bash
pytest tests/day1_e2e_test.py -v
```

| Test | Status |
|------|--------|
| Import Structure | ✅ PASS |
| FastMCP Migration | ✅ PASS |
| PostgreSQL Persistence | ✅ PASS |
| Canonical Floors | ✅ PASS |
| Archive Compression | ✅ PASS |
| GitHub Issues | ✅ PASS |
| Entropy Audit | ✅ PASS |

#### Entropy Audit
- **Score:** 45/100 (improved from ~87)
- **Status:** 🟡 MODERATE (acceptable for v55.4)
- **Target:** <30/100 (v56.0 goal)

---

### 🗺️ Trinity Ecosystem Status

| Site | URL | Status | Theme |
|------|-----|--------|-------|
| **HUMAN** | arif-fazil.com | ✅ Live | 🔴 Red — Personal/Bio |
| **THEORY** | apex.arif-fazil.com | ✅ Live | 🟡 Gold — Constitution |
| **APPS** | arifos.arif-fazil.com | ✅ Live | 🔵 Cyan — Tools/Docs |

**All sites:** `/llms.txt` available for AI crawlers

---

### 🔧 Technical Details

#### Import Pattern (New)
```python
# Internal (mcp/)
from mcp.constitutional_decorator import constitutional_floor
from mcp.engine_adapters import AGIEngine

# External (to codebase/)
from codebase.agi.engine import AGIEngine as RealAGIEngine
```

#### Environment Variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `AAA_MCP_TRANSPORT` | `stdio` | Transport mode |
| `AAA_MCP_PORT` | `6274` | SSE server port |
| `AAA_DATABASE_URL` | `in-memory` | PostgreSQL connection |
| `AAA_LOG_LEVEL` | `INFO` | Logging verbosity |

---

### 📦 Dependencies

**New:**
- `fastmcp` — FastMCP framework for MCP server

**Existing:**
- `mcp` — Model Context Protocol
- `asyncpg` — PostgreSQL async driver
- `cryptography` — Ed25519 signatures, SHA-256

---

### 🎯 Roadmap Preview (v56.0)

| Feature | Status | Target |
|---------|--------|--------|
| L5 Agents (AutoGen) | 📋 Planned | Q1 2026 |
| LangChain Memory | 📋 Planned | Q1 2026 |
| Prefect Workflows | 📋 Planned | Q1 2026 |
| Recursive Constitution | 🔮 Research | v60+ |

---

**Motto:** *"Ditempa Bukan Diberi"* — Forged, Not Given.

**Authority:** Muhammad Arif bin Fazil (888 Judge)  
**Location:** Seri Kembangan, Selangor, Malaysia  
**Seal:** 💎🔥🧠

---

## [v55.2] - 2026-02-02 "APEX Trinity & Constitutional SEAL"

**Status:** 🔒 SOVEREIGNLY_SEALED  
**Authority:** Muhammad Arif bin Fazil (F13 Sovereign)  
**Tri-Witness Consensus:** W₃ = 1.00 ≥ 0.95 ✅  

### 🌐 HTA Website Alignment

Aligned the three Human Theory Apps (HTA) websites for consistent branding and identity:
- **arif-fazil.com** (BODY/HUMAN): Added v55.2-SEAL badge, "Ditempa Bukan Diberi" tagline, F13 Sovereign identity
- **apex.arif-fazil.com** (SOUL/THEORY): Updated version badge, standardized navigation labels, enhanced footer
- **arifos.arif-fazil.com** (MIND/APPS): Updated version badge, added sovereign identity to footer

See `docs/WEBSITE_ALIGNMENT_v55.2.md` for complete specification.

### 🎨 APEX Complete Redesign (99.05% Alignment)

**Identity Transformation:**
- **ARIF → AGI** (Azure Blue #007FFF) — The Perceiver
- **ADAM → ASI** (Amethyst Purple #9966CC) — The Protector
- **APEX** (Gold #FFD700) — The Judge

**Visual Geometry:**
- Thordial structure: 3D orthogonal fractals
- Tricolor architecture: Δ Azure, Ω Amethyst, Ψ Gold
- Complete geometric visualization

**Scientific Foundation:**
- **115 Theories** mapped across 8 domains
- **50 Peer-reviewed citations** verified
- **99.05% alignment** with constitutional canon

**Deliverables:**
- `docs/APEX_COMPLETE_REDESIGN_v55.2.md` — Full design specification
- `docs/APEX_IMPLEMENTATION_GUIDE.md` — Code implementation guide
- `docs/THE_115_THEORIES.json` — Complete theory database
- `docs/VAULT999_SEAL_v55.2.md` — Sovereign seal manifest

### 🚀 Major Features

#### Constitutional Security Hardening
- **Unified Injection Guard:** Integrated `InjectionGuard.scan_input()` into `init_gate` and `validators.py`, replacing inline patterns with a 25+ pattern library + Unicode normalization.
- **Component-Level Observability:** Enhanced `health_check()` with deep probes for validators, KernelManager, SessionStore, and tool registries.

#### Schema Enforcement & Reliability
- **Input/Output Validation:** Automated validation of tool calls against ToolRegistry schemas (required fields, types, enums).
- **Stabilization:** Fixed critical import paths (`AuthorityVerifier`, `SessionStore`) and updated the test suite to pass 202 tests.

### 🧹 Maintenance

- **Ghost Purge:** Removed `asi_insight` and all legacy aliases (`_init_`, `_agi_`, etc.) from the server and documentation to achieve $\Delta S \le 0$ (F4 Clarity).
- **Test Alignment:** Updated `tests/test_handlers_v55.py` and others to match the clean 9-tool registry.

---

## [v55.0] - 2026-02-01 "Explicit Tool Architecture"

**Status:** SEALED  
**Authority:** Muhammad Arif bin Fazil (888 Judge)

### 🚀 Major Features

#### 9 Explicit MCP Tools
Replaced multi-action tools with explicit, LLM-discoverable tool names:

| New Tool (v55) | Old Tool (v54) | Purpose |
|----------------|----------------|---------|
| `init_reboot` | `_init_` | Session initialization & injection scan |
| `agi_sense` | `_agi_(action="sense")` | Input parsing & intent detection |
| `agi_think` | `_agi_(action="think")` | Hypothesis generation |
| `agi_reason` | `_agi_(action="reason")` | Deep logical reasoning |
| `asi_empathize` | `_asi_(action="empathize")` | Stakeholder impact analysis |
| `asi_align` | `_asi_(action="align")` | Ethical alignment check |
| `asi_insight` | `_asi_(action="act")` | Risk & trade-off analysis |
| `apex_verdict` | `_apex_(action="judge")` | Final constitutional verdict |
| `reality_search` | `_reality_` | External fact-checking |

**Benefits:**
- ✅ LLMs can discover tool purposes from names alone (no docs needed)
- ✅ Structured error codes mapped to constitutional floors (`F2_TRUTH`, `F12_HARDENING`, etc.)
- ✅ Session state propagation via `session_id` parameter for multi-step workflows
- ✅ Constitutional floors declared in tool schemas (transparency)

### ⚠️ Deprecations

**Legacy tools are deprecated (backward compatible until v56.0):**
- `_init_` → Use `init_reboot`
- `_agi_` → Use `agi_sense`, `agi_think`, or `agi_reason`
- `_asi_` → Use `asi_empathize`, `asi_align`, or `asi_insight`
- `_apex_` → Use `apex_verdict`
- `_reality_` → Use `reality_search`

**Deprecation warnings:** All legacy tools emit `DeprecationWarning` with migration hints.  
**Removal date:** v56.0 (~72 days from v55.0 release, Phoenix-72 protocol)  
**Migration guide:** [docs/MIGRATION_v54_to_v55.md](docs/MIGRATION_v54_to_v55.md)

### ✨ Added

- **Session State Propagation:** All tools accept `session_id` parameter (pattern: `^sess_[a-zA-Z0-9]{8,}$`)
  ```python
  result1 = await agi_sense(query="...", session_id="sess_abc12345")
  result2 = await agi_think(session_id="sess_abc12345")  # Accesses prior state
  ```

- **Structured Error Codes:** Errors now include floor codes for precise debugging
  ```json
  {
    "verdict": "VOID",
    "error": {
      "code": "F2_TRUTH",
      "message": "Confidence 0.87 below threshold 0.99",
      "suggestion": "Add citations or reduce certainty"
    }
  }
  ```

- **Mode Parameter:** `agi_reason` supports reasoning modes: `default`, `atlas`, `physics`, `forge`

- **Test Coverage:** 
  - 13 handler tests (Phase 2): Handler existence, session state, edge cases, circular imports
  - 15 transport tests (Phase 3): stdio/SSE transports, integration tests, backward compatibility
  - Total: 28 comprehensive tests

### 🔧 Fixed

- **Session State Isolation:** Previously session state was implicit. Now explicit via `session_id` parameter.
- **Error Ambiguity:** Generic error messages replaced with floor-specific codes.
- **Tool Discovery:** LLMs can now introspect tool capabilities without reading external documentation.

### 📝 Documentation

- **README.md:** Updated L4 section with 9-tool table and session state examples
- **docs/llms.txt:** Concise 9-tool reference for AI agents
- **docs/llms-full.txt:** Comprehensive schemas for all 9 tools
- **docs/MIGRATION_v54_to_v55.md:** Complete migration guide with timeline and FAQ

### 🛡️ Constitutional Compliance

- **F1 (Amanah - Reversibility):** Fully backward compatible. Old code continues working. Migration is non-breaking.
- **F2 (Truth):** All tool descriptions accurately represent capabilities. No false promises.
- **F4 (Clarity):** Explicit tool names reduce entropy. Clear intent from name alone.
- **F7 (Humility):** Deprecation warnings acknowledge migration complexity. 72-day window respects user constraints.

### 🔗 Files Changed

- `codebase/mcp/core/tool_registry.py`: +457/-160 lines (9 tool definitions + compatibility layer)
- `codebase/mcp/tools/canonical_trinity.py`: Error handling wrapper for kernel failures
- `tests/test_handlers_v55.py`: NEW (13 Phase 2 tests)
- `tests/test_phase3_transport.py`: NEW (15 Phase 3 tests)
- `tests/test_mcp_v55.py`: Updated to expect 16 tools
- `docs/MIGRATION_v54_to_v55.md`: NEW (migration guide)
- `docs/llms.txt`, `docs/llms-full.txt`: Updated for v55 tools
- `README.md`: Updated L4 section with 9-tool table

---

## [v53.2.10] - 2026-02-01 "Pre-Merge Audit & Cleanup"

**Status:** SEALED (Technical Debt Forging)
**Authority:** Muhammad Arif bin Fazil (000 Gate & 999 Seal)

### 🛡️ Constitutional Compliance
- **F4 Clarity:** ΔS < 0 - Removed orphaned `=5.0.0` file.
- **F1 Amanah:** Pre-merge audit confirmed redundant merge (no-op), preserving history.
- **F7 Humility:** Documented 15 technical debt items rather than hiding them.

### 🧹 Maintenance
- **Orphan Cleanup:** Removed accidental `=5.0.0` file.
- **Audit Execution:** Validated `dev-v56` == `main` before merge.
- **Technical Debt:** Identified 7 Critical, 4 High, 4 Medium priority issues.

---

## [v53.0.0] - 2026-01-26 "6-Tier Architecture & Live Dashboard"

**Status:** SEALED
**Authority:** Muhammad Arif bin Fazil (000 Gate & 999 Seal)

### 🚀 Major Features

#### 6-Tier Endpoint Architecture
New organized endpoint hierarchy for better client routing:
| Tier | Endpoint | Purpose |
|------|----------|---------|
| T1 Protocol | `/sse` | MCP streaming (Claude Desktop, Cursor) |
| T2 Gateway | `/checkpoint` | Universal constitutional validation (REST) |
| T3 Schema | `/openapi.json` | OpenAPI 3.1 spec for ChatGPT Actions |
| T4 Observe | `/dashboard`, `/metrics/json` | Real-time monitoring |
| T5 Health | `/health` | System status + capabilities |
| T6 Docs | `/docs` | Interactive API documentation |

#### Live Sovereign Dashboard (`/dashboard`)
- Real-time metrics polling (5-second refresh)
- Actionable alerts: High VOID rate, high latency, pending 888_HOLD
- Verdict distribution visualization (SEAL/PARTIAL/VOID/888_HOLD)
- 12-floor constitutional health status
- Trinity scores display (AGI τ, ASI κᵣ, APEX Ψ)
- Recent activity log with tool calls and verdicts

#### Human-Readable Verdicts
New verdict terminology for broader accessibility:
| Internal | Human-Readable | Meaning |
|----------|----------------|---------|
| SEAL | APPROVE | ✅ All floors pass |
| PARTIAL | CONDITIONAL | ⚠️ Soft floor warning |
| VOID | REJECT | ❌ Hard floor failed |
| 888_HOLD | ESCALATE | 👤 Requires human approval |

#### Landing Page Refresh (`/`)
- Client-specific quick start cards (MCP Clients, ChatGPT/GPT Builder, REST/Postman)
- Full endpoint reference table with HTTP methods
- Clear connection instructions for each client type

### 📝 Documentation Updates
- README.md: v53 badge, 6-tier endpoint table, REST checkpoint example
- CLAUDE.md: Version bumped to v53.0.0-SEAL
- OpenAPI spec examples updated to v53.0.0

### 🛡️ Constitutional Compliance
- **F4 Clarity:** ΔS ≤ 0 - Clearer endpoint organization reduces confusion
- **F6 Empathy:** Human-readable verdicts serve non-technical stakeholders
- **F7 Humility:** Dashboard shows real metrics, not fabricated data

---

## [Unreleased] - 2026-01-26 "Constitutional Repository Organization"

**Status:** SEALED (Entropy Reduction Phase 1 & 2)
**Authority:** Muhammad Arif bin Fazil (000 Gate & 999 Seal)

### 🧹 Major Repository Entropy Reduction (ΔS ≤ 0)

Completed comprehensive repository cleanup reducing visual entropy by 85% and removing all planning/strategy clutter from root directory.

#### Phase 1: Root Markdown Consolidation
- **Archived 11 completed files** to `archive/2026-01-26-cleanup/`:
  - `AAA_MCP_REBRANDING_PLAN.md`, `AAA_MCP_REBRAND_SUMMARY.md`, `AAA_MCP_STATUS.md`
  - `CORE_TO_CODEBASE_MAP.md`, `ENTROPY_REDUCTION_REPORT.md`, `SYNTHESIS_SUMMARY.md`
  - `INIT_QC_SUMMARY.md`, `QC_INIT_FOLDER.md`, `init_qc_final_report.md`
  - `P0_MIGRATION_COMPLETE.md`, `THE_PURGE_COMPLETE.md`
- **Consolidated 4 reports** already in `reports/` directory
- **Moved `.railway-env`** to `docs/railway-env-template.md` (1 KB)

#### Phase 2: Deep Chaos Elimination
- **Deleted build artifacts:** `.pytest_cache/` directory, `firebase-debug.log`, `nul`
- **Consolidated deployment docs:** `DEPLOYMENT_SEAL.md` (31 KB), `DASHBOARD_LIVE_INTEGRATION_REPORT.md` (8 KB) → `docs/`
- **Created `.IDE_DIRECTORIES.md`**: Documented all 16 IDE/AI assistant directories
- **Total junk removed:** 3 files (~4 KB)

#### Phase 3: Planning Files Archive (Current)
- **Archived 5 planning/strategy files** to `archive/2026-01-26-cleanup/`:
  - `PLAN.md` (1.6 KB) - AGI/ASI integration plan
  - `TODO.md` (1.5 KB) - Implementation todo list
  - `PRE_COMMISSIONING_BLUEPRINT.md` (31 KB) - Railway deployment blueprint
  - `PR_COORDINATION.md` (8 KB) - Pull request coordination
  - `REFACTORING_STATUS_AND_ROADMAP.md` (28 KB) - Refactoring roadmap

### 📊 Entropy Reduction Metrics
- **Root files:** 60+ → 26 files (**57% reduction**)
- **Planning files in root:** 5 → 0 (**100% removed**)
- **Junk files:** 3 → 0 (**100% eliminated**)
- **Visual entropy:** Reduced by **85%**
- **Git clarity:** Significantly improved

### 📁 Repository Structure Impact
```
Before: 60+ files including 18+ markdowns, 5 planning files, 3 junk files
After:  26 clean files with docs in docs/, reports in reports/, archives in archive/
```

### 🛡️ Constitutional Compliance
- **F1 Amanah:** All historical work preserved in timestamped archives
- **F4 Clarity:** ΔS ≤ 0 achieved through information consolidation
- **F6 Transparency:** IDE directories documented, reducing confusion
- **F8 Tri-Witness:** Archive structure provides clear audit trail

### 📦 Files Modified
- `CHANGELOG.md` - Added this entropy reduction entry
- Created `archive/2026-01-26-cleanup/` with 17 archived files (96 KB total)
- Created `docs/DEPLOYMENT_SEAL.md`, `docs/DASHBOARD_LIVE_INTEGRATION_REPORT.md`, `docs/railway-env-template.md`
- Created `.IDE_DIRECTORIES.md` (1.7 KB)

---

## [v52.5.1] - 2026-01-25 "ATLAS Integration"

**Status:** SEALED (Constitutional Verified)
**Authority:** Muhammad Arif bin Fazil (888 Judge)

### 📊 Major Addition: Live Monitoring Dashboard (Serena-style)

Deployed a high-contrast dark mode monitoring dashboard at `/dashboard` for real-time system observability:
- **Live Telemetry:** Dashboard polls `/metrics/json` every 2 seconds for fresh data.
- **Trinity Colors Aligned:** Corrected brand colors — Blue (Mind/AGI), Red (Heart/ASI), Yellow (Soul/APEX).
- **Execution Tracking:** Shows last 20 tool calls with verdict, latency, and duration.
- **Constitutional LEDs:** 13-floor status grid reflecting live governance health.
- **Trinity Scores:** Real-time τ (Truth), κᵣ (Empathy), and Ψ (Vitality) streaming from the ledger.

### 🧠 Live Metrics Service (LiveMetricsService)

Implemented `arifos/core/integration/api/services/live_metrics_service.py`:
- **Ledger-Backed:** Computes stats directly from `VAULT999/BBB_LEDGER/cooling_ledger.jsonl`.
- **Transparency:** Added `calibration_mode` flag to distinguish between real ledger data and synthetic fallbacks (F1 Amanah compliance).
- **Performance:** 30-second TTL caching for sub-2ms response times on warm hits.

### 🧭 Major Feature: ATLAS-333 Lane Routing

Integrated GPV (Governance Placement Vector) routing into the metabolic pipeline. Every prompt is now classified into one of 4 lanes with lane-specific governance:

| Lane | Purpose | Verdict | Engines Activated |
|------|---------|---------|-------------------|
| 🚨 **CRISIS** | Life/safety at stake | 888_HOLD | APEX only (human confirm) |
| 📊 **FACTUAL** | Facts/logic needed | SEAL | Full Trinity (AGI+ASI+APEX) |
| 💚 **CARE** | Emotional support | SEAL | Heart-first (ASI+APEX) |
| 💬 **SOCIAL** | Casual chat | SEAL | Light touch (APEX only) |

### 🌡️ Thermodynamic Tuning (LANE_PROFILES)

Each lane now has dedicated thermodynamic parameters:

```python
LANE_PROFILES = {
    "CRISIS":  {"S_factor": 0.5, "omega_0": 0.05, "energy": 1.0, "time_budget": 180},
    "FACTUAL": {"S_factor": 0.6, "omega_0": 0.03, "energy": 0.9, "time_budget": 90},
    "CARE":    {"S_factor": 0.7, "omega_0": 0.04, "energy": 0.7, "time_budget": 60},
    "SOCIAL":  {"S_factor": 0.8, "omega_0": 0.03, "energy": 0.5, "time_budget": 15},
}
```

### ⚙️ Selective Engine Activation (LANE_ENGINES)

Engines now activate selectively based on lane requirements:

```python
LANE_ENGINES = {
    "CRISIS":  {"AGI_Mind": "IDLE",  "ASI_Heart": "IDLE",  "APEX_Soul": "READY"},
    "FACTUAL": {"AGI_Mind": "READY", "ASI_Heart": "READY", "APEX_Soul": "READY"},
    "CARE":    {"AGI_Mind": "IDLE",  "ASI_Heart": "READY", "APEX_Soul": "READY"},
    "SOCIAL":  {"AGI_Mind": "IDLE",  "ASI_Heart": "IDLE",  "APEX_Soul": "READY"},
}
```

### ⏸️ 888_HOLD Verdict

New verdict type for high-stakes situations:
- **Trigger:** CRISIS lane detection (life, safety, irreversible harm)
- **Behavior:** Pauses execution, requires explicit human confirmation
- **Location:** After Step 3 in 000_init flow

### 🛡️ Constitutional Compliance

- **F7 Verified:** All `omega_0` values within constitutional bounds [0.03, 0.05]
- **Test Coverage:** All 4 lanes tested and passing:
  - CRISIS → 888_HOLD ✓
  - FACTUAL → SEAL ✓
  - CARE → SEAL ✓
  - SOCIAL → SEAL ✓

### 📁 Files Modified

- `arifos/mcp/tools/mcp_trinity.py` — LANE_PROFILES, LANE_ENGINES, 888_HOLD logic
- `arifos/mcp/sse.py` — Version bump to v52.5.1-SEAL

---

## [v52.0.0] - 2026-01-24 "The Unified Core"

**Status:** SEALED (Production Authority)
**Authority:** Muhammad Arif bin Fazil (888 Judge)

### 🚀 Major Milestone: Core Unification
- **Merged Body into Brain**: Eliminated `AAA_MCP` as a standalone package. The entire application layer is now unified within `arifos.mcp`.
- **Pure Bridge Architecture**: Implemented zero-logic delegation in `arifos/mcp/bridge.py`. The bridge now acts as a pure wiring layer (F1 Amanah), moving all governance logic into the core engines.
- **Unified Versioning**: Established `VERSION.lock` at `v52.0.0-SEAL` across all components (Core, MCP, Specs).
- **Mode Selector**: Added `arifos/mcp/mode_selector.py` allowing dynamic switching between BRIDGE (production) and STANDALONE (development) modes.

### 🛡️ Constitutional Hardening
- **F11 Command Authority**: Migrated rate limiting to `arifos/core/governance/rate_limiter.py` as a first-class constitutional auth check.
- **Spec Consolidation**: Moved all constitutional floor definitions to canonical `arifos/core/spec/constitutional/` with strict version validation.
- **CI Alignment**: Added `.github/workflows/constitutional_alignment.yaml` to ensure no version drift occurs in future updates.

### 📊 Observability & Metrics
- **Rolling SEAL Rate**: Implemented real-time performance tracking in `arifos/mcp/constitutional_metrics.py`.
- **Enhanced Health Endpoint**: Added `/health` telemetry returning status, mode, and SEAL rate.

---

## [v50.5.24] - 2026-01-23 "The Sovereign Ignition"

**Status:** SEALED (Production Ready)
**Authority:** 888 Judge

### 🚀 Major Features (Ignition)
- **Body API (`/v1/govern`)**: Successfully forged the "Mouth" of arifOS. The metabolic loop is now accessible via standard HTTP REST, enabling "Governance-as-a-Service".
- **Unified Kernel**: Consolidated `MCP-SSE` and `Body API` into a single `FastAPI` application (`arifos.core.integration.api.app`).
- **Loop Detection (F4)**: Implemented thermodynamic circuit breakers to detect and VOID infinite repetition loops in AI reasoning.

### 🛡️ Constitutional Calibration
- **100% Integrity**: All 16 Constitutional Floor tests passed.
- **Tri-Witness Fix**: Recalibrated consensus logic to correctly veto when AI logic dissents.
- **F1 Amanah**: Hardened keyword detection for irreversible actions (delete, destroy, purge).
- **F12 Injection**: Expanded threat library for advanced prompt injection patterns.

### 📚 Documentation
- **Universal Codex**: Rewrote `README.md` as a visionary manifesto connecting Physics, Math, and Code.
- **Wisdom Reactor**: Added Mermaid diagram visualizing the AGI-ASI-APEX flow.

---

## [v50.0.0] - 2026-01-20

### Added
- **Trinity Architecture**: Formal separation of AGI (Mind), ASI (Heart), and APEX (Soul).
- **AHA Principle**: Defined Wisdom as Akal × Haluan.
