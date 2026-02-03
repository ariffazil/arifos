# arifOS Master TODO & Checklist

**Author:** Claude Opus 4.5 | **Date:** 2026-02-02 | **Status:** LIVING DOCUMENT
**Method:** Codebase audit + test execution + cross-reference with all research docs

---

## Scoring Legend

Every task is scored on 5 dimensions (1-5 scale):

| Dimension | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **Criticality** | Nice-to-have | System unsafe without it |
| **Timing** | Can wait 6+ months | Needed this week |
| **Energy** | Days of focused work | Hours or less |
| **Risk/Reward** | Low payoff, high risk | High payoff, low risk |
| **Resource Dependency** | Needs external services/people | Self-contained, just code |

**Composite Score** = (Criticality + Timing + Risk/Reward + Resource Independence) - Energy Cost

Higher score = do it first.

---

## TIER 1: DO NOW (Score 15+)

These are self-contained, high-impact, low-energy tasks with no external dependencies.

---

### T1.1 Enable ledger disk persistence ✅ COMPLETED

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 5 | "Immutable audit trail" is the #1 selling point; currently lost on restart |
| Timing | 5 | Blocks all compliance, audit, and trust claims |
| Energy | 5 | `immutable_ledger.py` already supports `persist_path` — just need to configure it as default |
| Risk/Reward | 5 | Near-zero risk (append-only file), massive reward (audit trail survives) |
| Resource Dep | 5 | Pure code change, no external services |
| **TOTAL** | **20** | |

**Fixed:** 2026-02-03

**Changes made:**
- ✅ Migrated from in-memory/json storage to **PostgreSQL** with Railway
- ✅ Created `HardenedPersistentVaultLedger` with SSL support for Railway TCP proxy
- ✅ Added `vault_merkle_state` table for Merkle tree persistence
- ✅ Vault survives server restart (`vault_backend: "postgres"` confirmed)
- ✅ Verified: `vault_seal` → restart → `vault_read` returns data

**Files:** `codebase/vault/persistent_ledger_hardened.py`, `codebase/vault/migrations/run_migrations.py`

**Status:** LIVE at aaamcp.arif-fazil.com — F3 Tri-Witness compliance achieved

---

### T1.2 Fix the 34 broken test files (import migration)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 5 | Can't detect regressions; system is flying blind |
| Timing | 5 | Blocks all future development confidence |
| Energy | 3 | 34 files, mostly search-and-replace `arifos.` -> `codebase.` but some may need deeper fixes |
| Risk/Reward | 5 | Zero risk (fixing imports), massive reward (test suite works) |
| Resource Dep | 5 | Pure code, no dependencies |
| **TOTAL** | **18** | |

**What to do:**
- [ ] `tests/conftest.py` — fix base imports
- [ ] `tests/utils.py` — fix utility imports
- [ ] Batch fix the 32 remaining test files (replace `from arifos.` with `from codebase.`)
- [ ] Run `pytest tests/ --ignore=tests/archive -v` and fix remaining failures
- [ ] Delete or quarantine tests that reference truly removed modules

**The 34 files (non-archive):**
```
tests/conftest.py
tests/utils.py
tests/constitutional/test_01_core_F1_to_F13.py
tests/constitutional/test_anti_hantu_f9.py
tests/constitutional/test_apex_room_888_pipeline.py
tests/constitutional/test_pipeline_000_to_999_comprehensive.py
tests/core/test_constitutional.py
tests/core/test_constitutional_compliant.py
tests/core/test_kernel_fixes_simple.py
tests/enforcement/test_f4_zlib_clarity.py
tests/enforcement/test_f9_negation_aware_v1.py
tests/enforcement/test_meta_select_integration.py
tests/enforcement/test_validate_response_full_integration.py
tests/evidence/test_atomic_ingestion.py
tests/evidence/test_conflict_routing.py
tests/evidence/test_evidence_pack.py
tests/governance/test_merkle_ledger.py
tests/governance/test_signatures.py
tests/integration/test_aaa_migration_cli.py
tests/integration/test_complete_mcp_constitutional.py
tests/integration/test_crash_recovery.py
tests/integration/test_loop_bootstrap.py
tests/mcp/test_mcp_999_seal.py
tests/mcp/test_mcp_connection.py
tests/mcp/test_metrics.py
tests/mcp/test_rate_limiter.py
tests/mcp/test_session_ledger.py
tests/memory/test_cooling_ledger.py
tests/memory/test_cooling_ledger_integrity.py
tests/memory/test_cooling_ledger_kms_integration.py
tests/memory/test_ledger_cryptography.py
tests/memory/test_memory_phase1_invariants.py
tests/memory/test_memory_phase1_routing.py
tests/safe_chatbot_demo.py
```

---

### T1.3 Fix ASI soft floor scoring (kappa_r = 0.0 bug) ✅ COMPLETED

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 4 | Benign queries get VOID; makes the system unusable for normal use |
| Timing | 5 | Discovered today via e2e test; blocks pipeline trust |
| Energy | 4 | Likely a default-value fix in ASI engine ("no harm" should score high, not 0.0) |
| Risk/Reward | 5 | Low risk (fixing a scoring default), high reward (pipeline works end-to-end) |
| Resource Dep | 5 | Pure code |
| **TOTAL** | **18** | |

**Fixed:** 2026-02-03

**Changes made:**
- ✅ In `codebase/asi/engine_hardened.py`:
  - Added **emotional distress detection** (25 keywords: stressed, anxious, worried, etc.)
  - `_identify_stakeholders`: Creates `distressed_user` stakeholder with vulnerability=0.9 when emotional keywords detected
  - `_compute_kappa_r`: Calculates empathy based on stakeholder vulnerability × power
- ✅ In `codebase/asi/kernel.py`: Fixed OmegaBundle attribute access (`.empathy.kappa_r` not `.empathy_kappa_r`)
- ✅ In `codebase/init/000_init/mcp_bridge.py`: Wired ASI engine into init_gate APEX calculation
  - Calls ASI during init to detect emotional state
  - Adjusts E (energy) based on κᵣ: `E = max(0.5, kappa_r)`
  - **Result:** Distressed users get E² = 0.81+ (was 0.49 fixed)

**Before/After:**
- Before: "I am stressed" → E = 0.7 (CARE lane) → E² = 0.49
- After: "I am stressed" → detects distress → κᵣ = 0.9 → E = 0.9 → E² = 0.81

**Files:** `codebase/asi/engine_hardened.py`, `codebase/asi/kernel.py`, `codebase/init/000_init/mcp_bridge.py`

---

## COMPLETED TODAY (2026-02-03) — MAJOR MILESTONE

### ✅ Hybrid MCP/REST API Deployed

**What:** Deployed constitutional observability endpoints alongside MCP protocol

**Endpoints LIVE:**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/floors.json` | GET | 13 Constitutional Floors schema |
| `/api/v1/init_gate` | POST | Session init with APEX scoring |
| `/api/v1/health` | GET | API health check |
| `/mcp` | POST | Model Context Protocol (primary) |
| `/health` | GET | System status |

**Why it matters:** AI agents use MCP. Humans debug with REST. Both speak to same constitution.

**Files:** `codebase/mcp/api_routes.py`, `codebase/mcp/transports/rest_api.py`

---

### ✅ 13 Constitutional Floors Implemented

**What:** All 13 floors (F1-F13) now have working validators

| Floor | Status | Function |
|-------|--------|----------|
| F1 Amanah | ✅ | Reversibility audit |
| F2 Truth | ✅ | Information fidelity |
| F3 Tri-Witness | ✅ | Human × AI × Earth consensus |
| F4 Empathy | ✅ | Stakeholder care (κᵣ) |
| F5 Peace² | ✅ | Non-destructive power |
| F6 Clarity | ✅ | Entropy reduction |
| F7 Humility | ✅ | Uncertainty band |
| F8 Genius | ✅ | G = A × P × X × E² |
| F9 Anti-Hantu | ✅ | Consciousness claim prohibition |
| F10 Ontology | ✅ | Category lock |
| F11 CommandAuth | ✅ | Identity verification |
| F12 Injection | ✅ | Prompt injection defense |
| F13 Sovereign | ✅ | Human final authority |

**Files:** `codebase/constitutional_floors.py`

---

### ✅ init_gate Hardened

**What:** Real Ed25519 cryptography + 7-step ignition

**Features:**
- Real root key generation (`~/.arifos/root_key.ed25519`)
- Memory fetch from 7 sources (3 domains)
- F12 injection scanning
- APEX collapse: G = A × P × X × E²
- Returns: motto, seal, apex_summary with 13 floors

**Motto:** DITEMPA BUKAN DIBERI 💎🔥🧠

**Files:** `codebase/init/000_init/mcp_bridge.py`

---

## TIER 2: DO THIS WEEK (Score 12-14)

High-value tasks that require moderate effort but have clear payoff.

---

### T2.1 Wire stages 444-999 into the MCP pipeline

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 3 | Stages exist and work; they're just not called from MCP entry points |
| Timing | 4 | Needed for "metabolic loop" claim to be real |
| Energy | 3 | Stage files are real implementations (not stubs); need to wire into `mcp_trinity` or pipeline |
| Risk/Reward | 4 | Medium risk (integration bugs), high reward (full pipeline) |
| Resource Dep | 5 | Pure code |
| **TOTAL** | **14** | |

**What to do:**
- [ ] Map which MCP tool calls which stage:
  - `agi_reason` -> stages 111-333 (already done)
  - `asi_empathize` -> stage 555 (`stage_555.py`) — wire if not connected
  - `asi_align` -> stage 666 (`stage_666.py`) — wire if not connected
  - `apex_verdict` -> stage 888 (`stage_888_judge.py`) — wire if not connected
  - `vault_seal` -> stage 999 (`stage_999_seal.py`) — wire if not connected
- [ ] Add integration test: call all 9 tools in sequence, verify stage progression
- [ ] Verify stage 444 trinity sync is triggered between AGI and ASI

**Files:** `codebase/stages/`, `codebase/mcp/tools/canonical_trinity.py`, `codebase/mcp/core/bridge.py`

---

### T2.2 Add /health endpoint ✅ COMPLETED

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 3 | No observability currently; can't tell if system is healthy |
| Timing | 3 | Needed for any deployment (Kubernetes probes, monitoring) |
| Energy | 4 | Small endpoint returning JSON: floor status, tool count, ledger depth, uptime |
| Risk/Reward | 5 | Zero risk, high operational reward |
| Resource Dep | 5 | Pure code |
| **TOTAL** | **14** | |

**Fixed:** 2026-02-03

**Changes made:**
- ✅ Health endpoint already existed in `sse.py`
- ✅ Enhanced with version info: `v55.2-AAA`
- ✅ Returns: `{status: "GREEN", version: "v55.2-AAA", tools: 9, ...}`
- ✅ Added `/api/v1/health` REST endpoint for API v1 namespace

**Test:** `curl https://aaamcp.arif-fazil.com/health`

**Files:** `codebase/mcp/transports/sse.py`, `codebase/mcp/api_routes.py`

---

### T2.3 Clean archived tests

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | Noise, not danger; but confuses `pytest` collection |
| Timing | 3 | Should do alongside T1.2 (import fix) |
| Energy | 5 | Just move or add `conftest.py` with `collect_ignore` |
| Risk/Reward | 4 | Zero risk, moderate reward (cleaner test runs) |
| Resource Dep | 5 | Pure file ops |
| **TOTAL** | **13** | |

**What to do:**
- [ ] Add `tests/archive/conftest.py` with `collect_ignore_glob = ["*"]` to skip all archived tests
- [ ] Or move `tests/archive/` to `archive/tests_legacy/` (out of pytest path)
- [ ] Verify `pytest tests/ -v` no longer collects archived tests

---

### T2.4 Create JSON schema directory

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | README references `schemas/` directory but it doesn't exist |
| Timing | 3 | Documentation claims it exists |
| Energy | 4 | Extract schemas from `tool_registry.py` into standalone `.json` files |
| Risk/Reward | 4 | Low risk, enables external validation and llms.txt accuracy |
| Resource Dep | 5 | Pure code |
| **TOTAL** | **12** | |

**What to do:**
- [ ] Create `schemas/` directory
- [ ] Export each tool's `input_schema` and `output_schema` to `schemas/{tool_name}.input.json` and `schemas/{tool_name}.output.json`
- [ ] Add script or test to verify schemas match registry definitions
- [ ] Update `docs/llms-full.txt` to reference schema files

---

## TIER 3: DO THIS MONTH (Score 8-11)

Important but not urgent. Require more energy or have dependencies.

---

### T3.1 Implement one real L5 agent (Architect)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 3 | Proves the L5 design; currently all stubs |
| Timing | 2 | Not blocking anything immediate |
| Energy | 2 | Significant work: wire agent to MCP tools, implement sense/think/act methods |
| Risk/Reward | 4 | Medium risk, high reward (validates multi-agent architecture) |
| Resource Dep | 4 | Depends on T1.3 (ASI fix) and T2.1 (pipeline wiring) |
| **TOTAL** | **11** | |

**What to do:**
- [ ] Choose Architect (Delta) agent in `333_APPS/L5_AGENTS/agents/architect.py`
- [ ] Implement `sense()`: call `agi_sense` via canonical handler
- [ ] Implement `think()`: call `agi_think` and return hypotheses
- [ ] Implement `plan()`: call `agi_reason` with mode="atlas"
- [ ] Implement `validate()`: call `apex_verdict`
- [ ] Add integration test: Architect processes a real query end-to-end
- [ ] Document agent capabilities in L5 README

**Depends on:** T1.3, T2.1

---

### T3.2 EU AI Act compliance pack v1

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 3 | Aug 2026 deadline for high-risk system requirements |
| Timing | 3 | 6 months out, but templates take time |
| Energy | 2 | Research-heavy: risk taxonomy, QMS templates, audit export format |
| Risk/Reward | 4 | Low technical risk, high market reward |
| Resource Dep | 3 | May need legal review for accuracy |
| **TOTAL** | **11** | |

**What to do:**
- [ ] Create `compliance/` directory
- [ ] Map each MCP tool to EU AI Act risk categories
- [ ] Create DPIA (Data Protection Impact Assessment) template
- [ ] Create QMS (Quality Management System) template skeleton
- [ ] Add `/compliance` endpoint returning risk classification + audit status
- [ ] Add vault_seal export in EU-compatible audit format (JSON-LD or CSV)

---

### T3.3 Sidecar deployment pattern (Kubernetes)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | Not needed for development; needed for enterprise adoption |
| Timing | 2 | Q2-Q3 2026 target |
| Energy | 3 | Helm chart, sidecar container spec, proxy configuration |
| Risk/Reward | 4 | Low risk (packaging), high reward (enterprise deployment story) |
| Resource Dep | 3 | Needs Kubernetes cluster for testing |
| **TOTAL** | **10** | |

**What to do:**
- [ ] Create `deploy/kubernetes/` directory
- [ ] Write Helm chart with arifOS as sidecar container
- [ ] Define sidecar intercept pattern: request -> arifOS -> LLM -> arifOS -> response
- [ ] Add health/readiness probes using T2.2 /health endpoint
- [ ] Document deployment in `deploy/README.md`
- [ ] Test with minikube or kind

**Depends on:** T2.2 (/health endpoint)

---

### T3.4 Update llms.txt files to v55.2

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | AI agents use these for tool discovery |
| Timing | 2 | Should reflect current 9-tool canon |
| Energy | 4 | Regenerate from tool_registry.py definitions |
| Risk/Reward | 4 | Zero risk, helps AI integration |
| Resource Dep | 5 | Pure content |
| **TOTAL** | **10** | |

**What to do:**
- [ ] Regenerate `docs/llms.txt` from current 9 tools
- [ ] Regenerate `docs/llms-full.txt` with full schemas
- [ ] Remove `docs/llms-full-v54-backup.txt`
- [ ] Add generation script to avoid future drift

---

### T3.5 Fix `datetime.utcnow()` deprecation warnings

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 1 | Warnings only, not errors; but Python 3.14 will remove it |
| Timing | 2 | Running on Python 3.14 already, so it's noisy |
| Energy | 5 | Global search-replace: `datetime.utcnow()` -> `datetime.now(datetime.UTC)` |
| Risk/Reward | 4 | Zero risk, cleaner output |
| Resource Dep | 5 | Pure code |
| **TOTAL** | **9** | |

**What to do:**
- [ ] Find all `datetime.utcnow()` calls in `codebase/`
- [ ] Replace with `datetime.now(datetime.UTC)`
- [ ] Verify tests still pass

---

## TIER 4: DO THIS QUARTER (Score 5-7)

Strategic items that require significant energy, external dependencies, or prerequisites.

---

### T4.1 Model-agnostic adapters (OpenAI, Gemini, Claude)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | Currently works via MCP; adapters would enable direct API wrapping |
| Timing | 2 | Q2 2026 |
| Energy | 2 | Each adapter needs auth, request mapping, response normalization |
| Risk/Reward | 3 | Medium risk (API changes), medium reward (broader adoption) |
| Resource Dep | 2 | Needs API keys for testing |
| **TOTAL** | **7** | |

---

### T4.2 Agent Firewall (kill-switch, cost caps)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 2 | Important for enterprise trust; not critical for dev |
| Timing | 2 | Q3 2026 |
| Energy | 2 | Policy engine design, cost tracking, rate limiting |
| Risk/Reward | 3 | Medium risk, high enterprise reward |
| Resource Dep | 3 | Depends on T3.1 (working agents) |
| **TOTAL** | **7** | |

---

### T4.3 Academic paper: Thermodynamic Governance

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 1 | Credibility, not functionality |
| Timing | 1 | No deadline |
| Energy | 1 | Weeks of writing + formal proofs |
| Risk/Reward | 3 | High reward (citations, credibility), low technical risk |
| Resource Dep | 2 | May need academic collaborators |
| **TOTAL** | **6** | |

---

### T4.4 SSO integration (SAML, OIDC)

| Dimension | Score | Reason |
|-----------|-------|--------|
| Criticality | 1 | Enterprise feature, not needed for core |
| Timing | 1 | v57+ |
| Energy | 2 | Library integration (authlib, python-jose) |
| Risk/Reward | 3 | Low risk, high enterprise value |
| Resource Dep | 2 | Needs IdP for testing |
| **TOTAL** | **5** | |

---

## TIER 5: NOT YET (Score < 5 or Blocked)

These items are blocked by prerequisites or too speculative for current planning.

| Task | Blocked By | Score | Notes |
|------|-----------|-------|-------|
| DAO governance | No persistent storage, no users | 2 | v59+ at earliest |
| WASM edge deployment | Core pipeline incomplete | 3 | v58+ |
| Agent marketplace | Zero working agents | 2 | v57+ at earliest |
| Blockchain anchoring | Ledger persistence not proven in production | 2 | Research only |
| 20-agent swarm | L5 agents are stubs | 1 | v57+ |
| Recursive Constitutional Improvement | Pure research; needs formal proofs | 1 | v60+ |
| Multi-model Tri-Witness | Needs agents, needs adapters | 2 | v58+ |
| Hardware Security Module (SGX/Nitro) | Needs enterprise deployment first | 2 | v58+ |
| Negentropy Markets | Theoretical concept only | 0 | Research paper first |

---

## Execution Order (The Critical Path)

```
WEEK 1:
  [T1.1] Enable ledger persistence ──────────────────── 2-3 hours
  [T1.3] Fix ASI kappa_r scoring bug ────────────────── 1-2 hours
  [T2.3] Clean archived tests ───────────────────────── 30 minutes

WEEK 2:
  [T1.2] Fix 34 broken test imports ─────────────────── 4-8 hours
         (batch: conftest.py first, then the 32 files)

WEEK 3:
  [T2.1] Wire stages 444-999 into pipeline ──────────── 4-6 hours
  [T2.2] Add /health endpoint ───────────────────────── 2-3 hours
  [T3.5] Fix datetime.utcnow() warnings ────────────── 1 hour

WEEK 4:
  [T2.4] Create JSON schema directory ───────────────── 2-3 hours
  [T3.4] Update llms.txt to v55.2 ──────────────────── 1-2 hours

MONTH 2:
  [T3.1] Implement Architect agent (first real L5) ──── 1-2 weeks
  [T3.2] EU AI Act compliance pack v1 ──────────────── 1-2 weeks

MONTH 3:
  [T3.3] Sidecar deployment (Kubernetes) ────────────── 1 week

QUARTER 2+:
  [T4.1-T4.4] Strategic expansion items
```

---

## Dependency Graph

```
T1.1 (Ledger Persistence)
 └─> T3.3 (Kubernetes deploy — needs health + persistence)
 └─> T4.3 (Academic paper — needs verifiable audit trail)

T1.2 (Fix Test Imports)
 └─> ALL FUTURE WORK (can't trust anything without tests)

T1.3 (Fix ASI Scoring)
 └─> T2.1 (Pipeline wiring — pipeline should SEAL benign queries)
 └─> T3.1 (L5 Agent — agents need working engines underneath)

T2.1 (Wire Stages)
 └─> T3.1 (L5 Agent — agents orchestrate stages)

T2.2 (/health endpoint)
 └─> T3.3 (Kubernetes — needs health probes)
 └─> T3.2 (Compliance — needs status reporting)

T3.1 (First L5 Agent)
 └─> T4.2 (Agent Firewall — needs agents to govern)
 └─> T4.1 (Model Adapters — agents need to call different LLMs)
```

---

## Corrections to Prior Research

While building this TODO, I found corrections to the Claude deep research:

| Claim (Deep Research) | Correction (Verified Today) |
|----------------------|---------------------------|
| "Ledger is in-memory only" | `immutable_ledger.py` supports `persist_path` for disk writes; just not configured as default |
| "Stages 444-999 have partial implementation" | Stages 444-999 are **full implementations** (67-180 LOC each); they're just not wired into MCP tools |
| "~60% of tests fail" | Exactly **34 test files** (non-archive) need import migration |
| "No CI/CD" | **14 GitHub Actions workflows** exist including CI, secrets scan, and publish |

---

## How to Use This Document

1. **Pick the top unchecked item in Tier 1** and do it
2. **Check the box** when done
3. **Run `pytest tests/test_pipeline_e2e.py -v`** after each change to verify nothing broke
4. **Move to Tier 2** only when all Tier 1 items are checked
5. **Update this document** as tasks complete or new tasks emerge

---

**Authority:** Muhammad Arif bin Fazil
**Creed:** DITEMPA BUKAN DIBERI
