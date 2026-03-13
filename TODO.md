# arifOS TODO — Active Sector Tracking

**Operational Status:** ✅ LSP/ACP SEALED TO VAULT999 — 2026.03.13
**Latest Forge:** LSP + ACP Constitutional Integration v1.0
**Git Commit:** 36713d5ce
**VAULT999 Seal:** ACTIVE
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Version:** 2026.03.13-FORGED  
**Coverage:** ~75% (Target: 80%)  
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

## 🎯 Next Forge Priority (P0) — POST-LSP/ACP

1. **VPS Deployment Verification** — Confirm LSP/ACP live on production (`docker logs | grep -E "(LSP|ACP)"`).
2. **Editor Integration** — Connect Zed, VS Code, Antigravity, OpenCode to arifOS via ACP.
3. **Code Intelligence Workflow** — Build "analyze codebase → generate architecture doc" pipeline.
4. **E2E Visualizer Validation** — Verify LSP metrics show up in Constitutional Dashboard.
5. [x] **888_signer CLI** — Human ratification token utility for ACP session approval ✅
6. [x] **Complete H1.3 Test Recovery** — Add ~110 tests for zero-coverage modules ✅

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
