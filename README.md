# arifOS — DITEMPA BUKAN DIBERI

<p align="center">
  <img src="docs/forged_page_1.png" alt="arifOS — Forged, Not Given" width="800">
</p>

<p align="center">
  <strong>The Intelligence Kernel that governs whether AI cognition is permitted</strong><br>
  <em>Controls existence, allocates resources, schedules execution, guarantees isolation</em><br><br>
  <a href="https://pypi.org/project/arifos/"><img src="https://img.shields.io/pypi/v/arifos.svg" alt="PyPI version"></a>
  <a href="https://github.com/ariffazil/arifOS/actions/workflows/ci.yml"><img src="https://github.com/ariffazil/arifOS/actions/workflows/ci.yml/badge.svg" alt="arifOS CI"></a>
  <a href="https://arifosmcp.arif-fazil.com/health"><img src="https://img.shields.io/badge/status-LIVE-success" alt="Status"></a>
  <a href="https://arifos.arif-fazil.com/docs/"><img src="https://img.shields.io/badge/docs-LATEST-cyan" alt="Documentation"></a>
  <a href="./T000_VERSIONING.md"><img src="https://img.shields.io/badge/T000-2026.02.17--FORGE--UVX--SEAL-blue" alt="T000"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-green" alt="License"></a>
  <br><br>
  <a href="https://arifos.arif-fazil.com/docs/"><b>📖 Documentation</b></a> ·
  <a href="#-quick-start"><b>🚀 Quick Start</b></a> ·
  <a href="#-the-13-constitutional-floors"><b>🛡️ 13 Floors</b></a> ·
  <a href="#-implementation-status"><b>📊 Status</b></a> ·
  <a href="#-faq"><b>❓ FAQ</b></a>
</p>

<p align="center">
  <em>arifOS is a Python-based, open-source constitutional kernel for artificial intelligence. It wraps any LLM (Claude, GPT, Gemini, etc.) with 13 hard floors and a 000→999 verdict pipeline, deciding if a thought is permitted to exist.</em>
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

## 🏛️ The 8-Layer Stack

```
┌─────────────────────────────────────────────────────────────────┐
│ L7: ECOSYSTEM — Permissionless sovereignty (civilization-scale) │ 📋 Research
├─────────────────────────────────────────────────────────────────┤
│ L6: INSTITUTION — Trinity consensus (organizational governance) │ 🔴 Stubs
├─────────────────────────────────────────────────────────────────┤
│ L5: AGENTS — Multi-agent federation (coordinated actors)        │ 🟡 Pilot
├─────────────────────────────────────────────────────────────────┤
│ L4: TOOLS — MCP ecosystem (individual capabilities)             │ ✅ Production
├─────────────────────────────────────────────────────────────────┤
│ L3: WORKFLOW — 000→999 sequences (structured processes)         │ ✅ Production
├─────────────────────────────────────────────────────────────────┤
│ L2: SKILLS — Canonical actions (behavioral primitives)          │ ✅ Production
├─────────────────────────────────────────────────────────────────┤
│ L1: PROMPTS — Zero-context entry (user interface)               │ ✅ Production
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 🆕 L0: KERNEL — INTELLIGENCE KERNEL                             │ ✅ SEALED
│     ├─ 5-Organs (ΔΩΨ governance engine)                        │
│     ├─ 9 System Calls (A-CLIP tools)                           │
│     ├─ 13 Floors (existential enforcement)                     │
│     └─ VAULT999 (immutable audit filesystem)                   │
│                                                                 │
│     The substrate that L1-L7 run on                            │
│     [333_APPS/L0_KERNEL/README.md](./333_APPS/L0_KERNEL/)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight:** L0 is the [Intelligence Kernel](./333_APPS/L0_KERNEL/) — the constitutional substrate. L1-L7 are applications that run on it. **L0 is invariant, transport-agnostic law; L1–L7 are replaceable apps. Updating models or agents cannot bypass L0.**

**Full Documentation:** [arifos.arif-fazil.com/docs](https://arifos.arif-fazil.com/docs/) — Full 8-layer architecture & API Reference.

---

## 🚀 Quick Start

### For Operators & Self-Hosters (30 seconds)

The unified server (`server.py`) is the recommended method for running arifOS.

```bash
# Clone the repository
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Install dependencies
pip install -r requirements.txt

# Run the server (default: REST API)
python server.py
```

#### Server Modes
- `python server.py --mode rest`: **REST API** with HTTP + SSE + Tools (Default, Recommended)
- `python server.py --mode http`: FastMCP HTTP transport
- `python server.py --mode sse`: FastMCP SSE transport
- `python server.py --mode stdio`: STDIO for local clients (Claude Desktop, Cursor)

#### Features
- **22 Tools:** 9 AAA-MCP governance skills + 10 ACLIP-CAI sensory tools + 2 ChatGPT (search/fetch) + container tools
- **MCP Resource Templates:** `constitutional://mottos`, `constitutional://floors/{id}`, `system://health`, `tools://schemas/{tool}`

Connect from OpenClaw, Claude Desktop, ChatGPT Developer Mode, or any MCP client.

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
│  │    anchor→reason→validate→audit→seal                        ││
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

### 🔴 Hard Floors (Existential Persistence)

| # | Floor | Threshold | What It Checks |
| :---: | :--- | :--- | :--- |
| F1 | **Amanah** | LOCK | Can we undo this? |
| F2 | **Truth** | τ ≥ 0.99 | Is this grounded? |
| F4 | **Clarity** | ΔS ≤ 0 | Reduces confusion? |
| F7 | **Humility** | 0.03–0.15 | Admits uncertainty? |
| F10 | **Ontology** | LOCK | Grounded in reality? |
| F11 | **Authority** | LOCK | Requester verified? |
| F12 | **Defense** | < 0.85 | Adversarial attack? |

### 🟡 Soft Floors (Stability & Genius)

| # | Floor | Threshold | What It Checks |
| :---: | :--- | :--- | :--- |
| F3 | **Tri-Witness** | ≥ 0.95 | Human + AI + External (Earth/Physics) agree? |
| F5 | **Peace²** | ≥ 1.0 | System stable? |
| F6 | **Empathy** | κᵣ ≥ 0.70 | Vulnerable protected? |
| F8 | **Genius** | G ≥ 0.80 | Solution efficient? |
| F9 | **Anti-Hantu** | < 0.30 | No fake consciousness? |
| F13 | **Sovereign** | HUMAN | Human can override? |

Full specification: [`000_THEORY/000_LAW.md`](./000_THEORY/000_LAW.md)

---

## 📊 Implementation Status

> *F7 Humility requires we tell you what is and isn't working.*

### ✅ SEAL (Production)
| Layer | Evidence |
|:------|:---------|
| **L0 KERNEL** | 5 organs, 9 system calls, 13 floors enforced |
| **L1–L4** | 22 MCP tools (9 AAA + 10 ACLIP-CAI + 2 ChatGPT + container tools), multiple transports |
| **VAULT999** | PostgreSQL-backed immutable ledger with cryptographic seals |
| **Unified Server** | Single `server.py` with 4 modes (rest/http/sse/stdio) and MCP Resource Templates |
| **Live Deployment** | [arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health) |

### 🟡 SABAR (Experimental / In Progress)
| Component | Status |
|:----------|:-------|
| **CI/CD Pipeline** | 🔴 **Failing.** The main CI workflow is currently broken and undergoing repair. |
| **L5 Agents** | Multi-agent federation logic is defined but requires stress testing. |
| **ACLIP_CAI** | The 9-sense infrastructure console is functional but needs calibration. |
| **Tests** | Test suite exists but is not passing reliably due to CI issues. |


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
| [arifosmcp.arif-fazil.com/health](https://arifosmcp.arif-fazil.com/health) | **API Health** — System Health & Metrics | ✅ |
| [arifosmcp.arif-fazil.com/tools](https://arifosmcp.arif-fazil.com/tools) | **Tool Registry** — List of 22 MCP Tools | ✅ |

---
## Philosophy

**DITEMPA BUKAN DIBERI** — *Forged, Not Given*

Trust in AI cannot be assumed. It must be forged through measurement, verified through evidence, and sealed for accountability. The 13 floors are not suggestions; they are load-bearing structure.

**Built by:** Muhammad Arif bin Fazil — PETRONAS Geoscientist + AI Governance Architect  
**License:** [AGPL-3.0](./LICENSE)

---
*Cryptographic proof that this constitution is forged, not given.* 🔒
