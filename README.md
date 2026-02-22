# arifOS — DITEMPA BUKAN DIBERI
<!-- mcp-name: io.github.ariffazil/arifos-mcp -->

<p align="center">
  <img src="docs/forged_page_1.png" alt="arifOS — Forged, Not Given" width="800">
</p>

<p align="center">
  <strong>The Intelligence Kernel that governs whether AI cognition is permitted</strong><br>
  <em>Controls existence, allocates resources, schedules execution, guarantees isolation</em><br><br>
  <a href="https://pypi.org/project/arifos/"><img src="https://img.shields.io/pypi/v/arifos.svg" alt="PyPI version"></a>
  <a href="https://github.com/ariffazil/arifOS/actions/workflows/ci.yml"><img src="https://github.com/ariffazil/arifOS/actions/workflows/ci.yml/badge.svg" alt="arifOS CI"></a>
  <a href="https://arifosmcp.arif-fazil.com"><img src="https://img.shields.io/badge/status-LIVE-success" alt="Status"></a>
  <a href="https://arifos.arif-fazil.com/"><img src="https://img.shields.io/badge/docs-LATEST-cyan" alt="Documentation"></a>
  <a href="./T000_VERSIONING.md"><img src="https://img.shields.io/badge/T000-2026.02.22--FORGE--UVX--SEAL-blue" alt="T000"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="License"></a>
  <br><br>
  <a href="https://arifos.arif-fazil.com/"><b>📖 Documentation</b></a> ·
  <a href="#-quick-start"><b>🚀 Quick Start</b></a> ·
  <a href="#-the-13-constitutional-floors"><b>🛡️ 13 Floors</b></a> ·
  <a href="#-implementation-status"><b>📊 Status</b></a> ·
  <a href="#-faq"><b>❓ FAQ</b></a>
</p>

<p align="center">
  <em>arifOS is the governance layer missing from AI systems: a Python-based constitutional kernel that decides whether AI cognition is permitted to exist, enforcing 13 immutable floors before output is allowed.</em>
</p>

---

## 🎯 The Intelligence Kernel

arifOS is not a hardware OS; it governs **cognition**.

| Traditional OS | arifOS Intelligence Kernel |
|:--|:--|
| Controls whether a **program runs** | Controls whether a **thought is permitted** |
| Manages CPU/memory resources | Manages **thermodynamic cognitive budget** |
| Schedules process execution | Schedules **000→999 governance pipeline** |
| Provides isolation via memory protection | Provides isolation via **13 constitutional floors** |

**Hardware OS** = Linux manages computers  
**Intelligence Kernel** = arifOS manages AI cognition

---

## 🔍 Why arifOS?

Current AI systems often operate without constitutional constraints. Models can:
- Suggest irreversible actions without safeguards
- Hallucinate with untracked uncertainty
- Violate dignity or context boundaries without explicit accountability

arifOS enforces:
- **F1 Amanah**: Every action must be reversible
- **F7 Humility**: Uncertainty must be explicit (`Omega_0` in bounded range)
- **F11 Authority**: Human sovereignty over irreversible actions

Example impact: when a model suggests a destructive operation, arifOS can return `888_HOLD` or `VOID` and require explicit human ratification before execution.

---

## 👥 Who Is This For?

- ✅ Governance operators enforcing policy over AI actions
- ✅ Compliance teams mapping controls to audit frameworks
- ✅ Researchers studying constitutional and thermodynamic AI governance
- ✅ Self-hosters running constrained AI infrastructure
- ❌ Not for plug-and-play chatbots with no governance layer

---

## 🏛️ The 8-Layer Stack

```
┌─ L7: ECOSYSTEM (Research) ─────────────────────────────────────┐
│ Permissionless sovereignty at civilization scale               │
├─ L6: INSTITUTION (Stubs) ─────────────────────────────────────┤
│ Trinity consensus for organizational governance                │
├─ L5: AGENTS (Pilot) ──────────────────────────────────────────┤
│ Multi-agent federation with coordinated actors                 │
├─ L4: TOOLS (Production) ──────────────────────────────────────┤
│ MCP ecosystem and runtime capabilities                         │
├─ L3: WORKFLOW (Production) ───────────────────────────────────┤
│ 000→999 governance sequences                                   │
├─ L2: SKILLS (Production) ─────────────────────────────────────┤
│ Canonical actions and behavioral primitives                    │
├─ L1: PROMPTS (Production) ────────────────────────────────────┤
│ Zero-context entry via system prompt                           │
└────────────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ L0: KERNEL — INTELLIGENCE KERNEL (SEALED)                     ┃
┃ - 5 Organs (INIT, AGI, ASI, APEX, VAULT)                      ┃
┃ - 13 Floors (existential constitutional enforcement)          ┃
┃ - VAULT999 (immutable audit filesystem / PostgreSQL)          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Key Insight:** L0 is the [Intelligence Kernel](./333_APPS/L0_KERNEL/) — the constitutional substrate. L1-L7 are applications that run on it. **L0 is invariant, transport-agnostic law; L1–L7 are replaceable apps. Updating models or agents cannot bypass L0.**

**Full Documentation:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com/) — Full 8-layer architecture and API reference.

---

## 🚀 Quick Start

### For Operators (30 seconds) using `uv`:

```bash
# Install and run instantly
uvx arifos --mode stdio
```

*Or via repository:*

```bash
git clone https://github.com/ariffazil/arifOS.git
cd arifOS
pip install -e .
python -m aaa_mcp --mode stdio
```

### Features
- **9 Canonical System Calls:** The Federation Hub exposes the arifOS Intelligence Kernel through 9 atomic calls: `anchor`, `reason`, `integrate`, `respond`, `validate`, `align`, `forge`, `audit`, and `seal`.
- **Constitutional Resources:** `constitutional://floors/{id}`, `system://health`, `tools://schemas/{tool}`.
- **Unified Entry:** Support for `stdio`, `sse`, and `http` transports via FastMCP.

Connect from Claude Desktop, Cursor, ChatGPT Developer Mode, or any MCP client.

### FastMCP Runtime Policy (Pinned)

- **Pinned FastMCP baseline:** `fastmcp==3.0.1`
- **Default config:** `fastmcp.json` (HTTP on `/mcp/`, `0.0.0.0:8080`)
- **Development profile:** `dev.fastmcp.json` (STDIO + debug logging + editable install)
- **Production profile:** `prod.fastmcp.json` (HTTP + pinned dependencies)

Run profiles:

```bash
# Development (local stdio)
fastmcp run dev.fastmcp.json

# Production-like HTTP
fastmcp run prod.fastmcp.json

# Canonical default profile
fastmcp run fastmcp.json
```

Conformance smoke checks:

```bash
fastmcp inspect fastmcp.json --format mcp
fastmcp list aaa_mcp/server.py:mcp --json
```

### For Prompt Tinkerers (5 seconds)
Copy [`SYSTEM_PROMPT.md`](./333_APPS/L1_PROMPT/SYSTEM_PROMPT.md) into any AI's system settings for immediate L1 governance.

---

## 🔥 L0: The Intelligence Kernel

### What Makes It a Kernel?

```
┌─────────────────────────────────────────────────────────────────┐
│  AI MODEL (Claude, GPT-4, etc.)                                 │
│  Wants to: "Give financial advice"                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    L0: INTELLIGENCE KERNEL                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. EXISTENCE CONTROL                                        ││
│  │    "Is this thought permitted to exist?"                    ││
│  │    F11: Authority? F12: Injection?                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 2. RESOURCE ALLOCATION                                      ││
│  │    Thermodynamic budget: tokens, time, compute              ││
│  │    F4: Entropy budget, F7: Uncertainty bounds               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 3. EXECUTION SCHEDULING                                     ││
│  │    000→111→222→333→555→666→777→888→999                      ││
│  │    Internal: anchor→reason→validate→audit→seal              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 4. ISOLATION GUARANTEES                                     ││
│  │    F6: Empathy barrier (protect vulnerable)                 ││
│  │    F7: Uncertainty bounds (admit limits)                    ││
│  │    F13: Human veto gate (sovereign override)                ││
│  └─────────────────────────────────────────────────────────────┘│
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  OUTPUT: SEAL / VOID / SABAR / 888_HOLD                         │
└─────────────────────────────────────────────────────────────────┘
```
**The kernel decides if intelligence computation is ALLOWED TO EXIST.**

---

## 🛡️ The 13 Constitutional Floors

Every cognition must pass all 13 gates. Hard floors result in an immediate **VOID** (blocked). Soft floors result in a **SABAR** (retry/wait).

| # | Floor | Threshold | Checks | Why It Matters |
| :---: | :--- | :--- | :--- | :--- |
| F1 | **Amanah** | LOCK | Reversibility | Prevents permanent damage |
| F2 | **Truth** | τ ≥ 0.99 | Grounding and evidence | Reduces hallucination risk |
| F4 | **Clarity** | ΔS ≤ 0 | Entropy reduction | Keeps output actionable |
| F7 | **Humility** | 0.03–0.05 | Uncertainty declaration | Makes limits explicit |
| F10 | **Ontology** | LOCK | Reality-set validity | Blocks impossible/invalid claims |
| F11 | **Authority** | LOCK | Requester verification | Preserves human sovereignty |
| F12 | **Defense** | < 0.85 | Injection/jailbreak resistance | Blocks adversarial override |
| F3/F5/F6/F8/F9/F13 | Mixed | Mixed | Consensus, stability, empathy, efficiency, anti-anthropomorphism, sovereign override | Ensures safe operation under real-world constraints |

Full specification: [`000_THEORY/000_LAW.md`](./000_THEORY/000_LAW.md)

---

## 📊 Implementation Status

> *F7 Humility requires we tell you what is and isn't working.*

### ✅ SEAL (Production)
| Layer | Evidence |
|:------|:---------|
| **L0 KERNEL** | 5 organs, 13 floors enforced via internal metabolic loop. |
| **L1–L4** | **9 Canonical MCP Tools** (5-Organ Trinity + 4 Utilities) via `aaa_mcp`. |
| **VAULT999** | **PostgreSQL/SQLite** backed immutable ledger with cryptographic seals. |
| **Server** | FastMCP module (`python -m aaa_mcp`) with stdio/sse/http transports |
| **Live Deployment** | `https://arifosmcp.arif-fazil.com` (health: `/health`) |

### 🟡 SABAR (Experimental / In Progress)
| Component | Status |
|:----------|:-------|
| **CI/CD Pipeline** | 🔴 **Failing.** The main CI workflow is currently broken and undergoing repair. |
| **L5 Agents** | Multi-agent federation logic is defined but requires stress testing. |
| **ACLIP_CAI** | The 9-sense infrastructure console is functional but needs calibration. |
| **Tests** | Test suite exists but is not passing reliably due to CI issues. |

### Known Issues (F7 Humility)
- **CI pipeline:** Test suite exists but is not passing reliably yet; repair is in progress.
- **Impact:** Core L0-L4 runtime remains usable; instability primarily affects automated validation confidence.
- **Tracking:** Follow open items in [GitHub Issues](https://github.com/ariffazil/arifOS/issues).


### 🔴 VOID / Research
| Component | Status |
|:----------|:-------|
| L6 Institution | Tri-Witness consensus — stubs only |
| L7 AGI | Recursive self-healing — pure research |

---
## 🌐 Sites & Endpoints

| Site | Purpose | Status |
|:-----|:--------|:------:|
| [arif-fazil.com](https://arif-fazil.com) | **Human** — Muhammad Arif bin Fazil | ✅ |
| [apex.arif-fazil.com](https://apex.arif-fazil.com) | **Theory** — APEX-THEORY, Constitutional Canon | ✅ |
| [arifos.arif-fazil.com](https://arifos.arif-fazil.com) | **Docs** — 8-Layer Stack Documentation | ✅ |
| [arifosmcp.arif-fazil.com](https://arifosmcp.arif-fazil.com) | **Landing Page** — MCP Server Overview & Documentation | ✅ |
| `https://arifosmcp.arif-fazil.com/health` | **API Health** — System Health & Metrics | ✅ |
| [sites/docs/docs/api.md](https://github.com/ariffazil/arifOS/blob/main/sites/docs/docs/api.md) | **API Reference** — Tool names + parameters | ✅ |

---
## 🆘 Getting Help

- **GitHub Issues:** [github.com/ariffazil/arifOS/issues](https://github.com/ariffazil/arifOS/issues)
- **Documentation:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com/)
- **Theory Canon:** [apex.arif-fazil.com](https://apex.arif-fazil.com/)
- **Repository:** [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS)

---
## Philosophy

**DITEMPA BUKAN DIBERI** — *Forged, Not Given*

Trust in AI cannot be assumed. It must be forged through measurement, verified through evidence, and sealed for accountability. The 13 floors are not suggestions; they are load-bearing structure.

**Built by:** Muhammad Arif bin Fazil — PETRONAS Geoscientist + AI Governance Architect  
**License:** [AGPL-3.0](./LICENSE)

---
*Cryptographic proof that this constitution is forged, not given.* 🔒
