# arifOS TODO — Active Sector Tracking

**Operational Status:** 🔴 ACTIVE FORGE  
**Authority:** 888 Judge — Muhammad Arif bin Fazil  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🔥 Immediate Focus (2026.03.11)

- [x] **Repo Cleanup:** Removed `ARCHIVE_TRANSFER` bloat and legacy test files.
- [x] **Session State Separation:** Extracted state into `runtime/sessions.py`.
- [x] **Documentation Alignment:** Forged `CONSTITUTION.md` and updated Docusaurus sites.
- [x] **E2E Test implementation:** Validated the metabolic loop orchestrator.
- [x] **Main Branch Sync:** Version updated to `2026.03.09-SEAL` and pushed.
- [ ] **Copilot/Builder Reality Pass:** Align public agent-builder answers with actual live runtime behavior observed in `data/Copilotlogs`.
- [ ] **Scoring Semantics Audit:** Replace unsupported `0/10`, `8/10`, `9/10`, and `Zero Risk` style claims with a governed evidence rubric.
- [ ] **Capability Claim Hardening:** Remove or qualify unsupported claims like `all tools live`, `server fully operational`, and `real AI/no AI` unless backed by live checks.
- [ ] **Runtime Role Clarification:** Make it explicit when arifOS is acting as governance kernel, semantic runtime, or external-tool wrapper.
- [ ] **Flow Explanation Correction:** Ensure public explanations match the actual routed stage names and conditional pipeline behavior.
- [x] **Coverage Gap Matrix:** Forged a repo-grounded audit at `docs/COVERAGE_GAP_MATRIX_2026-03-12.md`.
- [x] **AKI Boundary Tests:** Added direct tests for `AKIContract`, `SovereignGate`, and `L0KernelGatekeeper`.
- [x] **Missing Floor Tests:** Added direct tests for `F3`, `F5`, `F6`, `F8`, and `F10`.
- [x] **Vault Integrity Enforcement:** `trace_replay` now rejects tampered ledger entries with a hard failure.
- [x] **Import/Test Hang Isolation:** Removed eager ML imports from `core.enforcement` and `core.shared.floor_audit`; added regression coverage for `aki_contract` import boundaries.

---

## 🛠️ Operational Hardening (H1)

### [ ] H1.1: Observability
- [ ] Integrate `prometheus-client` into `arifosmcp.runtime.server`.
- [ ] Export `G`, `ΔS`, and `Ω₀` metrics to Grafana.
- [ ] Implement `check_vital` sensory tool for real-time thermo-budget monitoring.
- [ ] Add metric provenance labels such as `measured`, `derived`, `policy_constant`, and `placeholder` to public scores.
- [ ] Document which envelope values are live runtime measurements versus static governance defaults.
- [ ] Add external-evaluation logging so every public health or score claim can point to its source of truth.

### [ ] H1.2: ASI Hardening
- [ ] Update `core/organs/_2_asi.py` to use `sentence-transformers` for SBERT-based scoring.
- [ ] Refine `F6 Empathy` (κᵣ) thresholds based on human interaction logs.
- [ ] Hardened `F9 Anti-Hantu` detection for subtle first-person personhood claims.
- [ ] Expose semantic backend health clearly so external builders cannot imply semantic intelligence is live when backend status is degraded.
- [ ] Separate `governance intelligence` from `semantic intelligence` in health checks, scoring, and public explanations.

### [ ] H1.3: Test Recovery (80% Target)
- [ ] Fix broken unit tests in `tests/core/`.
- [ ] Implement parameter-locked regression tests for `arifOS.kernel` (legacy: `metabolic_loop_router`).
- [ ] Verify `VAULT999` Merkle-chain integrity under high-concurrency loads.
- [ ] Add regression tests for public claim safety so builder-facing answers cannot overstate uptime, tool availability, or score certainty.
- [ ] Add transcript-driven tests for public questions like `what can arifOS do?`, `is the MCP server working?`, and `is there AI on the server?`.

---

## 🧬 Intelligence Kernel Refinement (L0)

- [ ] Complete implementation of `core/physics/thermodynamics_hardened.py`.
- [ ] Integrate Landauer Bound check into the `arifOS.kernel` verdict logic (legacy: `metabolic_loop_router`).
- [ ] Forge `F3 Tri-Witness` backend connector for external evidentiary sources.
- [ ] Implement `F12 Injection Defense` L4 (Sandboxed Simulation).
- [ ] Formalize a bounded external evaluation rubric for `AI present`, `governance present`, `semantic backend healthy`, and `capability proven`.
- [ ] Distinguish `deterministic governance path`, `semantic retrieval path`, and `LLM-assisted path` in runtime outputs and docs.

---

## 🔌 Integration & Dashboard

- [ ] Sync `arifos.arif-fazil.com` site with latest docs (verify publication).
- [ ] Refine `arifosmcp/sites/apex-dashboard` Real-Time Fetch UI.
- [ ] Implement `888_signer` CLI utility for local human ratification tokens.
- [ ] Add public Agent Builder / Copilot guidance so external builders describe arifOS accurately and conservatively.
- [ ] Surface semantic backend status, auth continuity status, and active tool-profile mode directly in the dashboard.

---

**Last SEALed:** 2026.03.11-SEAL
*"Ditempa bukan diberi"* 🔥
