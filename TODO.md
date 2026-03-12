# arifOS TODO — Active Sector Tracking

**Operational Status:** ✅ FORGE DEPLOYED  
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Version:** 2026.03.12-FORGED  
**Coverage:** ~64% (Target: 80%)  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

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

### [~] H1.3: Test Recovery (80% Target) 🔄
- [x] Fix broken unit tests in `tests/core/`.
- [x] Implement parameter-locked regression tests for `arifOS.kernel`.
- [x] Verify `VAULT999` Merkle-chain integrity under high-concurrency loads.
- [~] **Coverage Progress:**
  - [x] `engine_adapters.py`: 0% → ~85% (+85pp)
  - [x] `stage_orchestrator.py`: 0% → ~80% (+80pp)  
  - [x] `sbert_floors.py`: 0% → ~75% (+75pp)
  - [ ] `evaluator.py`: 0% → target 80% (~25 tests needed)
  - [ ] `heuristics.py`: 0% → target 80% (~10 tests needed)
  - [ ] `init_000_anchor.py`: 0% → target 80% (~15 tests needed)
  - [ ] `risk_engine.py`: 0% → target 80% (~8 tests needed)
  - [ ] `unified_memory.py`: 0% → target 80% (~12 tests needed)
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
|--------|--------|-------|-------|
| **Tests Passing** | 337 | ~410 | +73 |
| **Coverage** | 56% | ~64% | +8pp |
| **Zero-Coverage Modules** | 11 | 6 | -5 |
| **Test Failures** | 3 | 0 | -3 |
| **Kernel Coverage** | 0% | 80%+ | +80pp |

### New Test Files Created
- `tests/core/kernel/test_engine_adapters.py` — 39 tests
- `tests/core/kernel/test_stage_orchestrator.py` — 34 tests  
- `tests/core/test_sbert_floors.py` — 49 tests

### Fixed Test Files
- `tests/adversarial/judicial_orders/test_p0_orders.py` — LandauerError exception fix
- `tests/test_trace_replay.py` — Vault entry chaining fix

---

## 🎯 Next Forge Priority (P0)

1. **Complete H1.3 Test Recovery** — Add ~70 tests for remaining 5 zero-coverage modules
2. **External Evaluation Rubric** — Standardized answers for capability claims
3. **Semantic Health Separation** — Distinguish governance vs semantic backend in health checks
4. **888_signer CLI** — Human ratification token utility

---

## 🔐 Stashed Work

```bash
# To restore stashed runtime/core changes:
git stash pop
```

**Stash contains:** `.env.docker.example`, `arifosmcp/*`, `core/*`, `spec/*`

---

**Last SEALed:** 2026.03.12-FORGED  
**Commit:** `966409d11`  
*"Ditempa bukan diberi"* 🔥
