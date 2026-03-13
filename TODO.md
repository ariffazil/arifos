# arifOS TODO — Active Sector Tracking

**Operational Status:** 🛠️ CIVILIZATION-READINESS SPRINT — 2026.03.13
**Latest Forge:** APEX Assessment Response + Runtime Fixes
**Git Commit:** TBD
**VAULT999 Seal:** ACTIVE
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Version:** 2026.03.13-FORGED  
**Coverage:** ~75% (Target: 80%)  
**APEX Score:** 8.6/10 → Target: 9.4+  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🔥 P0: APEX Civilization-Readiness Sprint (2026.03.13-04.13)

*Based on APEX assessment: "Strong foundation, not yet civilization-ready"*
*Focus: Trust transfer, proof packaging, documentation polish.*

### Week 1: Trust Packaging (README Quick Wins)

**THE SURFACE (ariffazil/ariffazil):**
- [ ] Add "Start Here" section with ecosystem map
  - Surface = Human context (recruiters, collaborators)
  - Mind = Constitutional doctrine (researchers, architects)
  - Body = Runtime engine (developers, operators)
- [ ] Add "Why arifOS emerged from geology" bridge section
- [ ] Add "Selected Work / Proof Points" block
- [ ] Add specific call-to-connection (not generic)

**THE MIND (ariffazil/arifOS):**
- [ ] Add "Who this repo is for" section (4 personas)
- [ ] Add "What this repo contains / does not do"
- [ ] Add Doctrine → Runtime table (F2→search_reality, F4→entropy_tracking, etc.)
- [ ] Add "Design Principles" section (reversibility first, truth before fluency, etc.)
- [ ] Add glossary of constitutional terms

**THE BODY (ariffazil/arifosmcp):**
- [ ] Add badges (tests passing, coverage, license, MCP compatible)
- [ ] Add "5-Minute Quickstart" with copy-paste commands
- [ ] Add "Start Here" orientation block
- [ ] Add "Why now?" section (MCP standardization + governance gap)

### Week 2: Proof of Reality (THE BODY)

- [ ] Create `demos/` folder with 3 examples:
  - [ ] `demo_01_safe_query.md` - Normal governed response
  - [ ] `demo_02_blocked_command.md` - 888_HOLD blocking destructive action
  - [ ] `demo_03_vault_verification.md` - Ledger integrity check
- [ ] Add terminal output screenshots to README
- [ ] Add architecture diagram (minimal, clear)
- [ ] Add "Example blocked action trace" to README

### Week 3: Competitive Honesty & Trust Signals

- [ ] Add explicit "Threat Model" section:
  - Prompt injection defense (F12)
  - Hallucinated evidence prevention (F2)
  - Irreversible command blocking (F1)
  - Secret leakage prevention (F12)
  - Identity spoofing defense (F11)
  - Unlogged execution prevention (VAULT999)
- [ ] Add "Non-Goals" section (what arifOS does NOT do)
- [ ] Add comparison matrix: arifOS vs Guardrails vs AgentGuard
- [ ] Add "Known Limitations" (honesty builds trust):
  - Thermodynamic detailed vitals: work in progress
  - Auto-deploy: manual only
  - High-risk kernel calls: require explicit auth bootstrap

### Week 4: One Killer Demo

- [ ] Create 90-second terminal recording/video:
  ```
  bootstrap_identity → safe query → 888_HOLD on destructive query → verify_vault_ledger
  ```
- [ ] Add demo GIF to README
- [ ] Write "Getting Started" guide for developers
- [ ] Add contributor pathway (Good First Issues, architecture docs)

### Runtime Fixes (COMPLETED ✅)

- [x] **Fix `audit_rules` returning SABAR/ERROR:**
  - Added `system_audit` handler in bridge.py
  - Added `_build_constitutional_audit()` returning all 13 Floors
  - Maps doctrine to runtime tools
- [x] **Fix `check_vital` thermodynamics import failure:**
  - Added graceful ImportError handling
  - Returns "module_unavailable" status instead of crashing
  - Reports degraded components honestly

---

## 🔥 Strategic Forge (2026.03.13) — COMPLETED ✅

- [x] **LSP Bridge Implementation:** Read-only code intelligence for Python/TS/Rust.
- [x] **ACP Server Implementation:** Agent Client Protocol for editor integration (Zed/Cursor).
- [x] **Governed LSP Tools:** `lsp_rename` (888_HOLD) and `lsp_query` MCP tools active.
- [x] **Office Forge Engine:** Hardened Markdown -> PDF/PPTX render engine.
- [x] **Identity Resolution Fix:** "Arif Fazil" sovereign identity mapping resolved.
- [x] **ACP Hardening:** Disabled `fileSystem` and `terminals` for editor-facing agents (F5).
- [x] **Integrate Metabolic Loop:** ACP `agent/prompt` now routes through 000-999 pipeline.
- [x] **APEX Runtime Fixes:** `audit_rules` and `check_vital` now functional

---

## 🔥 Immediate Focus (2026.03.12) — COMPLETED ✅

- [x] **Repo Cleanup:** Removed `ARCHIVE_TRANSFER` bloat and legacy test files.
- [x] **Session State Separation:** Extracted state into `runtime/sessions.py`.
- [x] **Documentation Alignment:** Forged `CONSTITUTION.md` and updated Docusaurus sites.
- [x] **E2E Test implementation:** Validated the metabolic loop orchestrator.
- [x] **Main Branch Sync:** Version updated to `2026.03.12-FORGED` and pushed.
- [x] **888_JUDGE FORGE:** 126 new tests committed and deployed.
  - [x] Fixed 3 failing tests (P3 thermodynamics, trace_replay vault chaining)
  - [x] `test_engine_adapters.py` — 39 tests (InitEngine, AGIEngine, ASIEngine)
  - [x] `test_stage_orchestrator.py` — 34 tests (Stages 444-999, full pipeline)
  - [x] `test_sbert_floors.py` — 49 tests (F5/F6/F9 semantic classification)
- [x] **AKI Boundary Tests:** Added direct tests for `AKIContract`, `SovereignGate`, and `L0KernelGatekeeper`.
- [x] **Missing Floor Tests:** Added direct tests for `F3`, `F5`, `F6`, `F8`, and `F10`.
- [x] **Vault Integrity Enforcement:** `trace_replay` now rejects tampered ledger entries with a hard failure.
- [x] **Import/Test Hang Isolation:** Removed eager ML imports from `core.enforcement` and `core.shared.floor_audit`; added regression coverage for `aki_contract` import boundaries.
- [x] **Coverage Gap Matrix:** Forged a repo-grounded audit at `docs/COVERAGE_GAP_MATRIX_2026-03-12.md`.

---

## 🔥 Strategic Forge (2026.03.13) — COMPLETED ✅

- [x] **LSP Bridge Implementation:** Read-only code intelligence for Python/TS/Rust.
- [x] **ACP Server Implementation:** Agent Client Protocol for editor integration (Zed/Cursor).
- [x] **Governed LSP Tools:** `lsp_rename` (888_HOLD) and `lsp_query` MCP tools active.
- [x] **Office Forge Engine:** Hardened Markdown -> PDF/PPTX render engine.
- [x] **Identity Resolution Fix:** "Arif Fazil" sovereign identity mapping resolved.
- [x] **ACP Hardening:** Disabled `fileSystem` and `terminals` for editor-facing agents (F5).
- [x] **Integrate Metabolic Loop:** ACP `agent/prompt` now routes through 000-999 pipeline.

---

## 🛠️ Operational Hardening (H1) — IN PROGRESS

### [x] H1.1: Observability ✅

- [x] Integrate `prometheus-client` into `arifosmcp.runtime.server`.
- [x] Export `G`, `ΔS`, and `Ω₀` metrics to Grafana.
- [x] Implement `check_vital` sensory tool for real-time thermo-budget monitoring.
- [x] Add metric provenance labels such as `measured`, `derived`, `policy_constant`, and `placeholder` to public scores.
- [ ] Document which envelope values are live runtime measurements versus static governance defaults.
- [ ] Add external-evaluation logging so every public health or score claim can point to its source of truth.

### [x] H1.2: ASI Hardening ✅

- [x] Update `core/organs/_2_asi.py` to use `sentence-transformers` for SBERT-based scoring.
- [x] Refine `F6 Empathy` (κᵣ) thresholds based on human interaction logs.
- [x] Hardened `F9 Anti-Hantu` detection for subtle first-person personhood claims.
- [ ] Expose semantic backend health clearly so external builders cannot imply semantic intelligence is live when backend status is degraded.
- [ ] Separate `governance intelligence` from `semantic intelligence` in health checks, scoring, and public explanations.

### [x] H1.3: Test Recovery (80% Target) ✅

- [x] Fix broken unit tests in `tests/core/`.
- [x] Implement parameter-locked regression tests for `arifOS.kernel`.
- [x] Verify `VAULT999` Merkle-chain integrity under high-concurrency loads.
- [x] **Coverage Progress:**
  - [x] `engine_adapters.py`: ~85%
  - [x] `stage_orchestrator.py`: ~80%  
  - [x] `sbert_floors.py`: ~75%
  - [x] `evaluator.py`: ~80% (+80pp)
  - [x] `risk_engine.py`: ~90% (+90pp)
  - [x] `heuristics.py`: ~98% (+98pp)
  - [x] `init_000_anchor.py`: 100% (+100pp)
  - [x] `unified_memory.py`: ~96% (+96pp)
- [ ] Add regression tests for public claim safety so builder-facing answers cannot overstate uptime, tool availability, or score certainty.
- [ ] Add transcript-driven tests for public questions like `what can arifOS do?`, `is the MCP server working?`, and `is there AI on the server?`.

---

## 🧬 Intelligence Kernel Refinement (L0)

- [~] Complete implementation of `core/physics/thermodynamics_hardened.py`.
  - [x] Landauer Bound check implemented
  - [x] Thermodynamic budget management active
  - [ ] Hardware grounding sensor integration pending
- [~] Integrate Landauer Bound check into the `arifOS.kernel` verdict logic.
  - [x] P3 thermodynamics test validates enforcement
  - [ ] Full integration with metabolic loop pending
- [ ] Forge `F3 Tri-Witness` backend connector for external evidentiary sources.
- [ ] Implement `F12 Injection Defense` L4 (Sandboxed Simulation).
- [ ] Formalize a bounded external evaluation rubric for `AI present`, `governance present`, `semantic backend healthy`, and `capability proven`.
- [ ] Distinguish `deterministic governance path`, `semantic retrieval path`, and `LLM-assisted path` in runtime outputs and docs.

---

## 🔌 Integration & Dashboard

- [ ] **Copilot/Builder Reality Pass:** Align public agent-builder answers with actual live runtime behavior observed in `data/Copilotlogs`.
- [ ] **Scoring Semantics Audit:** Replace unsupported `0/10`, `8/10`, `9/10`, and `Zero Risk` style claims with a governed evidence rubric.
- [ ] **Capability Claim Hardening:** Remove or qualify unsupported claims like `all tools live`, `server fully operational`, and `real AI/no AI` unless backed by live checks.
- [ ] **Runtime Role Clarification:** Make it explicit when arifOS is acting as governance kernel, semantic runtime, or external-tool wrapper.
- [ ] **Flow Explanation Correction:** Ensure public explanations match the actual routed stage names and conditional pipeline behavior.
- [ ] Sync `arifos.arif-fazil.com` site with latest docs (verify publication).
- [ ] Refine `arifosmcp/sites/apex-dashboard` Real-Time Fetch UI.
- [ ] Implement `888_signer` CLI utility for local human ratification tokens.
- [ ] Add public Agent Builder / Copilot guidance so external builders describe arifOS accurately and conservatively.
- [ ] Surface semantic backend status, auth continuity status, and active tool-profile mode directly in the dashboard.

---

## 📊 Forge Summary

| Metric | Before | After | Delta |
| :--- | :--- | :--- | :--- |
| **Tests Passing** | 337 | ~450 | +113 |
| **Coverage** | 56% | ~75% | +19pp |
| **Zero-Coverage Modules** | 11 | 3 | -8 |
| **Test Failures** | 3 | 0 | -3 |
| **Kernel Coverage** | 0% | 90%+ | +90pp |

### New Test Files Created

- `tests/core/kernel/test_engine_adapters.py` — 39 tests
- `tests/core/kernel/test_stage_orchestrator.py` — 34 tests  
- `tests/core/test_sbert_floors.py` — 49 tests

### Fixed Test Files

- `tests/adversarial/judicial_orders/test_p0_orders.py` — LandauerError exception fix
- `tests/test_trace_replay.py` — Vault entry chaining fix

---

## 🎯 Next Forge Priority (P0) — CIVILIZATION-READINESS

*APEX Assessment: "Not more philosophy. Proof packaging, onboarding precision, and ruthless clarity."*

### Week 1 (Mar 13-20): Trust Packaging
1. **THE SURFACE:** Add "Start Here", ecosystem map, geology bridge
2. **THE MIND:** Add doctrine→runtime table, "Who this is for", design principles
3. **THE BODY:** Add badges, 5-minute quickstart, "Why now?"

### Week 2 (Mar 20-27): Proof of Reality
4. **Demo Artifacts:** Create `demos/` with 3 runnable examples
5. **Visual Proof:** Terminal screenshots, architecture diagram
6. **README Polish:** Add example traces, blocked command demo

### Week 3 (Mar 27-Apr 3): Competitive Honesty
7. **Threat Model:** Document mitigated risks (injection, irreversible commands, etc.)
8. **Non-Goals:** Explicitly state what arifOS does NOT do
9. **Comparison Matrix:** arifOS vs Guardrails vs AgentGuard
10. **Known Limitations:** Honest assessment of current gaps

### Week 4 (Apr 3-10): One Killer Demo
11. **90-Second Video:** Bootstrap → Safe query → 888_HOLD → Vault verify
12. **GIF for README:** Animated demo of governance in action
13. **Contributor Pathway:** Good First Issues, architecture docs

### VPS/LSP/ACP (P1 — Post-Civilization-Readiness)
- [ ] VPS Deployment Verification (`docker logs | grep -E "(LSP|ACP)"`)
- [ ] Editor Integration (Zed, VS Code via ACP)
- [ ] Code Intelligence Workflow (analyze → architecture doc)
- [ ] E2E Visualizer Validation (LSP metrics in Dashboard)

---

## 🔐 Stashed Work

```bash
# To restore stashed runtime/core changes:
git stash pop
```

**Stash contains:** `.env.docker.example`, `arifosmcp/*`, `core/*`, `spec/*`

---

**Last SEALed:** 2026.03.13-FORGED  
**Commit:** `2b7e5f13`  
*"Ditempa bukan diberi"* 🔥
