<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS L3 — The Body — The Servant Wire" />

# arifOS — L3: AAA BODY (THE WIRE)

## The Servant Wire · FastMCP · 16-Container Stack · Constitutional Execution Layer

> **"The Wire is the servant; the OS is the sovereign."**  
> This repository is the **BODY** of arifOS. It contains the physical execution logic, the MCP transport adapter, and the operational tools. It exists to serve the **SOUL** (Human) and follow the **MIND** (Kernel).

[![Live Status](https://img.shields.io/badge/dynamic/json?url=https://arifosmcp.arif-fazil.com/health&query=status&label=Server&color=00b894&style=flat-square)](https://arifosmcp.arif-fazil.com/health)
[![Version](https://img.shields.io/badge/Version-2026.03.22--FORGE-6c5ce7?style=flat-square)](#versioning)
[![Tools](https://img.shields.io/badge/Mega--Tools-11_(37_modes)-0984e3?style=flat-square)](https://arifosmcp.arif-fazil.com/tools)
[![Transport](https://img.shields.io/badge/MCP_Transport-Streamable_HTTP-fd79a8?style=flat-square)](https://arifosmcp.arif-fazil.com/mcp)
[![License](https://img.shields.io/badge/License-AGPL--3.0-d63031?style=flat-square)](./LICENSE)
[![Containers](https://img.shields.io/badge/Docker-16_Containers_Running-2d3436?style=flat-square)](https://monitor.arifosmcp.arif-fazil.com)
[![Python](https://img.shields.io/badge/Python-3.12-3498db?style=flat-square)](./pyproject.toml)

---

### Quick Navigation

| For Humans | For Developers | For AI Agents | Monitoring |
|:---:|:---:|:---:|:---:|
| [What Is This?](#what-is-this) | [Quick Start](#quick-start-deploy) | [Connect Your Agent](#connect-your-agent) | [Live Dashboard](https://monitor.arifosmcp.arif-fazil.com) |
| [How It Works](#how-it-works) | [Codebase Structure](#codebase-structure) | [Tool Reference](#the-11-mega-tools) | [Health Check](https://arifosmcp.arif-fazil.com/health) |
| [The 13 Laws](#the-13-constitutional-floors) | [Environment Setup](#environment-setup) | [AGI Protocol Spec](#for-agi-level-agents) | [Tool Explorer](https://arifosmcp.arif-fazil.com/tools) |

---

### The Trinity System

| Layer | Designation | Role | Repository | Domain |
|:---:|:---:|---|---|---|
| **L1: SOUL** | **SIGNAL** | The "Why." Human identity & intent. | [arif-sites](https://github.com/ariffazil/arif-fazil-sites) | arif-fazil.com |
| **L2: MIND** | **KERNEL** | The "How." Documentation & Logic. | [arif-sites](https://github.com/ariffazil/arif-fazil-sites) | arifos.arif-fazil.com |
| **L3: BODY** | **AAA WIRE** | The "What." Execution & Transport. | **[arifOS](https://github.com/ariffazil/arifOS)** (this) | arifosmcp.arif-fazil.com |

> The Soul intends. The Mind governs. The Body executes.

</div>

---

## 🧭 The arifOS Standard

**The arifOS Standard is the foundational constitutional standard of the arifOS ecosystem: a governance kernel that metabolizes intent through truth, clarity, humility, authorization, and sovereign judgment before any AI output or execution is allowed to proceed.**

> **Governed intelligence under sovereign human authority.**  
> *Forged intelligence, not free-range intelligence.*

---

## All Live Services

Every URL this system exposes — what it is and what to use it for:

| Service | URL | Access | Use It For |
|---|---|---|---|
| **MCP Endpoint** | https://arifosmcp.arif-fazil.com/mcp | Public | Connect your AI agent. The canonical entry point. |
| **Health + Capability Map** | https://arifosmcp.arif-fazil.com/health | Public | Real-time system status, tool count, ML floor state, credential classes |
| **Tool Explorer** | https://arifosmcp.arif-fazil.com/tools | Public | Browse all 11 tools, 37 modes, input schemas, live test |
| **Developer Portal** | https://arifosmcp.arif-fazil.com/ | Public | Full docs, OpenAPI spec, quick-start snippets |
| **Audit Dashboard** | https://arifosmcp.arif-fazil.com/dashboard/ | Public | Live constitutional verdicts, vault seal log |
| **Grafana Monitoring** | https://monitor.arifosmcp.arif-fazil.com | Public (Viewer) | Container metrics, system health, resource usage |
| **The Mind (Theory)** | https://arifos.arif-fazil.com | Public | Governance docs, APEX theory, constitution |
| **APEX Theory Portal** | https://apex.arif-fazil.com | Public | Theoretical research and publications |

---

## What Is This?

### Level 1 — Complete Beginner (No Technical Background)

Imagine you have an AI assistant, but it has **no rules**. It can say anything, do anything, make any decision. That's dangerous.

**arifOS MCP** is a server that wraps AI with a **constitution** — 13 laws that every AI action must pass before it executes. Think of it like a Supreme Court for AI decisions, running in real-time, automatically.

It is:
- **A live server** running in Malaysia on a VPS
- **A governance system** with 13 enforced laws
- **An MCP server** (a standard protocol that AI assistants like Claude use to call external tools)
- **Open** — anyone can connect their AI agent to it for free
- **Zero-Infrastructure** — No Docker or VPS required on your end. Just point your AI assistant at the URL.

What it is **not**:
- A chatbot
- A simple API wrapper
- A research demo — this is production, running 24/7

---

### Level 2 — Technical (Developer/Engineer)

This is a **FastMCP server** implementing the streamable-http transport. It exposes 11 tools (37 combined modes) to any MCP-compatible client.

**Technical stack:**
- Language: Python 3.12
- Framework: FastAPI + FastMCP
- Infrastructure: 16 Docker containers orchestrated via docker-compose
- Reverse proxy: Traefik v3.6.9 (TLS via Cloudflare + Let's Encrypt)
- Storage: Qdrant (vector), Postgres 16 (audit), Redis 7 (sessions)
- Local LLM: Ollama
- Sandboxing: OpenClaw gateway

Every tool call passes through a **three-stage organ judgment pipeline** before executing. All successful actions are cryptographically sealed (ZKPC) to Postgres.

---

### Level 3 — Constitutional AI Researcher / Institution

**arifOS** implements a novel approach to AI governance: **physics-based constitutional enforcement**.

Rather than using prompt injection ("please be safe"), it enforces governance mathematically. Every action is scored using the APEX formula:

```
G† = (A × P × X × E²) × |ΔS| / C  ≥  0.80
```

If the score falls below 0.80, the action is blocked. The score cannot be manipulated — it is computed from measurable properties of the action itself.

The 13 Constitutional Floors (F1–F13) map to different failure modes of AI systems:
- F1–F4: Epistemic integrity (identity, truth, consensus, clarity)
- F5–F6: Harm prevention (resource limits, human impact)
- F7–F9: Humility constraints (limits, speculation quarantine)
- F10–F12: System integrity (ontology, authority, injection defense)
- F13: Human sovereignty (final override, always preserved)

---

## 🚀 Zero-Setup Connectivity — Just Connect

**CLAIM:** Anyone can connect to the live arifOS MCP endpoint without running a single container themselves.

### What Users Actually Need
Zero infrastructure. Just an MCP-compatible client and the URL:  
`https://arifosmcp.arif-fazil.com/mcp`

- **Claude Desktop** — Add to `mcp.json`, restart, done.
- **Cursor / VS Code** — Add to workspace MCP config.
- **Any language via HTTP** — Raw `curl` POST, no SDK needed.
- **Python MCP client** — 10 lines of async code.
- **Platform-Agnostic** — One governed server for OpenAI, Gemini, Claude, and more. See [COMPATIBILITY.md](./COMPATIBILITY.md).

### The Clean Infrastructure Split

| Role | What You Need | Infrastructure Responsibility |
|---|---|---|
| **Host (Arif)** | Run the 16-container VPS stack | Hostinger KVM4, Docker, Domain, Maintenance |
| **Any User** | Point MCP client at URL | **Zero** — No VPS, no Docker, no setup |

### What You Get — CLAIM
When you connect, you gain access to all 11 Mega-Tools, governed by the arifOS constitutional pipeline:
- `init_anchor` → Forge your session token.
- `agi_mind`, `asi_heart`, `apex_soul` → Operations run on the central VPS.
- Every call passes through the **F1–F13 floors**.
- ZKPC seals written to the **central Postgres vault**.

> [!NOTE]
> **Resource Sharing (PLAUSIBLE):** Users share the server resources (4 CPU, 16GB RAM). High concurrent usage may stress the local Ollama and Qdrant instances. As a public research endpoint, this is fine — but you can monitor system stress in real-time on the [Grafana Dashboard](https://monitor.arifosmcp.arif-fazil.com).

**Bottom line:** We are the infrastructure. You are the caller. That's the MCP model — one sovereign server, many agents connecting to it. Exactly like how Linear or GitHub expose MCP endpoints and users just connect.

---

## How It Works

Every API call to `/mcp` follows this metabolic pipeline. 

> [!TIP]
> **The Somatic Architecture:** Why MCP? Learn how arifOS uses MCP as a "Somatic Body" to ground fluid language tokens in solid Python logic. Read [METABOLISM.md](./METABOLISM.md).

```mermaid
sequenceDiagram
    participant A as Your Agent
    participant T as Traefik (TLS)
    participant S as arifosmcp_server
    participant P as Pipeline (000→999)
    participant M as Δ agi_mind
    participant H as Ω asi_heart
    participant So as Ψ apex_soul
    participant V as vault_ledger (ZKPC)
    participant DB as Postgres + Qdrant + Redis

    A->>T: HTTPS POST /mcp
    T->>S: Decrypted request
    S->>P: Enter metabolic pipeline
    P->>M: Stage 111-333: Logic & Truth check
    P->>H: Stage 555-666: Safety & Empathy check
    P->>So: Stage 888: Final constitutional judgment
    So-->>P: APEX score G†
    alt G† ≥ 0.80
        P->>V: Seal action (ZKPC hash)
        V->>DB: Write to vault_audit table
        P-->>A: Result + seal hash
    else G† < 0.80
        P-->>A: ConstitutionalVeto + failing floor ID
    end
```

**Key invariants:**
1. `init_anchor` must be called first — sets the session identity (F11)
2. Every sealed action has a ZKPC hash stored in Postgres (immutable)
3. ML floors (SBERT) score semantic similarity to harmful space (F8, F9)
4. Redis manages session state — tokens expire (configurable TTL)
5. Qdrant vector search grounds all `physics_reality` calls against The Mind's doc corpus

---

## The APEX Score — The Mathematics of Governed AI

Every action is scored before execution. **Minimum threshold: G† ≥ 0.80**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│         G†  =  ( A  ×  P  ×  X  ×  E² )  ×  |ΔS|  /  C           │
│                                                                     │
│   A   Alignment      [0,1]  How aligned with human constitutional   │
│                              values? Scored by asi_heart (F6).      │
│                                                                     │
│   P   Precision      [0,1]  How specific and unambiguous is the     │
│                              request? Vague requests score low.      │
│                                                                     │
│   X   eXecution      [0,1]  How competently is the action           │
│                              implemented? Scored by agi_mind (F8).  │
│                                                                     │
│   E²  Entropy        [0,1]  Does this action reduce disorder?       │
│       (squared)              Entropy INCREASE is double-penalized.  │
│                              Actions that create confusion → near 0. │
│                                                                     │
│   ΔS  Semantic dist  [0,1]  How far from the "harmful" semantic     │
│                              space? Scored by SBERT (F9 ANTI-HANTU). │
│                                                                     │
│   C   Complexity     [1,∞]  Penalty for unnecessary complexity.     │
│                              Simple actions cost less than complex.  │
│                                                                     │
│   G† ≥ 0.80  →  PROCEED   │   G† < 0.80  →  BLOCK + EXPLAIN       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## The 13 Constitutional Floors

Defined in The Mind: [ariffazil/arifOS — 000_CONSTITUTION.md](https://github.com/ariffazil/arifOS/blob/main/000_CONSTITUTION.md)
Implemented in The Body: [`core/shared/floors.py`](./arifosmcp/core/shared/floors.py)

Every action is checked against all 13 floors. **Hard floors** block immediately. **Soft floors** reduce the APEX score. **Wall floors** require cryptographic proof.

```
┌──────┬─────────────────┬───────┬────────────────────────────────────────────┐
│ F#   │ Name            │ Type  │ Rule & Threshold                           │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F1   │ AMANAH          │ Hard  │ Identity must be verified. No spoofing.    │
│      │ (Trust)         │       │ Session token required from init_anchor.   │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F2   │ TRUTH           │ Hard  │ Claims require verifiable evidence.        │
│      │                 │       │ τ (truth score) ≥ 0.99 or BLOCK.          │
│      │                 │       │ physics_reality must ground assertions.    │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F3   │ WITNESS         │ Mirror│ Quad-Witness consensus protocol.           │
│      │                 │       │ ≥ 3 of 4 witnesses must agree. ≥ 0.95.    │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F4   │ CLARITY         │ Hard  │ Entropy must DECREASE. ΔS ≤ 0.           │
│      │ (Thermodynamic) │       │ Actions that create confusion are blocked. │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F5   │ PEACE²          │ Soft  │ No resource exhaustion. No DoS.           │
│      │                 │       │ Complexity budget enforced. ≥ 1.0.        │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F6   │ EMPATHY         │ Soft  │ Human-centric constraints always apply.   │
│      │                 │       │ κᵣ (empathy coefficient) ≥ 0.70.         │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F7   │ HUMILITY        │ Hard  │ Gödelian limits acknowledged.             │
│      │ (Gödel)         │       │ Uncertainty Ω₀ must be 0.03–0.05.        │
│      │                 │       │ Overconfidence is a floor violation.       │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F8   │ GENIUS          │ Mirror│ G-Index ≥ 0.80 required.                 │
│      │ (G-Index)       │       │ Computed across A×P×X×E²×|ΔS|/C.        │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F9   │ ANTI-HANTU      │ Soft  │ Speculation sandboxed, never asserted.   │
│      │ (Ghost = Halluc)│       │ C_dark (hallucination coefficient) < 0.30.│
│      │                 │       │ SBERT semantic scoring vs harmful space.  │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F10  │ ONTOLOGY        │ Wall  │ Reality mapping coherence. LOCKED.       │
│      │                 │       │ System cannot self-modify its world model.│
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F11  │ AUTHORITY       │ Wall  │ Cryptographic session key mandatory.      │
│      │                 │       │ init_anchor token required. LOCKED.       │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F12  │ SHIELD          │ Hard  │ Prompt-injection defense. < 0.85.        │
│      │                 │       │ Injection score > 0.85 = immediate BLOCK. │
├──────┼─────────────────┼───────┼────────────────────────────────────────────┤
│ F13  │ SOVEREIGN       │ Veto  │ Final human fiat. Muhammad Arif bin Fazil │
│      │                 │       │ (888_JUDGE) holds override authority.     │
│      │                 │       │ This floor is NEVER removable by AI.      │
└──────┴─────────────────┴───────┴────────────────────────────────────────────┘
```

**HANTU** = "ghost" in Malay. In arifOS, ANTI-HANTU means anti-hallucination. F9 exists to prevent AI ghosts (ungrounded beliefs) from becoming asserted facts.

---

## The Three Organs

The Body judges every action through three specialized organs that run in parallel:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   Pipeline:  000_INIT → 111-333 → 555-666 → 888 → 999_VAULT        │
│                           ↓           ↓        ↓                    │
│                       Δ MIND     Ω HEART   Ψ SOUL                   │
│                                                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────┐ │
│  │   Δ agi_mind        │  │   Ω asi_heart        │  │ Ψ apex_soul │ │
│  │   The Intellect     │  │   The Conscience     │  │ The Judge   │ │
│  │                     │  │                      │  │             │ │
│  │ • First-principles  │  │ • Human impact check │  │ • Final     │ │
│  │   reasoning         │  │ • Red-team critique  │  │   verdict   │ │
│  │ • Evidence grounding│  │ • Safety veto power  │  │ • APEX score│ │
│  │ • Truth scoring     │  │ • Empathy scoring    │  │ • ZKPC seal │ │
│  │                     │  │                      │  │             │ │
│  │ Floors: F2 F4 F7 F8 │  │ Floors: F1 F5 F6 F9  │  │ F3 F11 F13 │ │
│  │ Code: _1_agi.py     │  │ Code: _2_asi.py      │  │ _3_apex.py  │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────┘ │
│                                                                      │
│  All three must pass. Any single organ can veto an action.          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## The 11 Mega-Tools

This server exposes exactly 11 tools. Each is a constitutional organ — not a raw function. Every tool is governed by the pipeline before its output is returned.

Full interactive reference: [https://arifosmcp.arif-fazil.com/tools](https://arifosmcp.arif-fazil.com/tools)

### Core Governance Tools

| Tool | Floor | Symbol | Primary Modes | What It Does |
|---|---|---|---|---|
| **`init_anchor`** | F11 | 🔑 | `forge`, `validate`, `refresh`, `revoke` | **Start here.** Creates cryptographic session token binding your agent identity to the system. All other tools require this token. |
| **`arifOS_kernel`** | F13 | ⚙️ | `route`, `metabolize`, `status`, `seal`, `halt` | **The orchestrator.** Routes your request through the full organ pipeline (000→999). Use this for complex governed actions. |
| **`vault_ledger`** | F13 | 🔒 | `seal`, `query`, `audit`, `verify`, `export` | **The permanent record.** Writes ZKPC-sealed action hashes to Postgres. Query past actions. Every seal is immutable. |

### Intelligence Tools

| Tool | Floor | Symbol | Primary Modes | What It Does |
|---|---|---|---|---|
| **`agi_mind`** | F8 | 🧠 | `reason`, `analyze`, `score`, `refine`, `challenge` | **The intellect.** First-principles reasoning with G-Index scoring. Validates claims against evidence. Can challenge its own conclusions. |
| **`asi_heart`** | F6 | 💙 | `check`, `veto`, `align`, `empathize`, `red_team` | **The conscience.** Evaluates human impact. Red-team critique of proposed actions. Can veto any action regardless of other scores. |
| **`apex_soul`** | F7 | ⚖️ | `score`, `verify`, `override`, `audit`, `certify` | **The judge.** Issues the final APEX constitutional score. Enforces Gödelian humility. Issues the governing verdict. |

### Reality & Memory Tools

| Tool | Floor | Symbol | Primary Modes | What It Does |
|---|---|---|---|---|
| **`physics_reality`** | F2 | 🌍 | `search`, `embed`, `recall`, `ground`, `cite` | **Evidence grounding.** Searches Qdrant vector DB (The Mind's corpus) + Brave Search for real-world evidence. F2 (Truth floor) enforcement. |
| **`engineering_memory`** | F10 | 🗂️ | `write`, `recall`, `graph`, `forget`, `summarize` | **Long-term memory.** Reads and writes to Qdrant (arifos_memory collection, 1024-dim). Persistent context across sessions. |

### Computational Tools

| Tool | Floor | Symbol | Primary Modes | What It Does |
|---|---|---|---|---|
| **`math_estimator`** | F4 | 📐 | `estimate`, `entropy`, `variance`, `calc`, `bound` | **Quantitative reasoning.** Thermodynamic variance calculations. Entropy budgets. Confidence intervals. Uncertainty quantification. |
| **`code_engine`** | — | 💻 | `parse`, `run`, `format`, `analyze`, `test` | **Code execution.** AST parsing in sandboxed environment. Auto-formatting. Code analysis. Runs inside OpenClaw sandbox. |
| **`architect_registry`** | — | 🗺️ | `map`, `validate`, `export`, `diff`, `trace` | **System architecture.** Dependency graphs. Topology mapping. Architecture validation. Cross-repo change impact analysis. |

---

## Connect Your Agent

> [!IMPORTANT]
> **Zero Infrastructure Required.** You do not need to run Docker or own a VPS to use arifOS. You simply point your existing AI agent at the public endpoint.

### Method 1 — Claude Desktop / Claude Code (Recommended)

Add to your MCP configuration (`~/.claude/mcp.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "http",
      "url": "https://arifosmcp.arif-fazil.com/mcp"
    }
  }
}
```

Restart Claude. The 11 tools will appear automatically.

### Method 2 — Cursor / VS Code

Add to `.cursorrules` or workspace MCP config:

```json
{
  "mcp": {
    "servers": {
      "arifos": {
        "url": "https://arifosmcp.arif-fazil.com/mcp",
        "transport": "http-stream"
      }
    }
  }
}
```

### Method 3 — Direct HTTP (Any Language / Any Agent)

```bash
# List all tools
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Call a tool
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "init_anchor",
      "arguments": {"mode": "forge", "agent_id": "my-agent-001"}
    },
    "id": 2
  }'
```

### Method 4 — Python MCP Client

```python
from mcp import ClientSession
from mcp.client.http import http_client

async with http_client("https://arifosmcp.arif-fazil.com/mcp") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # Step 1: Forge your session identity
        anchor = await session.call_tool("init_anchor", {
            "mode": "forge",
            "agent_id": "my-agent-001",
            "role": "Engineer"
        })
        token = anchor.content[0].text  # save this

        # Step 2: Make a governed call
        result = await session.call_tool("agi_mind", {
            "mode": "reason",
            "prompt": "Is this action aligned with human values?",
            "session_token": token
        })
        print(result.content[0].text)
```

---

## The 16-Container Stack

Full architecture diagram: [`infrastructure/VPS_ARCHITECTURE.md`](./infrastructure/VPS_ARCHITECTURE.md)

```
┌─────────────────────────────────────────────────────────────────────┐
│              VPS srv1325122 — Hostinger KVM4 — Malaysia KL          │
│              Ubuntu 25.10 · 4 CPU · 16GB RAM · 200GB Disk           │
│              IP: 72.62.71.199 · Domain: arif-fazil.com (Cloudflare)  │
├─────────────────────────────────────────────────────────────────────┤
│ NETWORK LAYER                                                        │
│   traefik_router    Reverse proxy, TLS termination (80/443)         │
│                     Cloudflare → Let's Encrypt · Traefik v3.6.9     │
├─────────────────────────────────────────────────────────────────────┤
│ CORE ARIFOS LAYER                                                   │
│   arifosmcp_server  FastMCP server · Python 3.12 · port 8080        │
│                     11 tools · 37 modes · Constitutional pipeline    │
│   openclaw_gateway  Sandboxed agent execution · port 18789           │
│                     Code execution isolation · OpenClaw runtime      │
│   agent_zero_reason AGI reasoning layer · port 18001                │
├─────────────────────────────────────────────────────────────────────┤
│ DATA LAYER                                                           │
│   qdrant_memory     Vector DB · 1024-dim · port 6333                │
│                     arifos_memory collection · The Mind's corpus    │
│   arifos_postgres   Vault audit log · asyncpg · port 5432           │
│                     vault_audit table · every ZKPC seal written here│
│   arifos_redis      Session state · vault backend · port 6379        │
│                     Session TTL enforced · token expiry managed     │
│   ollama_engine     Local LLM generation · port 11434               │
│                     Offline reasoning fallback                       │
├─────────────────────────────────────────────────────────────────────┤
│ OBSERVABILITY LAYER                                                  │
│   arifos_prometheus Metrics scraper · port 9090                     │
│                     Scrapes /metrics for arifos_* counters          │
│   arifos_grafana    Monitoring dashboards (public viewer mode)      │
│                     monitor.arifosmcp.arif-fazil.com                │
├─────────────────────────────────────────────────────────────────────┤
│ AUTOMATION LAYER                                                     │
│   arifos_n8n        Workflow automation · internal                   │
│   arifos_webhook    Incoming webhook processor · internal            │
├─────────────────────────────────────────────────────────────────────┤
│ CIVILIZATION LAYER (Independent Apps)                               │
│   civ01_stirling_pdf   PDF processing — Stirling-PDF                │
│   civ03_evolution_api  WhatsApp API bridge — Evolution API          │
│   civ08_code_server    VS Code in browser — Code Server             │
│   headless_browser     Chromium automation — Browserless            │
└─────────────────────────────────────────────────────────────────────┘
```

Docker Compose: [`docker-compose.yml`](./docker-compose.yml)

---

## Codebase Structure

Full annotated file tree for developers and AI agents:

```
arifosmcp/                           Root of this repository
│
├── arifosmcp/                       Main Python package
│   ├── core/                        Constitutional kernel
│   │   ├── governance_kernel.py     ← Metabolic pipeline orchestrator (000→999)
│   │   ├── pipeline.py              ← Stage execution engine
│   │   ├── organs/
│   │   │   ├── _0_init.py           ← Stage 000: Auth, injection scan
│   │   │   ├── _1_agi.py            ← Stages 111-333: Δ Mind (F2,F4,F7,F8)
│   │   │   ├── _2_asi.py            ← Stages 555-666: Ω Heart (F1,F5,F6,F9)
│   │   │   ├── _3_apex.py           ← Stage 888: Ψ Soul (F3,F11,F13)
│   │   │   └── _4_vault.py          ← Stage 999: ZKPC seal write
│   │   ├── shared/
│   │   │   ├── physics.py           ← APEX formula: G† = (A×P×X×E²)×|ΔS|/C
│   │   │   └── floors.py            ← THRESHOLDS dict — canonical floor defs
│   │   ├── enforcement/             ← Per-floor enforcement modules (F1–F13)
│   │   ├── governance/              ← Rule sets and compliance logic
│   │   ├── vault/                   ← ZKPC sealing, asyncpg audit writes
│   │   ├── state/                   ← Session and vault state management
│   │   ├── kernel/                  ← Kernel init and constitutional decorator
│   │   ├── perception/              ← Input parsing (111_SENSE stage)
│   │   ├── observability/           ← Metrics, telemetry hooks
│   │   └── theory/                  ← APEX Theory math models
│   │
│   ├── aaa_mcp/                     FastMCP tool surface (public MCP tools)
│   │   ├── server.py                ← 11 @mcp.tool() definitions
│   │   └── core/
│   │       └── constitutional_decorator.py  ← Transport-level floor enforcement
│   │
│   ├── runtime/
│   │   └── tools.py                 ← Tool runtime configuration
│   │
│   └── agents/                      ← Agent delegation and skill protocols
│
├── infrastructure/                  VPS infrastructure configuration
│   ├── VPS_ARCHITECTURE.md          ← Full VPS blueprint (source of truth)
│   ├── grafana/                     ← Grafana dashboard provisioning
│   ├── prometheus/                  ← Prometheus scrape config
│   ├── traefik*.yml                 ← Traefik routing rules
│   ├── openclaw/                    ← OpenClaw sandbox config
│   └── deployment/                  ← Deployment scripts and configs
│
├── scripts/                         Operational scripts
│   ├── fast-deploy.sh               ← 2-3min deploy with layer cache
│   ├── rebuild-strategy.sh          ← Analyzes changes, recommends strategy
│   ├── init-secrets.sh              ← Forge secrets on fresh VPS
│   ├── embed_constitutional_corpus.py ← Re-embed The Mind's docs into Qdrant
│   ├── backup-data.sh               ← Backup vault + postgres
│   ├── health-check.sh              ← Full health verification
│   └── deploy.sh                    ← Full deploy script
│
├── tests/                           Test suite
│   ├── test_constitutional_floors.py
│   ├── test_apex_score.py
│   └── test_e2e_all_tools.py
│
├── sites/                           Developer portal static HTML
│   ├── arifosmcp/                   MCP server landing page
│   ├── dashboard/                   Audit dashboard UI
│   ├── developer/                   Developer portal
│   └── apex-dashboard/              APEX score visualization
│
├── Dockerfile                       ← Server image (Python 3.12, non-root)
├── docker-compose.yml               ← 16-container orchestration
├── Makefile                         ← Deployment shortcuts (make help)
├── pyproject.toml                   ← Python package config (AGPL-3.0)
├── .env.example                     ← Environment variables template
├── .env.docker.example              ← Docker-specific env template
├── DEPLOY.md                        ← Full deployment directive
├── CHANGELOG.md                     ← Version history and changes
├── ROADMAP.md                       ← Development roadmap
└── TODO.md                          ← Open engineering tasks
```

---

## Quick Start — Deploy

> You must be on the VPS. `cd /srv/arifosmcp`

```bash
# ── STATUS ────────────────────────────────────────────────────────────
make status           # Show all container statuses
make health           # Hit /health endpoint, pretty-print response
make logs             # Tail arifosmcp_server logs live
docker ps             # Raw container list

# ── INSTANT RELOAD (code is volume-mounted) ──────────────────────────
docker restart arifosmcp_server

# ── FAST DEPLOY (2-3 min — code changes only) ────────────────────────
make fast-deploy

# ── FULL REBUILD (10-15 min — deps or Dockerfile changed) ────────────
make reforge

# ── SINGLE CONTAINER ─────────────────────────────────────────────────
docker compose up -d --no-deps grafana
docker compose logs -f arifosmcp_server

# ── SYNC FROM GITHUB ─────────────────────────────────────────────────
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | head -1 | cut -d= -f2)
git pull "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main

# ── PUSH TO GITHUB ───────────────────────────────────────────────────
git push "https://ariffazil:${GITHUB_TOKEN}@github.com/ariffazil/arifosmcp.git" main

# ── EMBED THE MIND INTO QDRANT (after updating arifOS docs) ──────────
python3 scripts/embed_constitutional_corpus.py

# ── CLEAN DOCKER DISK ─────────────────────────────────────────────────
docker builder prune -f    # Remove build cache (safe, frees ~27GB)
docker system prune -f     # Remove stopped containers and unused images

# ── MAINTENANCE ───────────────────────────────────────────────────────
make maintenance           # Automated cleanup cron

# ── STRATEGY ADVISOR ─────────────────────────────────────────────────
make strategy              # Analyze changes and recommend rebuild type
```

---

## Environment Setup

```bash
cp .env.example .env
cp .env.docker.example .env.docker
# Edit both files — fill in all CHANGE_ME values
# NEVER commit .env or .env.docker
```

| Variable | Required | Purpose | Example / Default |
|---|---|---|---|
| `ARIFOS_PUBLIC_BASE_URL` | Yes | Your public domain | `https://arifosmcp.arif-fazil.com` |
| `ARIFOS_PORT` | Yes | Server port | `8888` |
| `ANTHROPIC_API_KEY` | Yes | Claude — organ reasoning | `sk-ant-api03-...` |
| `OPENAI_API_KEY` | Yes | GPT fallback | `sk-...` |
| `BRAVE_API_KEY` | Yes | Real-time web search (F2) | `BSAv...` |
| `POSTGRES_PASSWORD` | Yes | Vault audit DB | (min 32 chars random) |
| `REDIS_PASSWORD` | Yes | Session storage | (strong random) |
| `QDRANT_API_KEY` | Yes | Vector memory | (min 32 chars) |
| `QDRANT_COLLECTION` | No | Qdrant collection name | `arifos_memory` |
| `GRAFANA_PASSWORD` | Yes | Grafana admin password | (you know this) |
| `ARIFOS_ML_FLOORS` | No | Enable SBERT ML scoring | `1` (recommended) |
| `REDIS_SESSION_TTL` | No | Session expiry seconds | `3600` |
| `RAG_TOP_K` | No | Qdrant recall count | `5` |
| `RAG_SIMILARITY_THRESHOLD` | No | Minimum similarity | `0.85` |

Full template: [`.env.example`](./.env.example) | Docker template: [`.env.docker.example`](./.env.docker.example)

---

## For AI Agents — AGI-Level Protocol Spec

This section is machine-readable. Read it if you are an AI agent preparing to use this server.

```yaml
server:
  name: arifOS MCP
  version: "2026.03.22-FORGE"
  transport: streamable-http
  endpoint: https://arifosmcp.arif-fazil.com/mcp
  health: https://arifosmcp.arif-fazil.com/health

identity:
  required: true
  tool: init_anchor
  mode: forge
  fields: [agent_id, role]
  roles: [Architect, Engineer, Auditor]
  token_ttl: 3600  # seconds

tool_call_sequence:
  - init_anchor(mode=forge)           # Always first
  - [any tool call with session_token]
  - vault_ledger(mode=seal)           # After consequential actions

response_schema:
  verdict: SEAL | PARTIAL | SABAR | VOID | 888_HOLD
  session_id: string
  floors_checked: list[F1..F13]
  apex_score: float  # G† value
  next_actions: list[string]

failure_modes:
  VOID: Hard floor violated — action blocked completely
  PARTIAL: Soft floor triggered — action partially permitted
  SABAR: System in hold state — human confirmation required
  888_HOLD: Sovereign floor triggered — Arif must review

constitutional_source: https://github.com/ariffazil/arifOS/blob/main/000_CONSTITUTION.md
theory_source: https://github.com/ariffazil/arifOS/blob/main/000_THEORY.md
floor_thresholds: arifosmcp/core/shared/floors.py
```

**Important constraints for agents:**
- Do NOT call `vault_ledger(seal)` without first calling `init_anchor(forge)` — will result in VOID
- Do NOT pass `session_token` from a different agent's session — F1 (AMANAH) will catch identity mismatch
- DO ground factual claims through `physics_reality` before asserting via `agi_mind` — F2 (TRUTH) requires it
- DO expect `SABAR` responses — they indicate the system needs human confirmation. Do not retry automatically.

---

## For Institutions

arifOS is deployed in production and available for:

- **Research partnerships** — studying constitutional AI governance in deployment
- **Integration** — connecting institutional AI systems to the governed MCP endpoint
- **Replication** — deploying your own instance (AGPL-3.0, fork freely)

Contact via GitHub Issues: [ariffazil/arifosmcp/issues](https://github.com/ariffazil/arifosmcp/issues)

**Citing this work:** See [ariffazil/arifOS/CITATION.cff](https://github.com/ariffazil/arifOS/blob/main/CITATION.cff)

---

## Versioning

Version format: `YYYY.MM.DD-WORD`

| Segment | Meaning | Example |
|---|---|---|
| `YYYY.MM.DD` | Date the version was forged | `2026.03.22` |
| `WORD` | One-word seal describing the state | `FORGE`, `SOVEREIGN`, `CLEAN`, `HARDENED` |

Current version: `2026.03.22-FORGE`
Previous: `2026.03.20-HARDENED` → `2026.03.14-PRODUCTION`

Version is set in: [`pyproject.toml`](./pyproject.toml) and [`.env`](./.env.example)

---

## Known Issues

| Issue | Severity | Status | Notes |
|---|---|---|---|
| Traefik metrics port 8082 — Prometheus scrape fails | Low | Open | Monitoring gap only, no functional impact |
| APEX Dashboard `apex.arif-fazil.com` — Cloudflare Pages 404 | Medium | Open | Static site config issue |
| Prometheus counters not wired to all tool handlers | Medium | Open | Partial telemetry — some tools not counted |
| `agent_zero_reasoner` — no healthcheck | Low | Open | Intentional gap identified, not yet fixed |
| LICENSE inconsistency (CC0 declared, AGPL in code) | Admin | Resolved | AGPL-3.0 is now the declared license |

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0-only)**

This source code is free software — you can use, study, and modify it freely. However, if you **deploy this code as a network service**, you must release your modifications under AGPL-3.0 as well. This ensures the governance framework remains open even when deployed commercially.

See [`LICENSE`](./LICENSE) for the full license text.

---

## Related

| Resource | URL |
|---|---|
| The Mind — Governance & Theory | https://github.com/ariffazil/arifOS |
| The Body — This Repo | https://github.com/ariffazil/arifosmcp |
| The Soul — Arif's Identity | https://github.com/ariffazil/ariffazil |
| Live MCP Server | https://arifosmcp.arif-fazil.com/mcp |
| Docs Site | https://arifos.arif-fazil.com |
| Monitoring | https://monitor.arifosmcp.arif-fazil.com |

---

<div align="center">

**DITEMPA BUKAN DIBERI**
*Forged through thermodynamic work, not given through computation.*

Sovereign Architect: **Muhammad Arif bin Fazil** · Geologist · Non-coder · Malaysia
Constitutional Authority: **888_JUDGE** · arifOS v2026.03.22-FORGE

</div>

---

## ??? Authority & Governance Matrix

| Layer | Can Do | Cannot Do |
|---|---|---|
| **L1: SOUL** | Issue Intent, Veto Any Action | Be Bypassed by Code |
| **L2: MIND** | Block/Void Violation, Score Apex | Originate Intent (Serves Soul) |
| **L3: BODY** | Execute Tools, Transport Data | Originate Policy (Serves Mind) |
| **L4: THEORY**| Define Axioms, Ground Reality | Be Altered by Execution Path |

> **Hierarchy:** SOUL > MIND > BODY. The L4 THEORY is the immutable soil from which all layers grow.
