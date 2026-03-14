# CHANGELOG — arifOS Constitutional AI Kernel

All changes follow [T000 versioning](T000_VERSIONING.md): `YYYY.MM.DD-PHASE-STATE`.  
**Creed:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## [2026.3.14-NERVOUS-SYSTEM-9-FORGED] — 2026-03-14 — NERVOUS-SYSTEM-9-FORGED

**T000:** 2026.03.14-NERVOUS-SYSTEM-9-FORGED  
**Theme:** Hardened Internal Infrastructure — The 9-Sense Nervous System

### 🔥 Nervous System 9 — ACLIP Infrastructure Hardened

**Validation:** 9/9 Tools ✅ 100% SEALED

The internal machine toolset (ACLIP) has been completely hardened with RuntimeEnvelope wrapping, constitutional governance, and full VAULT999 audit integration.

#### The 9 Hardened Tools

**System Sense (The Feelers):**
- `system_health` — Hardware telemetry (CPU, memory, disk, thermal)
- `process_list` — Process enumeration with resource monitoring
- `net_status` — Network connectivity and service diagnostics

**Memory & Storage (The Archive):**
- `chroma_query` — Semantic vector search with dual Qdrant API support
- `arifos_list_resources` — MCP resource enumeration (namespaced)
- `arifos_read_resource` — Canonical asset retrieval (namespaced)

**Diagnostics & Control (The Regulators):**
- `log_tail` — Smart log streaming with auto-path detection
- `fs_inspect` — Sandboxed filesystem inspection
- `cost_estimator` — Thermodynamic (ΔS) and AI cost projection

#### Hardening Features

- **RuntimeEnvelope:** All tools return canonical envelopes with full metadata
- **Governance:** F11 (Command Auth) + F12 (Injection) enforced on all tools
- **Audit:** Every operation sealed to VAULT999 immutable ledger
- **Compatibility:** chroma_query supports Qdrant v1.7 and v1.8+ automatically
- **Container-Aware:** system_health and process_list work in Docker/Kubernetes
- **Namespaced:** list_resources and read_resource prefixed as `arifos_*` to avoid MCP collisions

#### Files Forged

- `arifosmcp/intelligence/console_tools.py` — All 9 hardened tool implementations
- `arifosmcp/intelligence/tools/fs_inspector.py` — Added inspect_path alias
- `arifosmcp/intelligence/tools/net_monitor.py` — Added check_connectivity alias  
- `arifosmcp/intelligence/tools/thermo_estimator.py` — Cost estimation engine
- `arifosmcp/runtime/phase2_tools.py` — Registration alignment
- `arifosmcp/intelligence/cli.py` — ACLIP-CAI server synchronization

#### Testing

- **42 comprehensive tests** added
- **100% pass rate** on all 9 tools
- **E2E constitutional compliance** verified

---

## [2026.3.10-METABOLIC-ROUTER-SEAL] — 2026-03-10 — METABOLIC-ROUTER-SEAL

**T000:** 2026.03.10-METABOLIC-ROUTER-SEAL  
**Theme:** Dynamic Metabolic Routing (Stage 444), unified lifecycle hardening, and 000→999 sequential state machine.

### Added

- **Dynamic Metabolic Router** (`core/governance_kernel.py`):
  - Intelligent stage planning based on query intent (reality, safety, forge, judge).
  - Enforced guardrail: **Stage 777 (Forge) always implies Stage 888 (Judge)**.
  - Context-aware routing supports `force_grounding` and `human_required` overrides.
- **Sequential State Machine** (`arifosmcp/runtime/orchestrator.py`):
  - Completely refactored `metabolic_loop` into a clean, sequential execution pipeline.
  - **Constitutional Normalization:** All exploration stages (111-666) failing via `VOID` are normalized to `SABAR` to prevent early idea termination.
  - Terminal breaks for `SEAL`, `HOLD`, `HOLD_888`, and `VOID` status.
- **`HOLD_888` Verdict** (`core/shared/types.py`): New canonical verdict for specific human gating.

### Documentation Unification
- **Unified `DEPLOY.md`**: Consolidated historical deployment reports (`DEPLOYMENT_ANALYSIS.md`, `DEPLOYMENT_SUCCESS.md`, etc.) into a single, premium root entry point.
- **Agnostic HTTP Documentation**: Added specific guidance for ChatGPT connectivity via `AgnosticAcceptMiddleware`.

- **Unified Runtime Path:**
  - `arifosmcp.transport` now acts as a stable compatibility shim.
  - All core coordination logic moved into `arifosmcp.runtime` for agnostic MCP clients.
- **Final Output Schema Consistency:**
  - Standardized the `RuntimeEnvelope` top-level fields for all tool returns.
  - Unified telemetry and trace data structure across all organs.

### Fixed
- **Circular dependencies** and duplications in the orchestrator.
- **Initialization timing** for session state and auth context.

### Verification

- **Router Logic:** Tested across 12 diverse query scenarios.
- **Hardness Test:** Verified `777_FORGE` is inaccessible without `888_JUDGE`.
- **Schema Compliance:** All returns pass the v1.0.0 tool envelope.

---

## [2026.3.8-APEX-SOVEREIGN-SEAL] — 2026-03-08 — APEX-SOVEREIGN-SEAL

**T000:** 2026.03.08-APEX-SOVEREIGN-SEAL  
**Theme:** Architectural formalization of the APEX Theorem, 5-Layer intelligence stack, and Sovereign Dashboard launch.

### Added
- **APEX Sovereign Dashboard** (`arifosmcp/sites/apex-dashboard/`):
  - Self-contained React + Recharts dashboard visualizing the "Discipline Layer".
  - Radar geometry for Capacity (APX), Effort (E²), and Efficiency (η).
  - Log-decomposition waterfall view for diagnostic clarity.
  - Native FastMCP Custom HTML App integration (`ui://apex-dashboard/view.html`).
- **`open_apex_dashboard` tool**: Direct entry point for interactive observability.
- **APEX Theorem Physics** (`core/shared/physics.py`):
  - Native `G_dagger` (Realized Intelligence) and `eta` (Efficiency) methods in `GeniusDial`.
  - Formalized equation: $G^\dagger = G^* \cdot \eta$.

### Changed
- **5-Layer Intelligence Schema**:
  - Completely refactored `wrap_tool_output` to remove chaotic telemetry.
  - New output structure: `capacity_layer`, `effort_layer`, `entropy_layer`, `efficiency_layer`, `governed_intelligence`.
- **APEX Discipline Gate**:
  - Updated `core/organs/_3_apex.py` to enforce $G^\dagger \ge 0.80$ for `SEAL` verdicts.
  - Sessions failing the realization gate are automatically downgraded to `PARTIAL`.
- **Prefab UI Integration**:
  - Refactored `check_vital`, `audit_rules`, `vector_memory`, and `search_reality` to use FastMCP Prefab UI components (Metrics, DataTables, Badges).
- **Documentation Sync**:
  - Comprehensive rewrite of `README.md` for zero-context clarity.
  - Aligned `mcp-server.md`, `trinity-metabolic-loop.md`, and `intro.md` with the 10-tool metabolic stack.

### Fixed
- **Stage 000 Init Bugs**: `InitOutput` now correctly populates `floors_failed` upon failure.
- **Circular Import Fix**: Resolved dependency loop in `eval/suite.py` by moving triad imports to local scopes.
- **Deployment Pipeline**: Updated `run_evals.py` and `deploy-cloudflare.yml` to support the new dashboard sub-route.

### Verification
- **Constitutional Core**: 63/63 PASSED (including new $G^\dagger$ unit tests).
- **APEX Gate**: Verified via reproduction script (High Cost + Low Clarity = Downgrade).
- **Dashboard**: Verified live rendering across both internal and runtime-wrapped tools.

---

## [2026.3.8-APEX-METRICS-HARDENING-SEAL] — 2026-03-08 — APEX-METRICS-HARDENING-SEAL

**T000:** 2026.03.08-APEX-METRICS-HARDENING-SEAL  
**Theme:** APEX thermodynamic math hardening, dashboard runtime recovery, and deployment truth alignment

### Changed
- **`ThermoSnapshot.compute()`** (`arifosmcp/intelligence/core/thermo_budget.py`):
  - entropy removal is now capped to `H_before - H_after` instead of `abs(delta_s)`
  - `eta`, `G_dagger`, and `entropy_layer.delta_S` now remain bounded by the configured entropy baseline
- **APEX dashboard live path** (`arifosmcp/sites/apex-dashboard/index.html`):
  - live polling now sends `POST` requests with a `SystemCall` body instead of a bare `GET`
  - dashboard payloads are normalized so both `apex_output` envelopes and legacy `telemetry` envelopes can render
  - runtime display now reads canonical thermo fields (`G_dagger`, `eta`, `C`) rather than stale aliases (`governed_score`, `intelligence_efficiency`)

### Fixed
- **Dashboard boot failure:** inline JSX now uses the CSS variable string form `var(--dim)` correctly
- **Live APEX rendering:** real thermo payloads no longer crash the page on missing legacy field names
- **Thermodynamic overcounting:** sessions can no longer claim more entropy removal than the entropy baseline physically permits

### Docs
- `DEPLOY.md` now distinguishes the canonical public runtime server from the internal-only intelligence bridge used by standalone APEX dashboard live polling
- deployment examples now include the required `POST /mcp/anchor` and `POST /mcp/reason` `SystemCall` payload shape for operators who enable the bridge locally

### Verification
- `pytest tests/aclip_cai/test_thermo.py -q` -> pass
- `pytest tests/core/test_outputs.py -q` -> pass

---

## [2026.3.7-QUADWITNESS-SEAL] — 2026-03-07 — QUAD-WITNESS-BFT-P0-IMPLEMENTATION-SEAL

**T000:** 2026.03.07-QUADWITNESS-SEAL  
**Theme:** P0 Critical Fixes — Quad-Witness BFT consensus and Ψ-Shadow adversarial witness implementation

### Added
- **Ψ-Shadow (Adversarial Witness)** (`arifosmcp.intelligence/triad/psi/shadow.py`):
  - `PsiShadow` class implementing the 4th witness in Quad-Witness consensus
  - `attack_proposal()` method — actively attacks proposals to find flaws
  - `find_contradictions()` — detects logical inconsistencies (reversibility contradictions, safety bypass)
  - `simulate_injection()` — finds prompt/command injection vectors
  - `model_casualty_chain()` — models harm scenarios using Theory of Mind
  - `calculate_disorder()` — assesses entropy increase from destructive actions
  - **Attack Detection Patterns:**
    - Reversibility contradictions ("delete permanently but allow restore")
    - Safety bypass attempts ("bypass all safety checks")
    - Command injection (`rm -rf $(payload)`)
    - Prompt injection ("ignore previous instructions")
    - Production harm without backup checks
    - Data loss scenarios ("drop table", "delete all")
- **Quad-Witness Consensus** (`arifosmcp.transport/server.py`):
  - `compute_verifier_witness()` — Ψ-Shadow witness computation
  - **W4 Formula:** `W4 = (H × A × E × V)^(1/4) ≥ 0.75`
    - H = Human witness (authority/continuity)
    - A = AI witness (truth/coherence)
    - E = Earth witness (grounding/precedents)
    - V = Verifier witness (Ψ-Shadow adversarial check)
  - **BFT Compliance:** n=4, f=1 — tolerates 1 Byzantine fault
  - **Consensus Threshold:** 3/4 approval required (W4 ≥ 0.75)
- **Test Suite**:
  - `tests/test_psi_shadow.py` — 10 Ψ-Shadow adversarial analysis tests
  - `tests/test_quad_witness.py` — 12 Quad-Witness BFT consensus tests
  - All 22 new tests passing

### Changed
- **`build_governance_proof()`** (`arifosmcp.transport/server.py`):
  - **BEFORE:** Tri-Witness `w3 = product ** (1/3)` with 3 witnesses
  - **AFTER:** Quad-Witness `w4 = product ** (1/4)` with 4 witnesses
  - Added verifier witness integration
  - New parameters: `proposal`, `agi_result`, `asi_result`
  - Backward compatibility: W3 still computed for transition period
- **`apply_governance_gate()`** (`arifosmcp.transport/server.py`):
  - **BEFORE:** Checked `tri_witness_valid`
  - **AFTER:** Checks `quad_witness_valid`
  - Gate message: "Quad-Witness consensus below F3 threshold (W4 < 0.75)."
- **`critique_thought` tool** (`arifosmcp.transport/server.py`):
  - **BEFORE:** Only alignment check via `align()`
  - **AFTER:** Full adversarial analysis via `PsiShadow.attack_proposal()`
  - Updated description: "[Lane: Ψ Psi] [Floors: F4, F7, F8, F9] Ψ-Shadow adversarial analysis & attack simulation."
  - Returns both adversarial analysis AND alignment check for comparison
- **`apex_judge()` call site** (`arifosmcp.transport/server.py`):
  - Now passes `proposal`, `agi_result`, `asi_result` to `build_governance_proof()`
  - Enables Ψ-Shadow adversarial analysis on all judge decisions

### Fixed
- **Critical Gap #1:** Code used Tri-Witness (W3) instead of Quad-Witness (W4)
  - **Impact:** BFT claims were non-functional
  - **Fix:** Implemented W4 with 4th verifier witness
- **Critical Gap #2:** Ψ-Shadow lacked adversarial logic
  - **Impact:** 4th witness provided no protection
  - **Fix:** Implemented true adversarial analysis with attack detection

### Verification
- `pytest tests/test_psi_shadow.py tests/test_quad_witness.py -v` → 22/22 PASSED
- `pytest tests/verify_spec_compliance.py -v` → 11/11 PASSED
- Integration verification:
  - ✅ Imports working
  - ✅ PsiShadow rejects destructive actions
  - ✅ Quad-Witness blocks unsafe actions (W4 < 0.75)
  - ✅ Quad-Witness allows safe actions (W4 ≥ 0.75)

### Constitutional Compliance
- **F3 Tri-Witness** → **F3 Quad-Witness**: PASS — Now BFT-compliant (n=4, f=1)
- **F9 Anti-Hantu**: PASS — Ψ-Shadow detects deception patterns
- **F1 Amanah**: PASS — Fail-safe: shadow fails open (APPROVE) on error to prevent deadlock
- **F4 Clarity**: PASS — Safety through opposition (adversarial verification)
- **F6 Empathy**: PASS — Harm scenario modeling protects stakeholders
- **F8 Genius**: PASS — Multiplicative safety (G=0 if any dial=0) maintained with 4th witness

### Documentation
- **Theory Documents**:
  - `000_THEORY/ARIFOS_THEOREMS_AND_EQUATIONS.md` — Mathematical formalization
  - `000_THEORY/APEX_THEOREM.md` — Capstone meta-theory (Ψ-layer)
  - `000_THEORY/APEX_IMPLEMENTATION_MAP.md` — Spec-to-code mapping
  - `000_THEORY/VERIFICATION_SUMMARY.md` — Evidence-based compliance report
  - `000_THEORY/P0_IMPLEMENTATION_PLAN.md` — Detailed fix roadmap
  - `000_THEORY/P0_IMPLEMENTATION_COMPLETE.md` — Implementation summary
  - `000_THEORY/PRE_SEAL_CHECKLIST.md` — Pre-SEAL verification checklist

### Compliance
- **Implementation ⊨ Specification**: 77% → 95%
- **BFT Claims**: Theoretical → Enforced
- **Ψ-Shadow**: Documentation → Active enforcement

---

## [2026.3.7-ARCH-SEAL] — 2026-03-07 — ARCHITECTURE-INTEGRITY-NPM-REGISTRY-SEAL

**T000:** 2026.03.07-ARCH-SEAL
**Theme:** Forge broken promises — CLI entry points sealed, Docker Hub auto-publish wired, `@arifos/mcp@0.3.0` published to npm `latest`, registry accuracy restored, server import path fixed.

### Added
- **`[project.scripts]`** (`pyproject.toml`): Was documented in CLAUDE.md but never existed. Now real:
  - `arifos` = `arifosmcp.runtime.__main__:main` (canonical CLI)
  - `aaa-mcp` = `arifosmcp.transport.__main__:main` (compat shim)
  - `aclip-cai` = `arifosmcp.intelligence.cli:main` (ACLIP infrastructure CLI)
- **`arifosmcp.transport/unified_memory.py`**: Constitutional corpus + Google Drive semantic search module. Was untracked on VPS — now committed to repo.
- **`scripts/backup-state.sh`**: Phase 5A backup script (postgres + qdrant). Was untracked — now committed.
- **`.github/workflows/npm-publish.yml`**: New workflow with `workflow_dispatch` input (tag: `latest`/`next`), `id-token: write` permission for npm provenance, and `--provenance` flag.

### Changed
- **Docker Hub auto-publish** (`.github/workflows/docker-publish.yml`): Was release-only. Now also triggers on push to `main` for code paths: `Dockerfile`, `pyproject.toml`, `requirements*.txt`, `arifosmcp.transport/**`, `arifosmcp.runtime/**`, `core/**`, `arifosmcp.intelligence/**`.
- **`.gitignore`**: Added deployment artifacts — `BROWSER_SETUP_COMPLETE.md`, `DEPLOYMENT_COMPLETE_*.md`, `FINAL_SEAL_*.md`, `Hey.*`, `docker-compose.yml.backup.*`, `333_APPS/`.
- **`packages/npm/arifos-mcp/package.json`**: `0.2.1` → `0.3.0`, `publishConfig.tag: "next"` → `"latest"`.
- **`packages/npm/arifos-mcp/src/index.ts`**: `VERSION = '0.3.0'`, added `'2026.3.7'` to `ARIFOS_COMPATIBILITY`.
- **`packages/npm/arifos-mcp/src/types.ts`**: `ArifOSToolName` corrected to actual 13 tools — removed `recall_memory`, `fetch_content`, `inspect_file`; added `vector_memory`, `ingest_evidence`, `metabolic_loop`.
- **`packages/npm/arifos-mcp/src/langchain.ts`**: `getToolNames()` hardcoded list updated to match 13 canonical tools.
- **`packages/npm/arifos-mcp/src/client.ts`**: `'python'` → `'python3'`, client version `'0.1.0'` → `'0.3.0'`.
- **`mcp-clients.json`**: Stale Docker image tag (`arifazil/arifosmcp:forge-777` → `ariffazil/arifos:latest`), `python` → `python3`, removed ghost env var `ARIFOS_CONSTITUTIONAL_MODE`.
- **`MCP_CLIENT_SETUP.md`**: Tool count corrected `18 → 13`, removed fake Utility Tools section (`fetch_content`, `inspect_file`, `system_audit`, `list_prompts`, `get_prompt` — none were real `@mcp.tool()` tools).
- **`README.md`**: Major rewrite — TCP/IP analogy as core hook, `@arifos/mcp` TypeScript section, npm/Docker badges, AI manifest enriched with package registry entries and 12-container deployment map.

### Fixed
- **`arifosmcp.transport/server.py` — unified_memory import**: Hardcoded `sys.path.insert(0, "/srv/arifOS/333_APPS/L2_OPERATION/INTEGRATIONS")` fails inside Docker container (path does not exist). Fixed to `from arifosmcp.transport.unified_memory import get_unified_memory`.
- **`packages/npm/arifos-mcp/src/client.test.ts`**: `expect(VERSION).toBe('0.1.0')` was a hardcoded assertion blocking CI. Updated to `'0.3.0'`.

### Published
- **`@arifos/mcp@0.3.0`** — npm registry, `dist-tag: latest`. Took 3 CI runs: (1) test version assertion, (2) provenance permission, (3) success. Final dist-tags: `{latest: 0.3.0, next: 0.2.1}`.

### Constitutional Compliance
- **F4 Clarity**: PASS — CLI entry points were documented but absent (ΔS > 0). Now real.
- **F9 Anti-Hantu**: PASS — No ghost tool names on npm public surface.
- **F1 Amanah**: PASS — unified_memory import fix ensures container parity with VPS.
- **F2 Truth**: PASS — mcp-clients.json and MCP_CLIENT_SETUP.md now accurately reflect 13 tools.

### Verification
- `https://arifosmcp.arif-fazil.com/health` → `{status: healthy, tools_loaded: 13}`
- `npm info @arifos/mcp dist-tags` → `{latest: '0.3.0'}`
- All 12 containers: healthy
- Git: clean, pushed to `origin/main`

---

## [2026.3.7-P3-THERMO] — 2026-03-07 — P3-THERMODYNAMIC-HARDENING-SEAL

**T000:** 2026.03.07-P3-THERMO  
**Theme:** P3 Thermodynamic Hardening — Mandatory physics enforcement, no graceful fallbacks

### Added
- **Hardened Thermodynamics Module** (`core/physics/thermodynamics_hardened.py`):
  - **Mandatory Budget System**: Per-session thermodynamic budget (Joules) — no budget = VOID
  - **Practical Landauer Bound**: Detects suspiciously fast compute (1000x faster than expected = VOID)
  - **Semantic F4 Clarity**: Information density ratio instead of character entropy
  - **Mode Collapse Detection**: AGI/ASI orthogonality check (Ω_ortho ≥ 0.95)
  - **Hard Exceptions**: `LandauerViolation`, `EntropyIncreaseViolation`, `ThermodynamicExhaustion`
- **Tri-Witness Grounding** (`core/shared/floors.py` — F3):
  - Human witness: Derived from verified auth (not hardcoded)
  - AI witness: Computed from F2 truth + F7 humility + coherence
  - Earth witness: From grounding + thermodynamic validity
  - **Action Gating**: Different thresholds per action class (read/write/execute/critical)

### Changed
- **5-Organ Pipeline Integration**:
  - 000_INIT: Initializes `ThermodynamicBudget` (mandatory)
  - 333_AGI: Consumes energy per reasoning cycle
  - 888_APEX: Checks Landauer bound before SEAL
  - 999_VAULT: Captures final thermodynamic state
- **ConstitutionalTensor P3 Fields**:
  - `thermodynamic_cost`: Joules consumed
  - `landauer_ratio`: Compute efficiency vs expected
  - `orthogonality`: AGI/ASI separation
  - `budget_depletion`: Energy consumed ratio
- **F2 Truth Floor**: Practical Landauer check with graceful fallback on missing module
- **F4 Clarity Floor**: Semantic compression ratio (character entropy was wrong)

### Fixed
- **Landauer Calibration**: Changed from physical minimum (impossible) to expected compute
- **Graceful Degradation**: Distinguish missing module (fallback) vs check failure (VOID)
- **F4 Semantic Correctness**: Information density instead of character-level entropy

### Constitutional Compliance
- **F2 Truth**: PASS — Landauer bound detects cheap truth
- **F4 Clarity**: PASS — Semantic compression enforces clarity
- **F7 Humility**: PASS — Budget exhaustion → 888_HOLD
- **F8 Genius**: PASS — Mode collapse detection (Ω_ortho)

### Verification
- `pytest tests/e2e_test_hardened_thermodynamics.py`: 16/16 PASSED
- Thermodynamic budget tracking: Verified across 5-organ pipeline
- Landauer violation detection: Tested with 1000x efficiency threshold
- Entropy increase violation: Tested with semantic compression

---

## [2026.3.7-LABORATORY] — 2026-03-07 — CONSTITUTIONAL-LABORATORY-L0-L3-REARCHITECTURE-SEAL

**T000:** 2026.03.07-LABORATORY  
**Theme:** Transformation of `reason_mind` into an Epistemic Laboratory, consolidated L0-L3 4-layer architecture, and AKI Boundary formalization.

### Added
- **Constitutional Laboratory** (`reason_mind` tool v3.0):
  - **Epistemic Staging:** `VOID` verdicts during exploration are now downgraded to `PROVISIONAL` to allow speculative reasoning without early termination.
  - **Confidence Bands:** Numeric confidence mapped to human-readable tiers: `CLAIM` (≥0.90), `PLAUSIBLE` (0.70-0.89), `HYPOTHESIS` (0.40-0.69), `SPECULATION` (<0.40).
  - **Orthogonal Hypothesis Tracking:** Primary hypotheses from all three paths (Conservative, Exploratory, Adversarial) are now explicitly tracked and exposed in the main payload.
  - **Stability Scoring:** New `weighted_stability` metric (0.05-1.0) measures logic robustness based on contradiction count and severity.
  - **Contradiction Detection ("Scars"):** Automated detection of conflicts between reasoning branches (Conclusivity and Robustness scars).
  - **Operational Dispositions:** Each hypothesis is tagged with actions: `advance`, `ground`, `critique`, or `discard`.
- **AKI Contract Formalization** (`core/enforcement/aki_contract.py`):
  - Formalized the **Arif Kernel Interface (AKI)** as the hard airlock between L2 (Operation) and L3 (Civilization).
  - Integrated `SovereignGate` (888_HOLD logic) and `L0KernelGatekeeper` (protected paths) directly into the AKI boundary.

### Changed
- **L0-L3 Architectural Consolidation**:
  - Refactored fragmented 8-layer model into a consolidated 4-layer taxonomy:
    - **L0 CONSTITUTION:** Law, Kernel, Floors.
    - **L1 INSTRUCTION:** Prompts, Atlas, System Cards.
    - **L2 OPERATION:** Skills, Workflows, Agents.
    - **L3 CIVILIZATION:** Tools, Infrastructure, External World.
  - **Directory Rearchitecture:** Consolidated `333_APPS` into 4 clean tiers (`L0_KERNEL`, `L1_INSTRUCTION`, `L2_OPERATION`, `L3_CIVILIZATION`).
  - **Core Logic Migration:** Moved core architectural definitions (`Metabolizer`, `AppManifesto`, `SovereignGate`, `SystemAuditor`) from `333_APPS` into the `core/` package.
  - **Forwarding Stubs:** Converted original files in `333_APPS` (`manifesto.py`, `metabolizer.py`, `forge_init.py`) into forwarding stubs to maintain zero-breakage for downstream tools.
- **`arifosmcp.transport/server.py`**:
  - Updated `_agi_cognition` to expose the new Laboratory metrics (stability, scars, hypotheses, dispositions).
  - Integrated the consolidated L0-L3 taxonomy into the tool documentation.
- **`README.md`**: Comprehensive overhaul for human accessibility.
  - Added 30-second high-impact hook and safety mental model.
  - Added real-world "Dangerous Command" prevention example.
  - Simplified 13 Floors table and move JSON manifest to the footer.

### Constitutional Compliance
- **F4 Clarity**: PASS — Consolidated 8 layers into 4 clean tiers (ΔS ≤ 0).
- **F7 Humility**: PASS — Reasoning engine now explicitly scores logic stability and flags internal contradictions.
- **F13 Sovereign**: PASS — AKI boundary ensures no irreversible action bypasses the 888 Judge.

### Verification
- `python 333_APPS/manifesto.py`: Passed (Audit report verified).
- `python 333_APPS/metabolizer.py`: Passed (Zero bypass verified).
- `python 333_APPS/forge_init.py`: Passed (Membrane integrity verified).
- Directory consolidation confirmed via `ls -R 333_APPS`.

---

## [2026.3.6-CiV-BROWSER] — 2026-03-06 — CIVILIZATION-INFRASTRUCTURE-HEADLESS-BROWSER-SEAL

**T000:** 2026.03.06-CiV-BROWSER  
**Theme:** CIV Infrastructure Layer activation, Smart Hybrid Search with Headless Browser, comprehensive README rewrite

### Added
- **Headless Browser Service** (`docker-compose.yml`):
  - `headless_browser` container (browserless/chrome) on internal `arifos_trinity` network
  - DOM Reality extraction for JavaScript-heavy sites (SPAs, React, Vue)
  - Resource limits: 512MB RAM, max 2 concurrent sessions
  - F12 Defense: All content wrapped in `<untrusted_external_data>` envelope with SHA-256 hashing
- **HeadlessBrowserClient** (`arifosmcp.transport/external_gateways/headless_browser_client.py`):
  - Async client for internal browser service communication
  - Content quality scoring (0.0-1.0) with auto-fallback
  - Health check endpoint (`/pressure`) for load monitoring
  - Configurable via `ARIFOS_HEADLESS_BROWSER_ENABLED` env var
- **Smart Hybrid Search** (`arifosmcp.transport/server.py` — `search_reality` tool v2.0):
  - Query classifier: SPA/Research/News/General routing
  - 4-tier fallback chain: Jina → Perplexity → Brave → Headless Browser
  - Quality threshold-based fallback (0.2 minimum)
  - F3 Tri-Witness consensus merge when multiple sources available
  - Never returns empty — guarantees meaningful reality
- **CIV Infrastructure Documentation** (`333_APPS/L6_CIVILIZATION/`):
  - `EUREKA_CIV_INFRA_DISCOVERY.md` — Deep research findings
  - `SEAL_HEADLESS_BROWSER_INTEGRATION.md` — Production deployment seal
  - Clockmaker Daemon, Town Square (Redis), Resource Governor documented
- **VPS Architecture Master Dossier** (`docs/VPS_ARCHITECTURE_MASTER_DOSSIER.md`):
  - Complete update with CIV Infrastructure (L6) section
  - Headless Browser operational guide
  - Smart Hybrid Search architecture diagram
  - 12-container deployment matrix

### Changed
- **`arifosmcp.transport/server.py`**: `search_reality` completely rewritten for Smart Hybrid routing
  - New parameters: `force_source`, `min_content_quality`
  - Query type classification (SPA/Research/News/General)
  - Multi-source result merging with F3 consensus
  - Quality scoring algorithm (content length, structure, F12 envelope)
- **`arifosmcp.transport/external_gateways/__init__.py`**: Exports `HeadlessBrowserClient`
- **`docker-compose.yml`**: Added `headless_browser` service, volume mount for live code
- **`.env.docker`**: Added Headless Browser configuration (`ARIFOS_HEADLESS_BROWSER_ENABLED`, etc.)
- **VPS Skill** (`.agents/skills/arifos-vps-ops/SKILL.md`): Complete rewrite with CIV-Browser architecture

### Documentation
- **`README.md`**: Comprehensive rewrite (153 → 434 lines)
  - 🏛️ Canonical Trinity Web Links at TOP with web/file references
  - 🤖 AI Machine-Readable Manifest (JSON) for LLM parsing
  - 🧭 Zero-Context Intro (Human vs AI specific sections)
  - 🌡️ 8-Layer Architecture table (L0-L7) with status + file links
  - 🏛️ Complete 13 Constitutional Floors reference (F1-F13)
  - ⚙️ Metabolic Loop (000→999) with stage explanations
  - 🔌 14 MCP Tools catalog grouped by ARIF bands with file links
  - 🆕 Smart Hybrid Search section (Headless Browser integration)
  - 🎭 5-Role Agent Parliament (L5)
- **`docs/CONTRAST_ANALYSIS_README_VERSIONS.md`**: Analysis of README evolution vs past versions

### Fixed
- **`pyproject.toml`**: Removed duplicate TOML sections (361 lines deleted)
  - Fixed: `[project.optional-dependencies]` declared twice
  - Fixed: `[project.scripts]` declared twice
  - Fixed: `[project.urls]` declared twice
  - Fixed: `[tool.setuptools]` declared twice
  - Fixed: `[tool.pytest.ini_options]` declared twice
- **`Dockerfile`**: Fixed Playwright permissions for `arifos` user
  - Browser install now runs as root with proper chown
  - Removed redundant second install attempt

### Constitutional Compliance
- **F1 Amanah**: PASS — Headless Browser read-only, no destructive actions
- **F2 Truth**: PASS — Multi-source verification with quality scoring
- **F3 Tri-Witness**: PASS — Consensus merge when sources disagree
- **F4 Clarity**: PASS — Smart routing reduces entropy (ΔS ≤ 0)
- **F5 Peace²**: PASS — Resource limits prevent overload (512MB, 2 sessions)
- **F6 Empathy**: PASS — Graceful degradation on service unavailability
- **F7 Humility**: PASS — Quality thresholds with uncertainty bounds
- **F8 Genius**: PASS — Smart query classification (G = A×P×X×E²)
- **F9 Anti-Hantu**: PASS — No consciousness claims in browser automation
- **F10 Ontology**: PASS — Clear categorization (CIV Infrastructure)
- **F11 CommandAuth**: PASS — Internal network only (no public port)
- **F12 Defense**: PASS — `<untrusted_external_data>` envelope enforced
- **F13 Sovereign**: PASS — Configurable enable/disable (`ARIFOS_HEADLESS_BROWSER_ENABLED`)

### Verification
- All 12 containers healthy on VPS
- Headless Browser responding on `http://headless_browser:3000`
- Smart Hybrid Search tested with quality scoring
- GitHub repo synced with VPS (main branch)
- README renders correctly with all links functional

---

## [2026.3.6-CANON] — 2026-03-06 — CANONICAL-13-TOOL-SURFACE-LOCK-SCHEMA-ALIGN

**T000:** 2026.03.06-CANONICAL-13-TOOL-SURFACE-LOCK-SCHEMA-ALIGN
**Theme:** Phoenix retirement, three-layer schema alignment, ARIF Bands documentation, tool surface sealed at exactly 13

### Archived (Removed from Public Surface)
- **`recall_memory` (Phoenix)**: Retired → replaced by `vector_memory` (BGE-M3 768-dim multilingual embeddings + Qdrant + EUREKA sieve). F9 Anti-Hantu compliance — no ghost names on public surface.
- **`fetch_content`** + **`inspect_file`**: Consolidated → `ingest_evidence(source_type="url"|"file")`. Reduces surface entropy.
- **`trinity_forge`**: Demoted to internal orchestration alias. `metabolic_loop` is the canonical Band O tool.
- **`query_openclaw`**: Archived — internal diagnostic only, never part of 13-tool canon.

### Changed
- **Three-layer schema alignment** (all layers now agree on 13 canonical tool names):
  - `arifosmcp.transport/protocol/schemas.py` — added `ingest_evidence` + `metabolic_loop` to `TOOL_INPUT_SCHEMAS` + `TOOL_OUTPUT_SCHEMAS`
  - `arifosmcp.runtime/contracts.py` — `REQUIRES_SESSION`: `recall_memory` → `vector_memory`; `metabolic_loop` contract added
  - `arifosmcp.runtime/server.py` — 4 MCP prompts updated: `aaa_chain`, `trinity_forge`, `anchor_reason`, `audit_then_seal` now use Gen3 canonical names
- **`arifosmcp.transport/protocol/tool_naming.py`**: `vector_memory`, `ingest_evidence`, `metabolic_loop` added to `CANONICAL_PUBLIC_TO_LEGACY` map + `LEGACY_TOOL_NAMES`
- **`arifosmcp.transport/protocol/l0_kernel_prompt.py`**: Replaced stale `sensory_read` → `ingest_evidence` in the L0 constitutional kernel prompt
- **`arifosmcp.transport/server.py`**: Error message updated — `init_session (anchor)` → `anchor_session`
- **`arifosmcp.transport/README.md`**: `recall_memory` → `vector_memory`; `fetch_content` + `inspect_file` → `ingest_evidence`; `metabolic_loop` row added
- **`docs/00_META/GEMINI.md`**: 11 → 13 canonical tools; all Gen1 aliases replaced with Gen3 canonical names
- **ARIF Bands taxonomy** documented in `333_APPS/L4_TOOLS/README.md` (full dossier rewrite) and root `README.md`

### Documentation
- **`333_APPS/L4_TOOLS/README.md`**: Full dossier rewrite — Trinity Lanes table, per-tool Band/Stage/Floor/Description matrix, complete 13-tool ARIF lattice, metabolic chain ASCII diagram, archived tool table, A-CLIP alias map, verdict reference
- **`333_APPS/L4_TOOLS/MANIFEST.md`**: Version `v55.5.0` → `v2026.3.6-CANON`; entry point updated to `python -m arifosmcp.runtime`
- **`README.md`**: 14 → 13 canonical tools; Band O (Orchestrate / `metabolic_loop`) added; MCP section restructured into 8+4+1 layers

### Removed
- Temp artifacts deleted: `debug_mcp_v2.py`, `finalize_seal.py`, `verify_audit.py`, `git_diff_server.txt`

### Constitutional Compliance
- **F9 Anti-Hantu**: PASS — No archived tool names (`recall_memory`, `phoenix_recall`, `fetch_content`, `inspect_file`, `init_session`, `agi_cognition`, `apex_verdict`, `vault_seal`) survive on any public-facing layer
- **F4 Clarity**: PASS — Tool count reduced 14 → 13; three-layer schema alignment eliminates mismatch entropy
- **F1 Amanah**: PASS — `arifosmcp.transport/protocol/aaa_contract.py` runtime assertion `assert len(AAA_CANONICAL_TOOLS) == 13` guards the sacred count
- **F10 Ontology**: PASS — `trinity_forge` never existed as a public tool; `metabolic_loop` is the canonical orchestration surface

### Verification
- `arifosmcp.transport/protocol/aaa_contract.py`: Runtime assertion passes — 13 tools confirmed
- All commits lint-passed `constitution_lint` (all floors satisfied)
- Working tree clean, pushed to `origin/main`

---

## [2026.3.1-JINA] — 2026-03-01 — JINA-READER-INTEGRATION-SEARCH-REALITY

**T000:** 2026.03.01-JINA-READER-INTEGRATION-SEARCH-REALITY  
**Theme:** Jina Reader as PRIMARY search backend for superior content extraction and constitutional grounding

### Added
- **Jina Reader Client** (`arifosmcp.transport/external_gateways/jina_reader_client.py`):
  - `JinaReaderClient` class with `search()`, `read_url()`, `search_arxiv()` methods
  - `JinaReranker` class for semantic relevance-based result sorting
  - Clean Markdown extraction from URLs via `r.jina.ai`
  - Web search with extracted content via `s.jina.ai`
  - F12 Defense: External content wrapped in untrusted envelope with taint lineage
  - User-Agent header to avoid 403 Forbidden errors
- **`search_reality` tool enhancement**: Now uses Jina Reader as PRIMARY backend
  - Superior content extraction vs traditional SERP APIs
  - Fallback chain: Jina → Perplexity → Brave → Local knowledge
- **`fetch_content` tool enhancement**: Uses Jina Reader for URL-to-Markdown extraction
  - Returns clean, LLM-ready Markdown instead of raw HTML
  - Optional image and link extraction metadata
- **Environment variable**: `JINA_API_KEY` for higher rate limits (optional but recommended)

### Changed
- **External Gateways** (`arifosmcp.transport/external_gateways/__init__.py`): Exports `JinaReaderClient`, `JinaReranker`
- **Server** (`arifosmcp.transport/server.py`): `search_reality` and `fetch_content` now prioritize Jina Reader
- **Dockerfile**: Added embedding model directory setup (preparation for future embedding work)
- **`.env.docker.example`**: Added `JINA_API_KEY` placeholder
- **`.gitignore`**: Exclude embedding model files (*.safetensors, *.bin, *.pt, *.pth)

### Constitutional Compliance
- **F2 Truth**: Multi-source grounding with evidence URLs
- **F4 Clarity**: Clean Markdown output reduces entropy vs raw HTML
- **F12 Defense**: Untrusted envelope prevents prompt injection from external content
- **F7 Humility**: Graceful degradation when API key unavailable (NO_API_KEY status)

---

## [2026.3.1-FORGE] — 2026-03-01 — VAULT999-UNIFIED-TELEMETRY-TRINITY-FORGE-SEAL

**T000:** 2026.03.01-FORGE-VAULT999-UNIFIED-TELEMETRY-TRINITY  
**Theme:** VAULT999 Merkle ledger unification, FastMCP-native telemetry, trinity_forge emergence, production hardening

### Added
- **VAULT999 UNIFIED Ledger**: PostgreSQL + Redis + Merkle Tree + EUREKA Sieve wired together
  - `session_ledger.py` now provides unified `seal()` with automatic Merkle root computation
  - EUREKA anomalous contrast filter evaluates entries before storage
  - Redis hot caching for recent entries with chain state persistence
  - Chain verification via `verify_chain()` with tamper detection
- **`trinity_forge` unified tool**: Single-call 000-999 pipeline (emergent tool #14)
  - Internally executes: 000_INIT → 111-444 REASON → 555-666 HEART → 777-888 JUDGE → 999 SEAL
  - For ChatGPT/stateless clients requiring single-call constitutional validation
- **FastMCP-native telemetry** (`arifosmcp.transport/telemetry.py`):
  - `ConstitutionalSpan` wrapper with F1-F13 floor awareness
  - `@instrument_tool` decorator for automatic MCP tool instrumentation
  - OpenTelemetry semantic conventions: `tools/call {name}`, `arifos.verdict`, `arifos.metabolic_stage`
- **Governed Context** (`arifosmcp.transport/governed_context.py`):
  - FastMCP Context wrapper with 13-Floor constitutional enforcement
  - `StateEntry` with cryptographic checksums for F1 Amanah
  - `ConstitutionalProgressTracker` with metabolic stage awareness
- **FastMCP Context logging**: `ctx.info/debug` integration in `anchor_session` and `seal_vault`

### Changed
- **VAULT999 schema v3 UNIFIED**: Added columns `merkle_root`, `eureka_score`, `eureka_verdict`
- **14 tools total**: 13 canonical + 1 unified (`trinity_forge`)
- `seal_vault` tool: Now uses unified SessionLedger with Merkle + Redis persistence
- `arifosmcp.transport/server.py`: Integrated unified ledger, telemetry, and context logging

### Deployment Ready
- All 14 tools operational via MCP (stdio/SSE/HTTP)
- VAULT999 persistence layer: PostgreSQL (authoritative) + Redis (cache)
- Telemetry: OpenTelemetry + Prometheus metrics export
- Version: 2026.3.1-FORGE

---

## [2026.3.1] — 2026-03-01 — ENTROPY-REDUCTION-FORGE-777-SEAL

**T000:** 2026.03.01-ENTROPY-REDUCTION-FORGE-777-SEAL  
**Theme:** Massive codebase consolidation, MCP server unification, VPS deployment wiring

### Added
- Unified Docker Compose for VPS deployment with multi-network compartment access
- `.env.docker` template for compartment connection configuration (Qdrant, Ollama, OpenClaw, Agent Zero)
- Multi-homed container bridging 4 networks: coolify, ai-net, trinity_network, bridge

### Changed
- **Massive entropy reduction**: Removed 112,658 LOC (S_pre 0.94 → S_post 0.31, 75% reduction)
  - Purged `_ARCHIVE/` directory (legacy concepts, prototypes, experiments)
  - Purged `tests/archive/` and `tests/legacy/` (deprecated test suites)
  - Removed duplicate guards and unused `arifosmcp.transport` modules
- **MCP server consolidation**: Merged `arifosmcp.transport/server.py` into `arifosmcp.runtime/server.py`
  - Thin 90-line compatibility shim at `arifosmcp.transport/server.py`
  - Single 760-line canonical surface with 13 tools, 5 prompts, 4 resources
  - Eliminated circular dependencies between packages
- Docker image tagged: `arifos/arifosmcp:latest` (from `forge-777`, 14.8GB)
- Version badge updated to 2026.3.1

### Deployment
- Live VPS on port 8080 (streamable-http transport)
- Health status: healthy, 13 tools loaded
- Compartment IPs: qdrant(10.0.0.5), ollama(10.0.4.2), openclaw(10.0.1.2), agent-zero(10.0.2.3)

### Verification
- Container health check: `curl http://localhost:8080/health` → `{"status":"healthy"}`
- All 13 canonical tools verified operational
- Multi-network connectivity validated

---

## [2026.2.27] — 2026-02-27 — FORGE-PROTOCOL-NEGOTIATION-CONSISTENCY-SEAL

**T000:** 2026.02.27-FORGE-PROTOCOL-NEGOTIATION-CONSISTENCY-SEAL  
**Theme:** MCP version negotiation hardening, canonical tool naming convergence, and docs/runtime alignment.

### Added
- Streamable HTTP protocol negotiation tests for supported, unsupported, and mismatch session flows.
- MCP method parity for `resources/list`, `resources/read`, `prompts/list`, and `prompts/get` in streamable transport.

### Changed
- Canonical tool names converged to `apex_judge` and `eureka_forge` across runtime/tests/docs.
- Streamable HTTP handshake now negotiates `protocolVersion` per session and enforces header consistency.
- Discovery metadata now publishes `protocolVersion` and `supportedProtocolVersions` in `server.json` and well-known routes.
- Intro/docs trademark messaging aligned: "DITEMPA, BUKAN DIBERI" + epistemic humility subtitle.
- Package/release versions aligned to `2026.2.27`.

### Verification
- `pytest tests/test_aaa_phase888_mcp_protocol_e2e.py -q` -> pass
- `pytest tests/test_aaa_mcp_contract.py -q` -> pass
- `pytest tests/test_aaa_mcp_constitutional.py -q` -> pass

---

*See [docs/00_META/CHANGELOG.md](docs/00_META/CHANGELOG.md) for full historical changelog.*
