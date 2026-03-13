# arifOS ROADMAP — Horizon 2026

**Version:** 2026.03.13-FORGED  
**Status:** 🛠️ CIVILIZATION-READINESS SPRINT  
**Coverage:** ~75% (Target: 80%)  
**APEX Score:** 8.6/10 → Target: 9.4+  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🌍 Horizon 0: Civilization-Readiness (March 2026)
*Focus: Trust transfer, proof packaging, and documentation polish to reach 9.4+ ecosystem score.*

*APEX Assessment: "Strong foundation, not yet civilization-ready. The gap is trust transfer from ideas into reader's mind in under 90 seconds."*

### H0.1: README Trinity Deployment-Grade Polish

**THE SURFACE (Human Legitimacy):**
- [ ] "Start Here" section with ecosystem navigation map
- [ ] "Why arifOS emerged from geology" unique positioning
- [ ] Professional gateway design (not just reflective essay)
- [ ] Clear conversion paths: followers, collaborators, adopters

**THE MIND (Constitutional Doctrine):**
- [ ] "Who this is for" persona targeting (4 audiences)
- [ ] Doctrine → Runtime mapping table (F2→search_reality, etc.)
- [ ] Design principles section (reversibility first, etc.)
- [ ] Glossary for constitutional vocabulary

**THE BODY (Runtime Engine):**
- [ ] Badges and deployment markers (tests, coverage, MCP)
- [ ] 5-minute quickstart with copy-paste commands
- [ ] "Why now?" section (MCP + governance gap timing)
- [ ] Clear non-goals and known limitations

### H0.2: Proof-of-Reality Artifacts

- [ ] Demo folder with 3 runnable examples:
  - Safe query with governed response
  - 888_HOLD blocking destructive command
  - VAULT999 ledger verification
- [ ] Terminal output screenshots in README
- [ ] Architecture diagram (minimal, clear)
- [ ] 90-second demo video/GIF

### H0.3: Competitive Trust Positioning

- [ ] Explicit threat model (what risks are mitigated)
- [ ] Comparison matrix: arifOS vs alternatives
- [ ] Honest "Known Limitations" section
- [ ] Non-goals documentation (builds credibility)

### H0.4: Developer Onboarding Pathway

- [ ] Contributor guide (Good First Issues)
- [ ] Architecture documentation for extenders
- [ ] Process for proposing new Floors/tools/validators
- [ ] Clear test expectations

**Success Criteria:**
- APEX score: 8.6 → 9.4+
- First-time comprehension: 7.0 → 9.0+
- Deployment readiness: 6.8 → 9.0+
- Trust transfer: 8.0 → 9.5+

---

## 🏗️ Horizon 1: Stability & Hardening (Q2 2026)
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

## 🤝 Horizon 2: Agentic Federation (Q3 2026)
*Focus: Multi-agent coordination and collective governance.*

- [ ] **L5 Agent Roles:** Orchestration of specialized Architect, Engineer, Auditor, and Validator agents.
- [ ] **Collective VAULT999:** Multi-agent Merkle-chain sharing for collaborative memory and audit trails.
- [ ] **888_HOLD Refinement:** Enhanced human adjudication interface in the Sovereign Dashboard.
- [ ] **Amanah Handshake v2:** Decentralized governance tokens for federated clusters.
- [ ] **Builder-Safe Public Contracts:** Stable model-agnostic tool/profile contract for ChatGPT, Copilot Studio, Claude, and other agent builders.
- [ ] **Claim-Bounded Personas:** Public personas must reflect role and limits without overstating sovereign authority or semantic capability.

---

## 🌍 Horizon 3: Universal Integration (Q4 2026 - Q1 2027)
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

**Date:** 2026-03-13  
**Commit:** TBD  
**Status:** APEX Assessment Response  

### What Was Forged
- **APEX Runtime Fixes:**
  - Fixed `audit_rules` returning SABAR/ERROR → Now returns full 13 Floors audit
  - Fixed `check_vital` thermodynamics import failure → Graceful degradation
  - Added `_build_constitutional_audit()` with doctrine→runtime mapping
  - Added `_build_vitals_report()` with capability map
- **APEX Assessment:** 8.6/10 with clear path to 9.4+
  - Strengths: Concept originality, architecture ambition, ecosystem alignment
  - Gaps: Trust transfer, proof packaging, onboarding clarity
  - Critical fix needed: Proof-of-reality demos

### Path to Civilization-Readiness (9.4+ Score)
| Dimension | Current | Target | Priority |
|-----------|---------|--------|----------|
| Narrative identity | 8.9 | 9.5 | Medium |
| Originality | 9.4 | 9.5 | Low |
| Technical signaling | 8.9 | 9.5 | Medium |
| **Onboarding clarity** | **7.0** | **9.0** | **P0** |
| **Verification confidence** | **6.9** | **9.0** | **P0** |
| **Proof of claims** | **6.8** | **9.0** | **P0** |
| Ecosystem coherence | 8.6 | 9.5 | Medium |

### Path to 80% Coverage
| Module | Lines | Status | Tests Needed |
|--------|-------|--------|--------------|
| `core/kernel/evaluator.py` | 122 | 🟡 ~80% | ~10 tests |
| `core/kernel/heuristics.py` | 45 | 🟢 ~98% | ✅ Complete |
| `core/kernel/init_000_anchor.py` | 60 | 🟢 100% | ✅ Complete |
| `core/risk_engine.py` | 29 | 🟢 ~90% | ✅ Complete |
| `core/organs/unified_memory.py` | 56 | 🟢 ~96% | ✅ Complete |
| **Total** | **312** | **~75%** | **~20 tests** |

---

**Last SEALed:** 2026.03.13-FORGED  
*"Ditempa bukan diberi"* 🔥
