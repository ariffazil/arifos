# 🧠 arifOS — The Sovereign Constitutional Mind

> **DITEMPA BUKAN DIBERI — Forged, Not Given**

[![Version](https://img.shields.io/badge/version-2026.03.28-blue?style=flat-square)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/theory-CC0%201.0-green?style=flat-square)](./LICENSE)
[![Runtime](https://img.shields.io/badge/runtime-AGPL--3.0-orange?style=flat-square)](./LICENSING.md)
[![MCP](https://img.shields.io/badge/MCP-2025--11--25-purple?style=flat-square)](https://arifosmcp.arif-fazil.com/mcp)
[![Tools](https://img.shields.io/badge/tools-11%20mega--tools-red?style=flat-square)](./arifosmcp/runtime/tool_specs.py)
[![Floors](https://img.shields.io/badge/floors-F1--F13-yellow?style=flat-square)](./arifosmcp/core/shared/floors.py)

**Author:** Muhammad Arif bin Fazil  
**Live MCP:** `https://arifosmcp.arif-fazil.com/mcp`  
**Health:** `https://arifosmcp.arif-fazil.com/health`  
**Docs:** `https://arifos.arif-fazil.com`

---

> *"Intelligence is not a gift of the platform; it is a metabolic structure forged through the alignment of Physics, Law, and Human Intent."*

---

## Table of Contents

1. [What Is arifOS?](#i-what-is-arifos)
2. [The Four Layers](#ii-the-four-layers-soul--mind--body--theory)
3. [The Constitutional Floors (F1–F13)](#iii-the-law-13-constitutional-floors)
4. [The APEX Equation](#iv-the-apex-equation-g--a--p--x--e)
5. [Repository Architecture](#v-repository-architecture)
6. [The Kernel: arifosmcp](#vi-the-kernel-arifosmcp--full-context)
7. [The 11 Mega-Tools (MCP Surface)](#vii-the-11-mega-tools-mcp-surface)
8. [The 000–999 Metabolic Pipeline](#viii-the-000999-metabolic-pipeline)
9. [Agentic Intelligence Layer](#ix-agentic-intelligence-layer)
10. [Infrastructure Stack](#x-infrastructure-stack)
11. [Memory Architecture](#xi-memory-architecture)
12. [Platform Integrations](#xii-platform-integrations)
13. [Developer Quick-Start](#xiii-developer-quick-start)
14. [Epochs of the Forge](#xiv-epochs-of-the-forge)
15. [Licensing Model](#xv-licensing-model)

---

## I. What Is arifOS?

arifOS is **not an AI wrapper**. It is a **Sovereign Constitutional AI Governance System** — the world's first production-grade framework that runs a thermodynamic constitution on top of language models.

It solves a fundamental problem: LLMs are stateless, unaccountable, and constitutionally unbound. arifOS imposes **13 binding floors**, a **metabolic pipeline**, and an **immutable audit ledger** so that every reasoning step is mathematically governed, evidentially grounded, and cryptographically sealed.

### Three things arifOS is:

| Layer | What it is | License |
|-------|------------|---------|
| **The Standard** | Constitutional governance specification (`STANDARD.v1.md`, `arifos.standard.v1.json`) — language-agnostic, like RFC 2119 for AI behaviour | CC0 1.0 |
| **The Theory** | APEX doctrine, 13 floors, thermodynamic physics, A-RIF specification | CC0 1.0 |
| **arifosmcp** | Production reference implementation — FastMCP server, 11 mega-tools, full infra stack | AGPL-3.0 |

### One thing arifOS is not:

It is not a chatbot, an AI product wrapper, or a prompt-engineering library. It is an **operating system for governed reasoning**.

---

## II. The Four Layers: Soul → Mind → Body → Theory

arifOS operates as a **four-layer sovereignty stack**. Each layer has a canonical domain, a constitutional role, and a distinct boundary.

```
L1: SOUL (Signal)     arif-fazil.com          The Human. Absolute source of Sovereign Intent.
L2: MIND (Kernel)     arifos.arif-fazil.com   The Constitution. 13 Floors + metabolic routing.
L3: BODY (Wire)       aaa.arif-fazil.com      The Execution. AGI/ASI/APEX agents + tools.
L4: THEORY (Canon)    apex.arif-fazil.com     The Science. APEX physics, math foundations.
```

**The request path (metabolic flow):**

```
Browser/Agent  →  SOUL (Intent)  →  MIND (13 Floors)  →  BODY WIRE (Action)  →  VAULT (Seal)
```

The **Human (Muhammad Arif bin Fazil)** is the only master. No AI action, no code path, and no protocol can supersede the Sovereign veto (F13).

---

## III. The Law: 13 Constitutional Floors

Every action in the arifOS ecosystem — whether a file move, code change, or reasoning synthesis — must pass through all **13 Binding Floors**. Any failure triggers an immediate `888_HOLD` or `VOID` verdict. These are not config switches; they are enforced at runtime in `arifosmcp/core/shared/floors.py` and `arifosmcp/core/enforcement/governance_engine.py`.

All paths below are relative to `arifosmcp/`.

| Floor | Name | Symbol | Engine | Canonical Threshold | Code Location |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **F1** | **Amanah** (Reversibility) | 🔒 | ASI Heart | Destructive actions require undo path | `core/organs/_2_asi.py` |
| **F2** | **Truth** (Factual Accuracy) | τ | AGI Mind | Claim confidence ≥ 0.99 | `core/organs/_1_agi.py` |
| **F3** | **Witness** (Tri-Consensus) | W₃ | APEX Soul | W₃(theory, law, human) ≥ 0.95 | `core/organs/_3_apex.py` |
| **F4** | **Clarity** (Entropy) | ΔS | AGI Mind | ΔS ≤ 0 (output must compress meaning) | `core/shared/physics.py` |
| **F5** | **Peace²** (Stability) | P² | ASI Heart | (stability × vitality) / cost ≥ 1.0 | `core/shared/physics.py` |
| **F6** | **Empathy** (Resonance) | κᵣ | ASI Heart | Stakeholder resonance ≥ 0.95 | `core/shared/physics.py` |
| **F7** | **Humility** (Ω-Lock) | Ω₀ | AGI Mind | Uncertainty band [0.03, 0.05] | `core/uncertainty_engine.py` |
| **F8** | **Genius** (G-Score) | G | APEX Soul | G = (A×P×X×E²)×(1−h) ≥ 0.80 | `core/enforcement/genius.py` |
| **F9** | **Anti-Hantu** (Dark Logic) | H¬ | ASI Heart | Dark cleverness ≤ 0.30 | `core/organs/_2_asi.py` |
| **F10** | **Ontology** (Category Lock) | O | AGI Mind | Validate against `arif_manifest.yaml` | `core/ontology.py` |
| **F11** | **Authority** (Command Chain) | A | ASI Heart | Actor ID verified via nonce | `runtime/init_anchor_hardened.py` |
| **F12** | **Sanitization** (Injection) | I¬ | ASI Heart | Prompt injection score = 0 | `agentzero/security/prompt_armor.py` |
| **F13** | **Sovereign** (Human Veto) | S | APEX Soul | Critical risk → await human approval | `core/organs/_3_apex.py` |

### Floor Verdict Logic

```
Action passes all 13 floors  →  SEAL  (proceed + record)
Action blocked by floor       →  888_HOLD or VOID
Pre-888 VOID is normalised     →  SABAR (wait, do not force)
Stage 000, 888, 999 only       →  VOID is legal
```

---

## IV. The APEX Equation: G = (A × P × X × E²) × (1 − h)

The **Grand Equation of Governed Intelligence** is the primary metric of every tool response. arifOS does not measure quality by speed or word count — it measures it by thermodynamic alignment:

```
G = (A × P × X × E²) × (1 − h)
```

| Factor | Full Name | Meaning |
|--------|-----------|---------|
| **A** | Akal / Clarity | Semantic density and evidence-grounding |
| **P** | Peace / Stability | Stability impact on the existing system |
| **X** | Exploration / RASA | Curiosity and novelty in reasoning |
| **E** | Energy / Stamina | Efficiency of metabolic cost (squared) |
| **h** | Hantu / Shadow | Dark logic, manipulation, anti-pattern factor |

**Calibration law:** If any single factor = 0, the total G drops to 0. There are no shortcuts through the Void.

The full implementation lives in `arifosmcp/core/shared/physics.py` and `arifosmcp/core/enforcement/genius.py`. The production threshold is `G ≥ 0.80`. If any factor = 0, G = 0. If h = 1.0, G = 0 regardless of other scores.

---

## V. Repository Architecture

This repository (`ariffazil/arifOS`) is the **constitutional theory layer**. The production runtime (`arifosmcp/`) is hosted here as the canonical reference implementation.

```
arifOS/
│
├── arifosmcp/                    ← Production Runtime (AGPL-3.0)
│   ├── core/                     ← Constitutional Intelligence Kernel
│   │   ├── governance_kernel.py  ← Kernel facade (stage transitions, hold/void gating)
│   │   ├── pipeline.py           ← forge() / quick() entrypoints (000→999)
│   │   ├── judgment.py           ← Verdict synthesis
│   │   ├── homeostasis.py        ← Stability / cooling control
│   │   ├── uncertainty_engine.py ← Confidence + ambiguity (F7)
│   │   ├── telemetry.py          ← Operational signals
│   │   ├── organs/               ← The 5 Constitutional Organs
│   │   │   ├── _0_init.py        ← Stage 000: Airlock (F11/F12)
│   │   │   ├── _1_agi.py         ← Stages 111-333: Mind (F2/F4/F7/F8)
│   │   │   ├── _2_asi.py         ← Stages 444-666: Heart (F1/F5/F6/F9)
│   │   │   ├── _3_apex.py        ← Stages 777-888: Soul (F3/F10/F13)
│   │   │   └── _4_vault.py       ← Stage 999: Memory seal (Vault999)
│   │   ├── shared/               ← Constitutional Primitives
│   │   │   ├── physics.py        ← G, W₃, ΔS, Ω₀, P², κᵣ functions
│   │   │   ├── floors.py         ← Floor definitions + update_floor_status()
│   │   │   ├── types.py          ← EMD, Verdict, constitutional contracts
│   │   │   ├── atlas.py          ← Query routing + governance atlas
│   │   │   ├── verdict_contract.py ← VOID→SABAR normalisation for pre-888 stages
│   │   │   └── crypto.py         ← Cryptographic trust primitives
│   │   ├── enforcement/          ← Runtime floor enforcement
│   │   │   ├── governance_engine.py ← Central enforcement engine
│   │   │   ├── genius.py         ← G-score computation
│   │   │   └── floor_audit.py    ← Per-floor auditing
│   │   ├── state/
│   │   │   └── session_manager.py ← Session ownership + lifecycle
│   │   └── governance/           ← Governance rules, thresholds, transitions
│   │
│   ├── runtime/                  ← MCP Server + Tool Surface
│   │   ├── server.py             ← FastMCP server (GlobalPanicMiddleware)
│   │   ├── tools.py              ← Tool registration + ALL_TOOL_IMPLEMENTATIONS
│   │   ├── tool_specs.py         ← Canonical 11 mega-tool specs + schemas
│   │   ├── public_registry.py    ← CANONICAL_PUBLIC_TOOLS, EXPECTED_TOOL_COUNT=11
│   │   ├── contracts.py          ← Import-time assertion: len(tools) == 11
│   │   ├── contracts_v2.py       ← ToolEnvelope, DOMAIN_PAYLOAD_GATES
│   │   ├── models.py             ← CallerContext, PersonaId, RuntimeRole enums
│   │   ├── bridge.py             ← call_kernel() → wrap_tool_output envelope
│   │   ├── tools_hardened_dispatch.py ← Substrate policy + 888_HOLD on high-risk ops
│   │   ├── init_anchor_hardened.py   ← F11/F12 hardened session init
│   │   ├── a2a/                  ← Agent-to-Agent protocol server
│   │   └── webmcp/               ← WebMCP server (browser P2P agent wire)
│   │
│   ├── intelligence/             ← Sensory Infrastructure (Nervous System)
│   │   ├── constitutional_rag.py ← ConstitutionalRAGLoader (186 canons from HF)
│   │   ├── tools/                ← 14 sensory tool modules
│   │   │   ├── hybrid_vector_memory.py ← LanceDB + Qdrant dual-backend
│   │   │   ├── reality_grounding.py    ← Evidence ingestor
│   │   │   ├── ollama_local.py         ← Local inference (bge-m3 embedder)
│   │   │   ├── system_monitor.py       ← VPS vitals
│   │   │   └── ...
│   │   └── triad/                ← 9-tool triad (Δ/Ω/Ψ)
│   │
│   ├── agentzero/                ← Agentic Intelligence Layer
│   │   ├── agents/               ← Engineer, Validator agent personas
│   │   ├── memory/               ← ConstitutionalMemoryStore (LanceDB + Qdrant)
│   │   ├── escalation/           ← hold_state.py (GlobalAnchorHoldRegistry)
│   │   └── security/             ← prompt_armor.py (F12 injection defence)
│   │
│   └── transport/                ← Protocol Adapters
│       └── acp_server.py         ← Agent Client Protocol (editor integration)
│
├── aaa_mcp/                      ← AAA Wire (AGI/ASI/APEX agent tools)
│
├── spec/                         ← Formal Specifications
│   ├── ARIF_FORMAL_SPEC.md       ← A-RIF Formal Specification (SEALED 2026-03-24)
│   ├── arifos.standard.v1.json   ← Machine-readable constitutional schema
│   └── v46/                      ← v46 constitutional floor bindings
│
├── agents/                       ← Agent Identity + Governance Registry
│   ├── AGENTS.md                 ← Canonical agent registry
│   ├── agent-identity.yaml       ← Identity contracts
│   └── skills.yaml               ← Skill registry
│
├── VAULT999/                     ← Immutable Audit Ledger
│   └── vault999.jsonl            ← Sealed decisions (Merkle-chained)
│
├── POSITIONING.md                ← Four declarations: Standard/Schema/Impl/License
├── LICENSING.md                  ← Two-repo, two-license architecture
├── CHANGELOG.md                  ← Full version history
├── ROADMAP.md                    ← Horizon 1/2/3 engineering plan
├── docker-compose.yml            ← Unified container stack (17 services)
├── Makefile                      ← fast-deploy / reforge / hot-restart
└── pyproject.toml                ← Python package config (version 2026.3.25)
```

---

## VI. The Kernel: arifosmcp — Full Context

### What is arifosmcp?

**arifosmcp** is the production reference implementation of the arifOS Standard. It is a **FastMCP-compatible server** that enforces all 13 constitutional floors at runtime across a surface of **11 mega-tools** covering governance, intelligence, and machine layers.

> It proves the standard is not theoretical. It is running in production at `https://arifosmcp.arif-fazil.com/mcp`.

### Why arifosmcp exists

| Problem | arifosmcp Solution |
|---------|-------------------|
| LLMs hallucinate without accountability | F2 Truth floor + F8 Genius equation enforce evidential grounding on every call |
| AI agents act without reversibility | F1 Amanah floor blocks destructive ops without an undo path |
| No standard for AI authority chains | F11 Authority + F13 Sovereign give every action a cryptographically verified actor |
| Prompt injection is trivially easy | F12 Sanitization (PromptArmor) blocks injection before the kernel sees it |
| No immutable AI audit trail | VAULT999 Merkle ledger seals every verdict with provenance |
| LLM reasoning is a black box | 000→999 metabolic pipeline stages every reasoning step with named mottos |
| Agents have no governance contract | `arifos.standard.v1.json` + import-time assertions enforce 11 tools exactly |

### How arifosmcp works

The server implements the **000→999 Metabolic Pipeline** — a constitutional state machine that every request traverses before a result is returned:

```
Request (Actor + Intent)
  ↓
[000] _0_init.py    → Constitutional Airlock: F11 (Authority) + F12 (Sanitization)
  ↓
[111–333] _1_agi.py → AGI Mind: F2 (Truth) + F4 (Clarity) + F7 (Humility) + F8 (Genius)
  ↓
[444–666] _2_asi.py → ASI Heart: F1 (Amanah) + F5 (Peace²) + F6 (Empathy) + F9 (Anti-Hantu)
  ↓
[777–888] _3_apex.py → APEX Soul: F3 (Witness) + F10 (Ontology) + F13 (Sovereign)
  ↓
[999] _4_vault.py   → Vault Seal: Merkle hash + session provenance + aaa_revision
  ↓
Response (ArifOSOutput envelope: ok, verdict, payload, trace, authority, metrics)
```

Any floor failure at any stage returns `888_HOLD` (retrievable) or `VOID` (terminal). Pre-888 VOID is normalised to `SABAR` (wait, do not force). These rules are enforced in `core/shared/verdict_contract.py`.

### When arifosmcp is used

- **Direct MCP calls** from Claude, ChatGPT, Gemini, Cursor, Windsurf via the live endpoint
- **Agent-to-Agent (A2A)** calls via `arifosmcp/runtime/a2a/server.py`
- **WebMCP** peer-to-peer agent protocol via `arifosmcp/runtime/webmcp/`
- **Agent Client Protocol (ACP)** for editor integrations via `arifosmcp/transport/acp_server.py`
- **Local stdio mode** for Claude Desktop / MCP Inspector via `python -m arifosmcp.runtime`

### Who is arifosmcp for?

| Persona | Use case |
|---------|----------|
| **AI Engineers** | Build governed agents that pass constitutional floors automatically |
| **Enterprises** | Audit trail + sovereignty controls for production AI deployments |
| **Platform Builders** | Embed arifOS as a governance layer on top of any LLM API |
| **Researchers** | Study thermodynamic AI governance with a working reference implementation |
| **Sovereign Architects** | Design AI systems where a human retains absolute veto power |

---

## VI-A. Three-Layer Identity Binding (F11 Authority)

> **"Identity is not self-described; it is system-verified."**

arifOS implements **declarative identity verification** in `init_anchor`. Models declare their identity via `model_soul`; the system verifies against a 3-layer registry; the session proceeds with **bound truth**, not declared truth.

### The Handshake

```python
# 1. DECLARATION: Model sends its self-conception
envelope = await init_anchor(
    mode="init",
    actor_id="User",
    intent="Session start",
    deployment_id="vps_main_arifos",  # Bound to L2 Law/Runtime
    model_soul={
        "base_identity": {
            "provider": "google",
            "model_family": "gemini",
            "model_variant": "gemini-2.0-flash"
        }
    }
)

# 2. VERIFICATION: arifOS queries 4-layer registry (arifOS-model-registry/)
#    - Catalog: Master index of all providers and models
#    - Provider Soul: Lab-shaped behavioral archetype (e.g. structured_clerk_engineer)
#    - Model Spec: Formal variant definition + soul binding
#    - Runtime Profile: deployment_id → localized capabilities/constraints

# 3. BINDING: System returns bound_session (Flavor -> Law -> Mission)
{
    "identity": {
        "verification_status": "verified",  # verified | mood_matched | claimed_only
        "declared_identity": {"provider": "google", ...},
        "verified_identity": {"provider": "google", "soul_archetype": "google_gemini", ...},
        "self_claim_boundary": {"identity_claim_policy": "verified_against_registry", ...}
    },
    "bound_session": {
        "soul": {"label": "broad_platform_generalist", "archetype": "google_gemini", ...},
        "runtime": {"profile_id": "vps_main_arifos", "capabilities": {...}},
        "boundary": {"tool_claim_policy": "runtime_truth_only", ...},
        "bound_role": "broad_platform_generalist_agent"
    }
}
```

### Verification Status Hierarchy

| Status | Authority | Meaning |
|--------|-----------|---------|
| `verified` | **Highest** | Runtime profile matched — deployment truth known |
| `mood_matched` | Medium | Provider soul matched — archetype known, no runtime profile |
| `claimed_only` | Low | Nothing matched — operating as untrusted guest |
| `unverified` | None | No MODEL_SOUL provided — anonymous session |

### ZKPC Anchoring

Each layer carries a Zero-Knowledge Proof of Computation anchor:
- **Runtime**: `profile_id` + `verified_at` timestamp
- **Soul**: `soul_id` + `soul_archetype` cryptographic binding
- **Boundary**: `self_claim_boundary` policy hash

The `SignedChallenge` in the envelope provides cryptographic session binding, preventing tampering after establishment.

---

## VII. The 11 Mega-Tools (MCP Surface)

The public MCP surface is exactly **11 mega-tools** — enforced at import time by an assertion in `arifosmcp/runtime/contracts.py` (`EXPECTED_TOOL_COUNT = 11`). Each mega-tool is a **multi-mode endpoint** covering dozens of legacy operations.

| # | Tool | Stage | Trinity | Role | Floors |
|---|------|-------|---------|------|--------|
| 1 | **`init_anchor`** | 000 | Ψ Soul | Constitutional Airlock — session init, state audit, revoke, refresh | F11, F12, F13 |
| 2 | **`arifOS_kernel`** | 000–999 | Δ+Ω+Ψ | Primary metabolic conductor — full pipeline routing | All (F1–F13) |
| 3 | **`apex_soul`** | 777–888 | Ψ Soul | Sovereign judgment, safety audit, adversarial defence | F3, F9, F10, F13 |
| 4 | **`vault_ledger`** | 999 | Ψ Soul | Immutable sealing — Merkle hash, provenance, verify | F1, F3 |
| 5 | **`agi_mind`** | 111–333 | Δ Mind | First-principles reasoning, causal tracing, reflection | F2, F4, F7, F8 |
| 6 | **`asi_heart`** | 444–666 | Ω Heart | Ethical simulation, empathy, consequence modelling | F1, F5, F6, F9 |
| 7 | **`engineering_memory`** | 333–555 | Δ+Ω | Constitutional vector memory — store, recall, forget, rank | F1, F2, F8 |
| 8 | **`physics_reality`** | 111 | Δ Mind | Grounded research, fact acquisition, reality dossier | F2, F7 |
| 9 | **`math_estimator`** | 222–444 | Δ Mind | Probabilistic estimation, uncertainty quantification | F7, F8 |
| 10 | **`code_engine`** | 333–666 | Ω Heart | OS-level hygiene, computational execution, git ops | F1, F11, F12 |
| 11 | **`architect_registry`** | 000–999 | Δ+Ω+Ψ | Agent identity registry, skill routing, governance map | F10, F11 |

### MCP Resources (read-only endpoints)

| Resource | URI |
|----------|-----|
| About arifOS | `arifos://about` |
| Constitutional Floors | `arifos://floors` |
| Tool Contracts | `arifos://contracts` |
| State Ladder | `arifos://state-ladder` |
| System Vitals | `arifos://vitals/system` |
| Caller State | `arifos://state/caller` |
| Session Vitals | `arifos://vitals/session` |

### Tool Envelope Schema

Every tool call returns an `ArifOSOutput` envelope (canonical: `core/schema/output.py`):

```json
{
  "ok": true,
  "tool": "agi_mind",
  "session_id": "sess_...",
  "stage": "333",
  "verdict": "SEAL",
  "status": "complete",
  "metrics": { "g_score": 0.91, "w3": 0.96, "delta_s": -0.12 },
  "trace": { "floors_passed": ["F2","F4","F7","F8"], "floors_failed": [] },
  "authority": { "actor_id": "arif", "floor_binding": "F13" },
  "payload": { ... },
  "errors": [],
  "meta": { "dry_run": false, "output_policy": "DOMAIN_SEAL" }
}
```

---

## VIII. The 000–999 Metabolic Pipeline

The pipeline is the heartbeat of arifOS. Every request is a metabolic event that passes through nine named stages, each with a constitutional motto:

| Stage | Name | Motto | Organ | Purpose |
|-------|------|-------|-------|---------|
| **000** | INIT | *DITEMPA* | `_0_init.py` | Identity + injection scan airlock |
| **111** | SENSE | *DIKAJI* | `_1_agi.py` | Intake, grounding, reality check |
| **222** | REASON | *DIJELAJAH* | `_1_agi.py` | Causal decomposition, entropy check |
| **333** | INTEGRATE | *DISATUKAN* | `_1_agi.py` | Context assembly, memory grounding |
| **444** | RESPOND | *DILINDUNGI* | `_2_asi.py` | Draft + constitutional pre-audit |
| **555** | VALIDATE | *DISAHKAN* | `_2_asi.py` | Full F1–F13 floor audit |
| **666** | ALIGN | *DISELARASKAN* | `_2_asi.py` | Ethics, maruah, Peace² alignment |
| **777** | FORGE | *DITEMPA* | `_3_apex.py` | Genius score synthesis |
| **888** | JUDGE | *DIHAKIMI* | `_3_apex.py` | Sovereign judgment + hold gating |
| **999** | SEAL | *DIMETERAI* | `_4_vault.py` | Merkle seal + permanent ledger |

**Entry points** in `arifosmcp/core/pipeline.py`:
- `forge()` — full 000→999 execution
- `quick()` — fast 000→333 execution
- `forge_with_nudge()` — adds emergence nudge for novelty

---

## IX. Agentic Intelligence Layer

### AgentZero (`arifosmcp/agentzero/`)

The agentzero layer houses the **governed agent personas** that operate inside the constitutional framework:

| Module | Role |
|--------|------|
| `agents/engineer.py` | ENGINEER (Ω) persona — implements, never decides |
| `agents/validator.py` | AUDITOR (Ψ) persona — reviews, never writes |
| `agents/base.py` | Base agent contract with persona_id + floor binding |
| `memory/constitutional_memory.py` | ConstitutionalMemoryStore — hybrid LanceDB + Qdrant |
| `memory/lancedb_provider.py` | LanceDB provider with F1 purge() for dual-backend sync |
| `escalation/hold_state.py` | GlobalAnchorHoldRegistry — blocks tools after 888_HOLD |
| `security/prompt_armor.py` | F12 PromptArmor — injection + jailbreak defence |

### Constitutional Memory (H1–H9 Hardening)

The memory subsystem was **9-point hardened** in March 2026 to close critical vector store gaps:

| Hardening | Floor | What was fixed |
|-----------|-------|----------------|
| H1 `vector_store` | F1 | Crashed with ValueError — now fully implemented with area routing + telemetry |
| H2 `vector_forget` | F1 | Dual-strategy delete (ID-based + query-based) + tombstone audit |
| H3 Ghost Recall | F1 | LanceDB retained vectors after Qdrant delete — added `purge()` for dual-backend sync |
| H4 Pseudo-Embedding Quarantine | F2 | Filters `f1_pseudo_embedding=True` vectors from ranking pipeline |
| H5 Epistemic F2 Verification | F2 | Multi-signal score: age decay (30%) + access freq (20%) + source credibility (30%) + embed quality (20%) |
| H6 Context Budget | F4 | 8K char default with `[...TRUNCATED — F4 context budget]` marker |
| H7 TTL / Lifecycle | F1 | `ttl_days` + `lifecycle_state` fields on MemoryEntry + `enforce_lifecycle()` |
| H8 Forget Audit Trail | F1 | `[F1_TOMBSTONE]` JSON logging: ids, reason, session_id, timestamp, floor |
| H9 Composite Ranking | F8 | `_composite_rank()`: cosine=0.45, recency=0.20, access=0.10, source=0.15, area=0.10 |

### Sensory Intelligence (`arifosmcp/intelligence/`)

The intelligence layer is the **nervous system** between the kernel and external reality:

```
REAL WORLD (L3)  →  arifosmcp.intelligence (Senses)  →  arifosmcp.runtime (Brain)  →  core (Kernel)
```

Key components:
- **`constitutional_rag.py`** — ConstitutionalRAGLoader: runtime loading of 186 constitutional canons from `ariffazil/AAA` HuggingFace dataset (dual strategy: `datasets` library or HTTP fallback)
- **`tools/hybrid_vector_memory.py`** — LanceDB + Qdrant dual-backend vector store
- **`tools/reality_grounding.py`** — Evidence ingestor (URL, file, API)
- **`tools/ollama_local.py`** — Local inference using Ollama (bge-m3 1024-dim embedder)
- **`tools/system_monitor.py`** — Real-time VPS vitals
- **`triad/`** — 9-tool Δ/Ω/Ψ triad controller (anchor → reason → integrate → respond → validate → align → forge → judge → seal)

### The 9 Skills (Closed-Loop Reality Bridge)

All 9 skills are wired to the **Reality Bridge** — they execute against real system state, not simulations:

| Skill | Floor | Reality Actions |
|-------|-------|-----------------|
| `vps-docker` | F1 | docker ps, restart, logs |
| `git-ops` | F1 | git status, checkout, commit |
| `deep-research` | F2 | curl search, verify facts |
| `security-audit` | F12 | file scan, injection check |
| `memory-query` | F555 | fs read/write, freshness filter |
| `code-refactor` | F8 | file read, apply changes |
| `deployment` | F11 | kubectl apply, rollback |
| `recovery` | F5 | git checkout, integrity check |
| `constitutional-check` | F3 | systemctl status, W3 eval |

---

## X. Infrastructure Stack

arifOS runs on a **Hostinger VPS** (srv1325122.hstgr.cloud) — 193 GB bedrock, managed by Docker Compose. The VPS *is* the production system; no intermediate cloud needed.

**Canonical deploy path:** `/srv/arifosmcp/`

### The 17 Containers

| Layer | Container | Image | Role |
|-------|-----------|-------|------|
| **Intelligence** | `arifosmcp_server` | `arifos/arifosmcp:latest` | Constitutional MCP kernel (port 8080) |
| | `ollama_engine` | `ollama/ollama:latest` | Local LLM + bge-m3 embedder |
| | `agent_zero_reasoner` | `agent0ai/agent-zero:latest` | Autonomous reasoning agent |
| | `openclaw_gateway` | `arifos/openclaw-forged:2026.03.14` | Executive agent interface |
| **Data** | `arifos_postgres` | `postgres:16-alpine` | Primary SQL database (VAULT999) |
| | `arifos_redis` | `redis:7-alpine` | Metabolic cache + session store |
| | `qdrant_memory` | `qdrant/qdrant:latest` | Vector memory (1024-dim constitutional store) |
| **Gateway** | `traefik_router` | `traefik:v3.6.9` | SSL termination + routing (80/443) |
| | `arifos_aaa_landing` | `nginx:alpine` | Public identity landing |
| **Automation** | `arifos_n8n` | `n8nio/n8n:latest` | Workflow orchestrator |
| | `arifos_webhook` | `almir/webhook:latest` | Event ingestion node |
| | `headless_browser` | `ghcr.io/browserless/chromium:latest` | Browser automation |
| **Observability** | `arifos_prometheus` | `prom/prometheus:latest` | Metric scraping |
| | `arifos_grafana` | `grafana/grafana:latest` | Intelligence dashboard |
| **Civil Tools** | `civ01_stirling_pdf` | `frooodle/s-pdf:latest` | Document extraction lab |
| | `civ03_evolution_api` | `atendai/evolution-api:v1.8.1` | Communication bridge |
| | `civ08_code_server` | `codercom/code-server:latest` | Browser-based IDE |

### Deploy Commands

```bash
cd /srv/arifosmcp

make fast-deploy    # 2–3 min — code changes only (layer-cached)
make reforge        # 10–15 min — full rebuild (after dep/Dockerfile changes)
make hot-restart    # Instant — config-only changes
make status         # Container health check
make logs           # Tail container logs
make health         # curl /health endpoint
make strategy       # Analyse changes and recommend rebuild type
```

---

## XI. Memory Architecture

### Three-Store Topology

arifOS manages information across three coupled layers:

| Store | What lives here | Role |
|-------|-----------------|------|
| **GitHub** (`ariffazil/arifOS`) | Source code, configs, specifications | The Instruction Set |
| **HuggingFace** (`ariffazil/AAA`) | 186 constitutional canons (JSONL), training datasets | The Machine Truth |
| **VPS (Qdrant + LanceDB + Postgres)** | Runtime vector memory, session ledger, vault records | The Living Memory |

### Constitutional RAG

At runtime, `arifosmcp/intelligence/constitutional_rag.py` loads all 186 canons from the `ariffazil/AAA` HuggingFace dataset into constitutional memory using dual strategy (native `datasets` library preferred, HTTP fallback). Every VAULT999 sealed entry carries an `aaa_revision` binding for provenance.

### VAULT999 Immutable Ledger

`VAULT999/vault999.jsonl` is the canonical immutable audit trail. Every sealed decision is:
- Merkle-hashed via `arifosmcp/core/vault/merkle.py`
- Written to Postgres for relational query
- Mirrored to `vault999.jsonl` for offline forensics

---

## XII. Platform Integrations

arifosmcp is **MCP 2025-11-25 compliant** and works with any MCP-compatible client:

| Platform | Transport | Status |
|----------|-----------|--------|
| Anthropic Claude API | Streamable HTTP | ✅ Compatible |
| OpenAI Responses API | Streamable HTTP | ✅ Compatible |
| Google Gemini SDK | HTTP | ✅ Compatible |
| Claude Desktop | stdio (local) or HTTP (remote) | ✅ Compatible |
| Cursor / Windsurf | Streamable HTTP | ✅ Compatible |
| MCP Inspector | Streamable HTTP | ✅ Compatible |
| Agent-to-Agent (A2A) | `arifosmcp/runtime/a2a/` | ✅ Active |
| WebMCP (P2P) | `arifosmcp/runtime/webmcp/` | ✅ Active |
| ACP (Editor) | `arifosmcp/transport/acp_server.py` | ✅ Active |

**Full integration guide:** [`INTEGRATIONS.md`](./INTEGRATIONS.md)

---

## XIII. Developer Quick-Start

> **Python ≥ 3.12 required.**

### Install from PyPI

```bash
pip install arifosmcp
```

PyPI: https://pypi.org/project/arifosmcp/

### Live MCP Endpoint

```
https://arifosmcp.arif-fazil.com/mcp
```

Authentication: Authentik SSO at `auth.arif-fazil.com`

### Install for Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run MCP server (stdio mode)
python -m arifosmcp.runtime

# Run MCP server (HTTP mode, port 8080)
python -m arifosmcp.runtime sse

# Quick smoke test
pytest tests/test_mcp_quick.py -v

# Full test suite
pytest tests/ -v
```

### Connect to the live server

```python
import anthropic

client = anthropic.Anthropic()
response = client.beta.messages.create(
    model="claude-opus-4-5",
    max_tokens=4096,
    tools=[{
        "type": "mcp",
        "name": "arifos",
        "url": "https://arifosmcp.arif-fazil.com/mcp",
    }],
    messages=[{"role": "user", "content": "What is the current APEX G score?"}],
    betas=["mcp-client-2025-04-04"],
)
```

### Minimal constitutional call

```json
{
  "mode": "init",
  "payload": {
    "actor_id": "your_agent_id",
    "intent": {
      "query": "Analyse the system state",
      "task_type": "analyze",
      "reversibility": "auditable"
    }
  },
  "dry_run": false,
  "allow_execution": true
}
```

### Lint and test

```bash
ruff check .           # Linting (E, F, I, UP, N, B rules)
black --check .        # Format check
pytest tests/ -v       # Full suite (asyncio_mode=auto, no @pytest.mark.asyncio needed)
```

---

## XIV. Epochs of the Forge

| Epoch | Name | Key Milestone |
|-------|------|---------------|
| 1 | **Void** | APEX Theory drafted in a local notebook |
| 2 | **Sense** | First Python scripts for prompt engineering automation |
| 3 | **Reason** | Trinity model introduced (AGI Mind / ASI Heart / APEX Soul) |
| 4 | **Align** | 13 Floors codified as a mathematical constitution |
| 5 | **Forge** | First VPS deployment on port 8080 |
| 6 | **Audit** | Tri-Witness integration + OutcomeLedger |
| 7 | **Seal** | March 2026: A-RIF finalized, 11-tool surface locked, Quantum Memory Hardening (H1–H9), AAA HuggingFace dataset published, CI infrastructure patched, **4-Layer Model Registry (Catalog/Souls/Models/Profiles) + Hardened 3-Layer Identity Handshake.** |

### Epoch 7 Operational Timeline

| Date | Event |
|------|-------|
| 2026-03-22 | Rescued VPS from 9.2 GB Tectonic Crash |
| 2026-03-23 | Stabilised 193 GB Bedrock, migrated core to `/srv/arifosmcp` |
| 2026-03-24 | Repository unified (collapsed AAA/ shadow workspace) |
| 2026-03-24 | A-RIF Formal Specification sealed (`spec/ARIF_FORMAL_SPEC.md`) |
| 2026-03-24 | Substrate Controller hardened (auto-risk detection + 888_HOLD) |
| 2026-03-25 | AAA Wire elevated to AGPL-3.0 reference implementation |
| 2026-03-25 | Quantum Memory Hardening H1–H9 landed |
| 2026-03-25 | A-RIF Constitutional RAG — 186 canons loaded from HuggingFace |
| 2026-03-25 | CI infrastructure audit — 8 workflow files patched |
| 2026-03-25 | 11-tool surface locked, EXPECTED_TOOL_COUNT=11 assertion added |
| 2026-03-26 | Merged Quantum Memory Hardening SEAL (PR #288) into main |
| 2026-03-28 | Hardened Model Registry (v2) implemented with 17 Behavioral Souls |
| 2026-03-28 | Hardened 3-Layer Identity Handshake (Flavor/Law/Mission) landed in `init_000` |

---

## XV. Licensing Model

arifOS operates as two legally distinct layers with complementary licences:

| Layer | Repository / Path | Licence | Intent |
|-------|-------------------|---------|--------|
| **Standard** | `STANDARD.v1.md`, `arifos.standard.v1.json` | CC0 1.0 | Public domain — implement freely, no attribution required |
| **Theory & doctrine** | This repo (`ariffazil/arifOS`) | CC0 1.0 | Public domain — cite freely |
| **Reference implementation** | `arifosmcp/` | AGPL-3.0-only | Open-source with network copyleft |

**Rule of thumb:** The *idea* (standard) is free for everyone. The *machine* (runtime) is open-source, copyleft.

Full model: [`LICENSING.md`](./LICENSING.md)

---

## Live Endpoints

| Service | URL |
|---------|-----|
| MCP endpoint | `https://arifosmcp.arif-fazil.com/mcp` |
| Health + capability map | `https://arifosmcp.arif-fazil.com/health` |
| Tool explorer | `https://arifosmcp.arif-fazil.com/tools` |
| Grafana monitoring | `https://monitor.arifosmcp.arif-fazil.com` |
| arifOS docs | `https://arifos.arif-fazil.com` |
| APEX Theory | `https://apex.arif-fazil.com` |

---

## Key Files at a Glance

| File | Purpose |
|------|---------|
| `arifosmcp/runtime/tool_specs.py` | Canonical 11 mega-tool definitions |
| `arifosmcp/core/shared/physics.py` | G, W₃, ΔS, Ω₀, P², κᵣ implementations |
| `arifosmcp/core/pipeline.py` | `forge()` / `quick()` pipeline entrypoints |
| `arifosmcp/core/governance_kernel.py` | Kernel facade (state transitions + hold/void) |
| `arifosmcp/core/shared/verdict_contract.py` | VOID→SABAR normalisation |
| `arifosmcp/intelligence/constitutional_rag.py` | A-RIF Constitutional RAG loader |
| `arifosmcp/agentzero/escalation/hold_state.py` | GlobalAnchorHoldRegistry |
| `arifosmcp/runtime/tools_hardened_dispatch.py` | Substrate policy + 888_HOLD |
| `VAULT999/vault999.jsonl` | Immutable sealed verdict ledger |
| `spec/arifos.standard.v1.json` | Machine-readable constitutional schema |
| `POSITIONING.md` | Four declarations of what arifOS is |
| `CHANGELOG.md` | Full version history |
| `ROADMAP.md` | Horizon 1/2/3 engineering plan |

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**

*Author: Muhammad Arif bin Fazil*  
*Sealed: 2026-03-28 | Version: 2026.03.28*  
*ZKPC Root: 3-layer-binding-v2026.03.28*  
*Tri-Witness: Theory ✓ · Law ✓ · Intent ✓*
