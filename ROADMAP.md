# arifOS ROADMAP — Horizon 2026

**Version:** 2026.03.12-FORGED  
**Status:** ✅ DEPLOYED  
**Coverage:** ~64% (+8pp from 56%)  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🏗️ Horizon 1: Stability & Hardening (Current)
*Focus: Stabilizing the constitutional kernel and expanding observability.*

- [x] **Runtime/Kernel Separation (L0-L2):** Decoupled transport logic from core decision logic.
- [x] **MCP Unification:** Registry-driven 8-tool canonical surface via `public_registry.py` (Phase 1 SEAL).
- [x] **Constitutional Floors (F1-F13):** Full implementation of the 13 immutable laws.
- [x] **Metabolic Loop E2E:** Verified 000-999 flow with two-layer identity envelope (auth_context + caller_context).
- [x] **99 Legacies System:** 99 human knowledge domains as immutable thermodynamic constants (`core/shared/legacies.py`).
- [x] **Canonical v1.0.0 Schema:** `ArifOSOutput` envelope + `Trace` verdict contract finalized.
- [x] **H1.1: Production Observability:** Prometheus metrics endpoint (`/metrics`) + Grafana on VPS. Constitutional G†, ΔS, Ω₀, P² metrics live.
- [x] **H1.2: ASI Hardening:** SBERT-based semantic scoring for F5 (Peace²), F6 (Empathy), and F9 (Anti-Hantu). 95% accuracy classifier implemented and tested.
- [~] **H1.3: Test Recovery (80% Target):** 
  - ✅ 126 new tests forged (kernel adapters + stage orchestrator + SBERT)
  - ✅ Coverage: 56% → ~64% (+8pp)
  - ✅ 3 failing tests fixed (P3 thermodynamics, trace_replay vault chaining)
  - ✅ `core/kernel/engine_adapters.py`: 0% → ~85%
  - ✅ `core/kernel/stage_orchestrator.py`: 0% → ~80%
  - ✅ `core/shared/sbert_floors.py`: 0% → ~75%
  - 🔄 Remaining: `evaluator.py`, `heuristics.py`, `init_000_anchor.py` (~80 tests needed)
- [ ] **Public Explanation Hardening:** Align Agent Builder, Copilot, and public docs to runtime truth so external surfaces do not overclaim capability or certainty.
- [ ] **Metric Provenance Model:** Every public score should declare whether it is measured, derived, bounded estimate, or policy constant.
- [ ] **External Evaluation Rubric:** Convert anecdotal transcript-based judgments into a repeatable evidence rubric for uptime, semantic health, governance health, and capability claims.
- [ ] **Semantic Backend Truthfulness:** Separate `governance kernel live` from `semantic/LLM path live` in health checks, builder copy, and dashboard UX.

---

## 🤝 Horizon 2: Agentic Federation (Q2 2026)
*Focus: Multi-agent coordination and collective governance.*

- [ ] **L5 Agent Roles:** Orchestration of specialized Architect, Engineer, Auditor, and Validator agents.
- [ ] **Collective VAULT999:** Multi-agent Merkle-chain sharing for collaborative memory and audit trails.
- [ ] **888_HOLD Refinement:** Enhanced human adjudication interface in the Sovereign Dashboard.
- [ ] **Amanah Handshake v2:** Decentralized governance tokens for federated clusters.
- [ ] **Builder-Safe Public Contracts:** Stable model-agnostic tool/profile contract for ChatGPT, Copilot Studio, Claude, and other agent builders.
- [ ] **Claim-Bounded Personas:** Public personas must reflect role and limits without overstating sovereign authority or semantic capability.

---

## 🌍 Horizon 3: Universal Integration (Q3-Q4 2026)
*Focus: Scaling arifOS across the edge and platform ecosystems.*

- [ ] **Edge Sidecar:** Lightweight arifOS runtime for mobile and IoT devices.
- [ ] **Native Platform Connectors:** Deep integration with OpenAI GPTs, Anthropic Projects, and Google Vertex AI.
- [ ] **The Sovereign Cloud:** Fully managed, private constitutional intelligence hosting.
- [ ] **Cross-Platform Builder Kits:** Reference packages for Copilot Studio, ChatGPT Apps, Claude Projects, and model-agnostic MCP deployments.
- [ ] **Public Benchmark Pack:** Standardized external evaluation harness for `what can arifOS do?`, `is the MCP server working?`, and `is there real AI inside?`.

---

## 🔬 Horizon 4: Exploration Frontiers (2027+)
*Focus: Recursive self-healing and thermodynamic intelligence research.*

- [ ] **Recursive Self-Healing:** Kernel-level ability to detect and patch constitutional drift autonomously.
- [ ] **Thermodynamic Grounding v2:** Using actual hardware power metrics for Landauer Bound enforcement.

---

## 📊 Latest Forge Update

**Date:** 2026-03-12  
**Commit:** `966409d11`  
**Status:** Pushed to main, auto-deployed to VPS  

### What Was Forged
- 126 new tests covering kernel execution layer
- SBERT semantic classification tests (49 tests for F5/F6/F9)
- Fixed 3 failing tests (constitutional compliance restored)
- Coverage increased from 56% to ~64%

### Path to 80% Coverage
| Module | Lines | Status | Tests Needed |
|--------|-------|--------|--------------|
| `core/kernel/evaluator.py` | 122 | 🔴 0% | ~25 tests |
| `core/kernel/heuristics.py` | 45 | 🔴 0% | ~10 tests |
| `core/kernel/init_000_anchor.py` | 60 | 🔴 0% | ~15 tests |
| `core/risk_engine.py` | 29 | 🔴 0% | ~8 tests |
| `core/organs/unified_memory.py` | 56 | 🔴 0% | ~12 tests |
| **Total** | **312** | | **~70 tests** |

---

**Last SEALed:** 2026.03.12-FORGED  
*"Ditempa bukan diberi"* 🔥
