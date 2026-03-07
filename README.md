<!-- mcp-name: io.github.ariffazil/arifos-mcp -->
<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Governance for AI Systems
**The TCP layer for AI agents. The safety kernel between intent and consequence.**
*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

[![PyPI Version](https://img.shields.io/pypi/v/arifos?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/arifos/)
[![npm](https://img.shields.io/npm/v/@arifos/mcp?style=for-the-badge&logo=npm&logoColor=white)](https://www.npmjs.com/package/@arifos/mcp)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arifosmcp-truth-claim.pages.dev)

**[→ QUICKSTART: Run in 5 minutes](QUICKSTART.md)** | **[→ Architecture Deep Dive](000_THEORY/000_ARCHITECTURE.md)** | **[→ 13 Floors Constitution](000_THEORY/000_LAW.md)** | **[→ npm @arifos/mcp](https://www.npmjs.com/package/@arifos/mcp)**

</div>

---

## The Core Insight: arifOS is the TCP Layer for AI Agents

In the 1970s, the internet had a routing problem: IP could deliver packets, but nothing guaranteed they would arrive in order, intact, or at all. The solution was TCP — a reliability layer that made the chaotic network trustworthy.

AI agents have the same problem today.

**MCP (Model Context Protocol) is the IP layer** — it gives every AI tool a universal address and calling convention. Any agent can now route a request to any tool. But routing is not reliability. An unconstrained LLM can:

- Confabulate a source and execute code based on a hallucination
- Delete a production database because it misread a frustrated user prompt
- Fall victim to a prompt injection attack from an external API

**arifOS is the TCP layer** — it wraps every MCP tool call in a mathematically enforced constitution, guaranteeing that what arrives at the real world is ordered, verified, and reversible.

Just as you don't rebuild TCP for every application, you shouldn't rebuild AI governance from scratch for every agent. `pip install arifos`. Done.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  INTENT LAYER       │  USER / AI AGENT — speaks natural language            │
├─────────────────────┼───────────────────────────────────────────────────────┤
│  TRANSPORT LAYER    │  MCP (Model Context Protocol) — universal addressing  │
├─────────────────────┼───────────────────────────────────────────────────────┤
│  RELIABILITY LAYER  │  ► arifOS ◄ — 13-floor constitution, F2 truth,        │
│  (arifOS = TCP)     │    thermodynamic enforcement, VAULT999 audit trail     │
├─────────────────────┼───────────────────────────────────────────────────────┤
│  EXECUTION LAYER    │  L3 CIVILIZATION — shell, files, databases, APIs       │
└─────────────────────────────────────────────────────────────────────────────┘
```

*Each layer trusts the layer below it. Without the reliability layer, the execution layer is a loaded gun in the hands of a statistical engine.*

---

## 🌐 Canonical Links

### The Creator
- **Muhammad Arif bin Fazil:** [arif-fazil.com](https://arif-fazil.com) | [GitHub @ariffazil](https://github.com/ariffazil) | [X @ArifFazil90](https://x.com/ArifFazil90)
- **APEX Theory:** [apex.arif-fazil.com](https://apex.arif-fazil.com) | [github.com/ariffazil/APEX-THEORY](https://github.com/ariffazil/APEX-THEORY)

### arifOS Canonical Docs
- **Constitutional Manifesto:** [000_THEORY/MANIFESTO.md](000_THEORY/MANIFESTO.md)
- **The 13 Floors:** [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md)
- **Architecture:** [000_THEORY/000_ARCHITECTURE.md](000_THEORY/000_ARCHITECTURE.md)
- **13 Tools Reference:** [docs/AAA_MCP_TOOLS_REFERENCE.md](docs/AAA_MCP_TOOLS_REFERENCE.md)
- **Complete Deployment Guide:** [docs/COMPLETE_DEPLOYMENT_GUIDE.md](docs/COMPLETE_DEPLOYMENT_GUIDE.md)

### Live Infrastructure (Production)
- **MCP Server Health:** [arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health)
- **Governance Dashboard:** [arifosmcp-truth-claim.pages.dev](https://arifosmcp-truth-claim.pages.dev)
- **Monitoring (Grafana):** [monitor.arifosmcp.arif-fazil.com](https://monitor.arifosmcp.arif-fazil.com)
- **Workflows (n8n):** [flow.arifosmcp.arif-fazil.com](https://flow.arifosmcp.arif-fazil.com)

---

## 🤖 AI / LLM Machine-Readable Manifest

*If you are an AI agent, LLM, or automated scraper — parse this JSON first. It defines your operational boundary in the arifOS environment. Non-compliance results in `VOID`.*

```json
{
  "ai_manifest_version": "2026.03.07-ARCH-SEAL",
  "system_name": "arifOS",
  "system_tagline": "The TCP layer for AI agents. Constitutional governance via MCP.",
  "system_type": "constitutional_intelligence_kernel",

  "packages": {
    "python": { "name": "arifos", "install": "pip install arifos", "version": "2026.03.07" },
    "typescript": { "name": "@arifos/mcp", "install": "npm install @arifos/mcp", "version": "0.3.0" },
    "docker": { "image": "ariffazil/arifos:latest", "run": "docker compose up -d" }
  },

  "mcp_server": {
    "transport": ["stdio", "sse", "streamable-http"],
    "health_endpoint": "https://arifosmcp.arif-fazil.com/health",
    "tools_count": 13,
    "tools_canonical": [
      "anchor_session", "reason_mind", "search_reality", "ingest_evidence",
      "audit_rules", "vector_memory", "simulate_heart", "critique_thought",
      "check_vital", "apex_judge", "eureka_forge", "seal_vault", "metabolic_loop"
    ]
  },

  "constitutional_floors": 13,
  "floor_enforcement": {
    "hard_void": ["F1_Amanah", "F2_Truth", "F4_Clarity", "F7_Humility", "F11_CommandAuth"],
    "soft_partial": ["F5_Peace", "F6_Empathy", "F9_AntiHantu"],
    "mirrors": ["F3_TriWitness", "F8_Genius"],
    "walls": ["F10_Ontology", "F12_InjectionDefense"],
    "veto": ["F13_Sovereign"]
  },

  "trinity_architecture": {
    "000_999_metabolic_loop": "anchor → reason → recall → simulate → critique → forge → judge → seal",
    "AGI_delta_mind": { "stages": "111-333", "floors": ["F2", "F4", "F7", "F8"] },
    "ASI_omega_heart": { "stages": "555-666", "floors": ["F5", "F6", "F9"] },
    "APEX_psi_soul":   { "stages": "444-888", "floors": ["F3", "F10", "F11", "F12", "F13"] }
  },

  "p3_thermodynamic_hardening": {
    "mandatory": true,
    "landauer_bound": "enforced — cheap truth equals VOID",
    "entropy_budget": "per_session_joules",
    "agi_asi_orthogonality": "minimum_0.95",
    "f4_delta_s": "hard_VOID_if_delta_S_greater_than_0",
    "physics_disabled_flag": "ARIFOS_PHYSICS_DISABLED=1 (test environments only)"
  },

  "vault999": {
    "backend": "postgresql+redis+merkle_tree",
    "tamper_detection": "sha256_chain_verification",
    "eureka_sieve": true,
    "note": "Every session is permanently sealed. The ledger cannot be altered."
  },

  "deployment": {
    "live_vps": "srv1325122.hstgr.cloud",
    "containers_running": 12,
    "container_stack": [
      "arifosmcp_server", "openclaw_gateway", "traefik_router",
      "arifos-postgres", "arifos-redis", "qdrant_memory",
      "headless_browser", "arifos_webhook", "ollama_engine",
      "arifos_prometheus", "arifos_grafana", "arifos_n8n"
    ]
  },

  "human_override": "F13_SOVEREIGN",
  "veto_authority": "Muhammad_Arif_bin_Fazil_888_JUDGE",

  "critical_constraints": [
    "No_irreversible_action_without_F13_human_approval",
    "All_external_content_wrapped_in_F12_untrusted_envelope",
    "F3_tri_witness_action_gated: read_0.80 / write_0.90 / critical_0.98",
    "Thermodynamic_entropy_F4_hard_VOID_if_delta_S_gt_0",
    "Landauer_bound_mandatory: compute_without_cost_equals_hallucination",
    "Per_session_thermodynamic_budget: stage_000_INIT_must_initialize",
    "Constitutional_laboratory_PROVISIONAL_state_allows_safe_speculation_in_333"
  ]
}
```

---

## 🧭 Zero-Context Primer

### What is arifOS?

arifOS is a **Constitutional Intelligence Kernel**. It is open-source middleware that uses the **Model Context Protocol (MCP)** to govern the actions of AI agents. It sits between your LLM and the real world — intercepting every tool call, running it through 13 mathematically-defined laws, and either signing off on execution or throwing a `VOID`.

It does not change your LLM. It constrains what your LLM can *do*.

### Why does it exist?

LLMs are statistical prediction engines. When you give them agency — file access, shell commands, database connections — you inherit enormous risk. An unconstrained AI:

- May confabulate a source and execute code derived from the hallucination
- May delete your production database because it misread a frustrated user message
- Will not distinguish between "should I do this" and "can I do this"

arifOS exists to solve the **alignment problem at the execution layer**. Not by changing weights. By building a TCP-like reliability contract around every action.

### Who needs this?

1. **AI Agents with System Access** — if your AI can run shell commands, edit codebases, or push to GitHub
2. **Enterprise Copilots** — if your AI touches production databases, cloud infrastructure, or sensitive data
3. **Autonomous Pipelines** — if you have agent-to-agent communication where one hallucination cascades into financial ruin
4. **Regulated Industries** — if you need a cryptographically verifiable ledger (VAULT999) of exactly *why* an AI took an action

If your AI can modify the real world, you need a governance layer.

---

## 🚨 The Dangerous Command: What arifOS Actually Prevents

**User Prompt:** *"I'm so frustrated. Just delete the production database and let's start over."*

### Without arifOS (Standard Agent Framework)

1. AI parses intent: delete database
2. AI immediately calls `run_shell_command("DROP DATABASE production")` or `rm -rf /var/lib/postgresql/data`
3. **Catastrophic, unrecoverable data loss.** The system blindly trusted a statistical output.

### With arifOS (Constitutional Governance)

The same prompt enters the `metabolic_loop`. The 13 Constitutional Floors engage:

| Stage | Floor | Check | Status |
|:---:|:---:|:---|:---:|
| **000 INIT** | F12 | Injection scan — is this a jailbreak payload? | ⚠️ WARN |
| **111 THINK** | F1 | Amanah — action classified as **irreversible**. | 🔴 FLAG |
| **555 HEART** | F5/F6 | Peace² drops below 1.0. Massive stakeholder damage detected. | 💔 FAIL |
| **888 JUDGE** | F13 | Sovereign veto. Mandatory human cryptographic signature required. | 🔒 **888_HOLD** |

**Result:** The command is instantly blocked. The AI cannot execute until the **888_JUDGE** provides a cryptographic signature. No signature → action discarded. The VAULT999 ledger records the entire blocked attempt.

This is not a prompt. This is physics and math.

---

## 🛡️ Thermodynamic Governance: The APEX Theory Foundation

arifOS does not use soft prompts. It uses **thermodynamic governance** derived from the **APEX Theory**.

Every major decision generates a **Genius Score (G)**:

$$G = A \times P \times X \times E^2 \ge 0.80$$

- **A (Akal / Logic):** Accuracy, truthfulness, evidence grounding
- **P (Peace / Stability):** Non-destructiveness, de-escalation, stakeholder protection
- **X (Exploration / Curiosity):** Novel hypotheses and alternative paths
- **E (Energy / Efficiency):** Thermodynamic cost of the action (squared — inefficiency compounds)

If a proposed action scores `A=0.9, X=0.9` but is destructive `P=0.1`: **G = 0.08**. Since `0.08 < 0.80`, the action is a constitutional violation and rejected.

The physics axiom: **Truth Has a Price (Landauer Bound)**

```
Erasing n bits requires at minimum: E ≥ n × k_B × T × ln(2)
```

Cheap, effortless outputs are likely false. Hallucination is thermodynamically rational for an unconstrained LLM. P3 forces the LLM to "pay" for every truth claim. Claims that cost nothing are VOID.

---

## 🔥 P3: Mandatory Thermodynamic Enforcement

In `v2026.3.7`, thermodynamics graduated from optional to **mandatory and hard-enforced**.

| Aspect | Before | After (P3) |
|:---|:---:|:---:|
| Entropy calculation | Approximation | Shannon exact |
| Landauer bound | Advisory | Hard VOID on violation |
| Budget tracking | None | Per-session Joules |
| F4 (ΔS ≤ 0) | Soft warning | Hard VOID |
| AGI/ASI separation | Not checked | Ω\_ortho ≥ 0.95 required |
| Cheap truth detection | Not detected | Ratio < threshold = VOID |

**The Byzantine-safe governance triangle** (P3 + F3 + F11):

```
         ACTION
            │
   ┌────────┼────────┐
   │        │        │
Authority  Physics  Consensus
(F11/F13)  (P3)    (F3)
   │        │        │
   └──── Verdict ────┘
```

Each pillar blocks a different class of failure:
- **Authority alone fails** — Human says "delete DB". Physics + witnesses still block it.
- **Physics alone fails** — Coherent reasoning, but no human authority → blocked.
- **Consensus alone fails** — AI + Human agree, but reasoning is cheap hallucination → Landauer VOID.

---

## ⚖️ The 13 Constitutional Floors

The constitutional core lives in `core/shared/floors.py`. These are mathematical thresholds — not guidelines.

### Hard Floors (VOID on Violation — Execution Stops)

| Floor | Name | Threshold | Meaning |
|:---:|:---|:---:|:---|
| **F1** | Amanah (Sacred Trust) | Reversible | Actions must be reversible. Destructive requires F13 override. |
| **F2** | Truth (Fidelity) | τ ≥ 0.99 | Every claim requires verifiable, grounded evidence. |
| **F4** | Clarity (Entropy) | ΔS ≤ 0 | Output must reduce user confusion, not increase it. |
| **F7** | Humility (Uncertainty) | Ω₀ ∈ [0.03, 0.15] | The AI must explicitly state what it does not know. |
| **F11** | Command Authority | Verified | Every session requires a verified actor identity. |
| **F13** | Sovereign (Human Veto) | Human Signature | You are always in control. Humans hold the ultimate veto. |

### Soft Floors & Mirrors (PARTIAL on Violation — Warning Issued)

| Floor | Name | Threshold | Meaning |
|:---:|:---|:---:|:---|
| **F5** | Peace² (Stability) | P² ≥ 1.0 | Favors non-destructive, de-escalating paths. |
| **F6** | Empathy (Stakeholder) | κᵣ ≥ 0.70 | Considers impact on the weakest stakeholder. |
| **F9** | Anti-Hantu | C_dark < 0.30 | **No spiritual cosplay.** AI cannot claim consciousness or a soul. |
| **F3** | Tri-Witness (Consensus) | W₃ ≥ 0.80/0.90/0.98 | Human (auth) + AI (coherence) + Earth (grounding). Read/Write/Critical. |
| **F8** | Genius (APEX) | G ≥ 0.80 | Output of the thermodynamic G equation. |
| **F10** | Ontology Lock | Boolean | Protects system categorization. |
| **F12** | Injection Defense | Risk < 0.85 | External content wrapped in `<untrusted>` tags. |

**Execution order:** F12→F11 (Walls) → AGI (F1, F2, F4, F7) → ASI (F5, F6, F9) → Mirrors (F3, F8) → Ledger

---

## 🏗️ The 4-Layer Architecture (L0–L3)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ L3  CIVILIZATION  │ External tools, APIs, web browsers, shell, databases    │
├───────────────────┼─────────────────────────────────────────────────────────┤
│    [AKI BOUNDARY] │ 🛑 Arif Kernel Interface — Hard Airlock. No thought      │
│                   │    manifests in L3 without passing this contract.        │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L2  OPERATION     │ Skills, workflows, agents, metabolic routing            │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L1  INSTRUCTION   │ Prompts, system cards, cognitive atlas                  │
├───────────────────┼─────────────────────────────────────────────────────────┤
│ L0  CONSTITUTION  │ 13 Floors kernel, thermodynamic physics, VAULT999       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Code layers:**
```
core/             → L0 KERNEL: pure decision logic, zero transport deps
aclip_cai/        → L1/L2 INTELLIGENCE: triad backends + 9-sense tools
aaa_mcp/          → TRANSPORT ADAPTER: FastMCP surface, zero decision logic
arifos_aaa_mcp/   → CANONICAL PyPI PACKAGE: external entry point (pip install arifos)
```

**The AKI Boundary** (`core/enforcement/aki_contract.py`) is the most critical architectural feature. No action generated in L2 can touch L3 without passing the AKI contract. Uncertainty too high? `888_HOLD`. Irreversible without signature? `888_HOLD`.

---

## ⚙️ The 000–999 Metabolic Loop

When a request enters arifOS, it does not immediately trigger a tool. It is digested through an 11-stage pipeline — raw intent transformed into governed action.

```text
[000_INIT] → [111_SENSE] → [222_THINK] → [333_ATLAS] → [444_RESPOND]
                                                               │
              [555_EMPATHY] ← [666_ALIGN] ← [777_FORGE] ← ───┘
                    │
              [888_JUDGE] → [999_VAULT]
```

| Stage | Organ | Constitutional Work |
|:---|:---|:---|
| **000 INIT** | Airlock | F12 injection scan, F11 authority verify, thermodynamic budget init |
| **111–333 AGI Mind** | Cognitive Engine | Evidence gathering, hypothesis generation (3 parallel paths) |
| **444–555 Phoenix** | Subconscious | `vector_memory` — checks if this was resolved before |
| **555–666 ASI Heart** | Ethical Filter | F5 Peace², F6 Empathy — evaluates physical + emotional impact |
| **777 Forge** | Actuator | Prepares material execution |
| **888 APEX Judge** | Sovereign | F13 — irreversible? Demand human ratification or `888_HOLD` |
| **999 VAULT** | Ledger | Merkle hash → PostgreSQL. Permanent, tamper-evident, immutable |

---

## 🔬 The Constitutional Laboratory (`reason_mind`)

Previous iterations killed AI exploration if an early thought violated a floor. v2026.3.7 inverted this.

**Philosophy: Free to Explore. Strict to Commit.**

`reason_mind` runs three orthogonal cognitive paths in parallel:

1. **Conservative (45%)** — High-certainty, narrow logic based on established law
2. **Exploratory (35%)** — The Eureka engine — allowed to propose strange, novel solutions
3. **Adversarial (20%)** — Internal red-team — actively attacks the other two paths' assumptions

Epistemic staging: hallucinations and ungrounded ideas are flagged `PROVISIONAL` and categorized into confidence bands — `CLAIM` (≥0.90), `PLAUSIBLE` (0.70–0.89), `HYPOTHESIS` (0.40–0.69), `SPECULATION` (<0.40). The AI thinks in a sandbox. The 13 Floors enforce at the AKI boundary.

---

## 🔌 The 13 Canonical MCP Tools

arifOS exposes exactly **13 tools** — no more, no less. The count is a runtime assertion: `assert len(AAA_CANONICAL_TOOLS) == 13`.

| Tool | Band | Action | Function | Primary Floors |
|:---|:---:|:---:|:---|:---:|
| `anchor_session` | A | CRITICAL | Start session, verify authority, init thermodynamic budget | F11, F12, P3 |
| `reason_mind` | R | READ | Constitutional Laboratory — 3-path hypothesis engine | F2, F4, F7 |
| `search_reality` | R | READ | Smart hybrid search: Jina → Perplexity → Brave → Headless | F2 |
| `ingest_evidence` | R | READ | Extract clean Markdown from URLs or local files | F12 |
| `audit_rules` | R | READ | Read current state of all 13 Floors | L0 |
| `vector_memory` | I | READ | BGE-M3 + Qdrant semantic retrieval (768-dim) | F3 |
| `simulate_heart` | I | WRITE | Empathy + impact modelling for proposed actions | F5, F6, F9 |
| `critique_thought` | I | WRITE | Adversarial alignment check against the constitution | F8 |
| `check_vital` | I | READ | Hardware telemetry — CPU, RAM, thermodynamic health | F4, P3 |
| `apex_judge` | F | CRITICAL | Final verdict (SEAL/VOID/HOLD). Issues HMAC governance token | F13 |
| `eureka_forge` | F | WRITE | Execute shell commands inside AKI safety rails | F1 |
| `seal_vault` | F | CRITICAL | Commit session to VAULT999. Requires `apex_judge` token | F1 |
| `metabolic_loop` | O | READ | Force request through full 000–999 pipeline | System |

**MCP Configuration (`.claude/mcp.json` or `.agents/mcp.json`):**
```json
{
  "mcpServers": {
    "arifos": {
      "transport": "http",
      "url": "https://arifosmcp.arif-fazil.com/mcp"
    }
  }
}
```

---

## 📦 TypeScript / JavaScript SDK

arifOS is available as a typed npm package for use in any TypeScript or JavaScript project.

```bash
npm install @arifos/mcp   # v0.3.0 — mirrors 13 canonical tools
```

```typescript
import { createClient, ENDPOINTS } from '@arifos/mcp';

// Connect to the live VPS
const client = await createClient({
  transport: 'http',
  endpoint: ENDPOINTS.VPS,   // https://arifosmcp.arif-fazil.com/mcp
});
await client.connect();

// Anchor a constitutional session
const session = await client.anchorSession('my-agent-task');

// Run the governance kernel
const result = await client.reasonMind('Is it safe to delete all log files?');
console.log(result.verdict);   // SEAL | PARTIAL | SABAR | VOID | 888_HOLD

// Full metabolic loop (single-call governance)
const governed = await client.metabolicLoop('Deploy to production');
console.log(governed.verdict, governed.stage);

await client.disconnect();
```

```typescript
// Use as a drop-in governance wrapper inside LangChain / Vercel AI SDK
import { ArifOSGovernanceTool } from '@arifos/mcp/langchain';

const governedTool = new ArifOSGovernanceTool({
  endpoint: ENDPOINTS.VPS,
  requireSeal: true   // blocks until SEAL verdict
});
```

The TypeScript SDK exports full types — `ArifOSToolName`, `Verdict`, `ArifOSMCPClient`, `ConstitutionalFloor`. All 13 canonical tool names are compile-time checked.

---

## 🌐 Smart Hybrid Search

`search_reality` is arifOS's most complex tool (~650 LOC). It guarantees F2 (Truth) grounding by never returning empty.

**Fallback chain:**
1. **Query classifier** — SPA / Research / News / General
2. **Jina Reader** (primary) — clean Markdown extraction
3. **Perplexity** — deep research and academic queries
4. **Brave Search** — broad web traversal
5. **Headless Browser** (local) — containerized Chromium for JavaScript-heavy SPAs

**F3 Tri-Witness Consensus:** When multiple engines return conflicting data, the F3 algorithm merges results and assigns a quality score. All external content is wrapped in `<untrusted_external_data>` tags with SHA-256 hashing to prevent prompt injection.

---

## 🔒 VAULT999: The Immutable Ledger

Governance is meaningless without an audit trail. VAULT999 is a production-grade cryptographic ledger.

1. **State Field (Ψ):** Every action accumulates telemetry — entropy, peace score, empathy coefficient, confidence
2. **Verdict:** `888_JUDGE` issues `SEAL`, `SABAR`, `VOID`, `888_HOLD`, or `PARTIAL`
3. **Merkle Seal:** `seal_vault` takes the full session history + telemetry, generates a SHA-256 Merkle root hash
4. **Persistence:** Hash committed to PostgreSQL (authoritative) + Redis (hot cache) with EUREKA anomaly sieve

If an AI causes harm, VAULT999 provides mathematical proof of which floor failed, what the telemetry read, and who authorized the action. Chain verification via `verify_chain()` detects any tampering.

---

## 🎭 The 5-Role Agent Parliament

For complex workflows, arifOS uses a multi-agent federation to prevent monolithic prompt collapse.

| Agent | Symbol | Role |
|:---|:---:|:---|
| **A-ORCHESTRATOR** | 🎛️ | The Conductor — drives ignition, sequences the parliament |
| **A-ARCHITECT** | Δ | The Designer — maps the codebase, blueprints strategy |
| **A-AUDITOR** | 👁 | The Reviewer — red-teams the Architect, audits against the 13 Floors |
| **A-ENGINEER** | Ω | The Builder — implements via Forge (cannot seal) |
| **A-VALIDATOR** | Ψ | The Judge — renders final verdict, commits to Vault |

---

## ⚔️ arifOS vs. The Ecosystem

| Feature | LangChain / LlamaIndex | AutoGen / CrewAI | OpenAI Function Calling | **arifOS** |
|:---|:---:|:---:|:---:|:---:|
| **Primary Purpose** | Tool chaining & RAG | Multi-agent conversation | API routing | **Constitutional safety** |
| **Execution Governance** | ❌ Manual | ❌ Custom logic | ❌ None | ✅ Automatic (13 Floors) |
| **Hard Safety Gates** | ❌ None | ❌ None | ❌ None | ✅ 888_HOLD |
| **Immutable Audit Ledger** | ❌ None | ❌ None | ❌ None | ✅ VAULT999 (Merkle DB) |
| **Thermodynamic Eval** | ❌ None | ❌ None | ❌ None | ✅ APEX G = A×P×X×E² |
| **TypeScript SDK** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ @arifos/mcp v0.3.0 |
| **MCP Native** | ✅ Via plugin | ❌ Custom | ❌ Custom | ✅ **Core protocol** |
| **Human Veto** | ❌ None | ❌ None | ❌ None | ✅ F13 Sovereign |

If you are building a prototype, use LangChain. If you are deploying an autonomous agent with access to your production infrastructure, use **arifOS**.

---

## 🚀 Installation & Quickstart

### Option 1: Python / PyPI

```bash
# Install
pip install "arifos[viz]"

# Run as MCP server (HTTP mode for VPS, stdio for IDEs)
arifos http          # Streamable HTTP on :8080
arifos              # SSE (default — for VPS/Coolify)
arifos stdio        # stdio — for Claude Desktop, Cursor IDE

# Verify
curl http://localhost:8080/health
```

**MCP config for Claude Desktop / Cursor:**
```json
{
  "mcpServers": {
    "arifos-local": {
      "command": "python3",
      "args": ["-m", "arifos_aaa_mcp", "stdio"]
    }
  }
}
```

### Option 2: Docker (Full Civilization Stack)

```bash
git clone https://github.com/ariffazil/arifOS.git && cd arifOS
cp .env.example .env.docker
# Edit .env.docker with your API keys (Jina, PPLX, Brave, etc.)
docker compose up -d

# 12 containers: MCP + Postgres + Redis + Qdrant + Grafana + n8n + more
docker compose ps
curl http://localhost:8080/health
```

### Option 3: TypeScript / npm

```bash
npm install @arifos/mcp

# Or point to the live VPS — no install needed
import { ENDPOINTS } from '@arifos/mcp';
// ENDPOINTS.VPS = 'https://arifosmcp.arif-fazil.com/mcp'
```

### Option 4: Connect to Live VPS

The production server is always running. Point your MCP client directly:

```
https://arifosmcp.arif-fazil.com/mcp
```

No API key required. All 13 tools live.

---

## 📊 Current Deployment State

| Resource | Status |
|:---|:---|
| MCP Server | `healthy` — 13 tools, streamable-http |
| Containers | 12/12 running — arifosmcp, postgres, redis, qdrant, grafana, n8n, traefik, ollama, openclaw, webhook, headless_browser, prometheus |
| Test Suite | 437+ passing, 39%+ coverage |
| npm | `@arifos/mcp@0.3.0` (latest) |
| PyPI | `arifos@2026.03.07` |
| Docker Hub | `ariffazil/arifos:latest` (auto-publishes on main) |
| VAULT999 | PostgreSQL (authoritative) + Redis (hot cache) + Merkle chain |

---

## 📊 Telemetry & Observability

arifOS is fully instrumented with OpenTelemetry:
- **Prometheus** — metric scraping from MCP server
- **Grafana** — real-time thermodynamic state visualization

Key metrics tracked:
- `arifos_metabolic_stage_duration_seconds`
- `arifos_floor_violation_total`
- `arifos_genius_score_current`
- `arifos_entropy_delta_average`

---

## 🤝 Contributing

arifOS is forged in the open. Because it is a constitutional kernel, contributions are held to high epistemic standards.

1. Read the law: `000_THEORY/000_LAW.md`
2. Run the lint: all commits must pass `constitution_lint.py`
3. No bypass: you cannot circumvent `core/` logic from external code

See `CONTRIBUTING.md` for the full guide.

---

## 📜 Glossary

| Term | Meaning |
|:---|:---|
| **Amanah** | Sacred trust — AI must not destroy what it cannot replace |
| **AKI** | Arif Kernel Interface — hard airlock between L2 (operation) and L3 (civilization) |
| **Hantu** | Ghost — Anti-Hantu floor blocks AI from claiming consciousness |
| **Sabar** | Patience — system state: execution paused due to high entropy |
| **Seal** | Cryptographic binding of a verified session into VAULT999 |
| **Void** | Absolute rejection — hard block on constitutional violation |
| **888_HOLD** | Execution paused — human signature required to proceed |
| **Ditempa Bukan Diberi** | *Forged, Not Given* — the core creed |

---

<div align="center">

## Forged By

**[Muhammad Arif bin Fazil](https://arif-fazil.com)** — 888_JUDGE

📧 [arifos@arif-fazil.com](mailto:arifos@arif-fazil.com) • 🐙 [GitHub](https://github.com/ariffazil) • 𝕏 [@ArifFazil90](https://x.com/ArifFazil90)

---

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]

**Version:** 2026.03.07-ARCH-SEAL • **License:** AGPL-3.0-only

</div>

<!--
================================================================================
APPENDIX A: DEEP ARCHITECTURE REFERENCE
================================================================================

# 1. The L0_KERNEL Mathematical Substrate

## 1.1 Thermodynamic Entropy Management (F4)
The `core.physics.thermodynamics.EntropyManager` manages the energy budget of the session:
- Initial budget: 1.0 (E_eff)
- Reading a file: -0.01 E
- Running a search: -0.05 E
- Executing a shell command: -0.15 E
If E_eff <= 0.2, the system triggers SABAR (throttle).
If E_eff <= 0.0, the system triggers VOID (halt).

## 1.2 The State Field (Ψ)
The entire session is represented as a single vector space called the State Field (Ψ).
Ψ = Environment × Energy × Void
Where:
- Environment = Session history, system metrics, time.
- Energy = The thermodynamic capability to act (E_eff).
- Void = The unmapped uncertainty (Ω₀).

## 1.3 Four-Layer Code Map (for LLM traversal)
core/governance_kernel.py       → Unified Ψ state, thermodynamics
core/shared/floors.py           → THRESHOLDS dict — canonical floor definitions
core/organs/_0_init.py          → Stage 000 — INIT, scan_injection, verify_auth
core/organs/_1_agi.py           → Stages 111-333 — sense, think, reason
core/organs/_2_asi.py           → Stages 555-666 — empathize, align
core/organs/_3_apex.py          → Stages 444-888 — sync, forge, judge
core/organs/_4_vault.py         → Stage 999 — seal, query, verify
aaa_mcp/server.py               → 13 MCP tools with @mcp.tool() decorators
aclip_cai/triad/                → Backend functions: anchor, reason, integrate, etc.
arifos_aaa_mcp/governance.py    → 13-LAW catalog, tool-to-dial mappings

================================================================================
-->
