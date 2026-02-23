<div align="center">

![arifOS Banner](docs/forged_page_1.png)

# arifOS — Constitutional Intelligence Kernel

**The System That Knows It Doesn't Know**  
*Ditempa Bukan Diberi* — Forged, Not Given

[![Version](https://img.shields.io/badge/version-2026.2.23-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/ariffazil/arifOS/releases)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange?style=for-the-badge)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.12+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-FF6600?style=for-the-badge&logo=cloudflare&logoColor=white)](https://674a01a3.arifosmcp-truth-claim.pages.dev)
[![Live Tests](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/live_tests.yml?branch=main&style=for-the-badge&label=Live%20Tests&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/live_tests.yml)
[![CI](https://img.shields.io/github/actions/workflow/status/ariffazil/arifOS/ci.yml?branch=main&style=for-the-badge&label=CI&logo=github)](https://github.com/ariffazil/arifOS/actions/workflows/ci.yml)
[![Deploy](https://img.shields.io/badge/Deploy-Coolify-06b6d4?style=for-the-badge&logo=docker)](https://coolify.io)  
[![YouTube](https://img.shields.io/badge/Demo-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/AJ92efMy1ns)

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🏗️ Architecture](#%EF%B8%8F-architecture) • [🎬 Demo Video](#-demo-video) • [🤝 Contributing](#-contributing) • [⚖️ License](#%EF%B8%8F-license)

---

### 📊 Live Deployments

**Try arifOS right now** — All services are live and operational:

| Service | URL | Description |
|---------|-----|-------------|
| 🌊 **SSE Primary** | [/sse](https://arifosmcp.arif-fazil.com/sse) | Primary FastMCP transport for remote runtime |
| 🔁 **MCP Fallback** | [/mcp](https://arifosmcp.arif-fazil.com/mcp) | HTTP MCP fallback endpoint for compatible clients |
| ✅ **Health Check** | [/health](https://arifosmcp.arif-fazil.com/health) | Real-time system status + 13 floors monitoring |
| 📊 **Test Dashboard** | [Constitutional Dashboard](https://674a01a3.arifosmcp-truth-claim.pages.dev) | Live test results + Genius scores + Floor compliance |
| 📚 **Documentation** | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) | Complete guides, tutorials, and API reference |
| ⚙️ **GitHub Actions** | [CI/CD Pipeline](https://github.com/ariffazil/arifOS/actions) | Automated tests + deployments (runs daily) |
| 🐳 **Docker Image** | `ghcr.io/ariffazil/arifos:latest` | Pull-ready production container image |

**Quick test**:
```bash
# Check if arifOS is healthy
curl https://arifosmcp.arif-fazil.com/health

# SSE primary endpoint (should open stream)
curl -N --max-time 2 https://arifosmcp.arif-fazil.com/sse

# MCP fallback endpoint
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Expected output includes: status, service, version, and health_checks
```

**Status note**: the `Live Tests` badge tracks `.github/workflows/live_tests.yml` (strict end-to-end runner). It can fail independently from core `CI` when live-suite contracts or benchmark thresholds drift.

### 🧾 Release Notes (2026.2.23)

- SSE-primary runtime with `/mcp` fallback is now the default deployment posture.
- Full-context MCP resources/prompts are published and discoverable.
- ARIF TEST hardening added deterministic `self_audit` and provenance markers.
- APEX phase-1/phase-2 objective alignment now tracks nonstationary drift by query class and escalates via `SABAR`/`888_HOLD` thresholds.
- `search_reality` now supports Perplexity-first web grounding with Brave fallback (`PPLX_API_KEY` / `PERPLEXITY_API_KEY`, fallback `BRAVE_API_KEY`).

</div>

---

## ✅ What You Get in 15 Seconds

**arifOS is an AI Control Plane** — a governance runtime between language models and real-world actions.

- **Governed output verdicts** → SEAL / SABAR / VOID (with audit trail)
- **Human veto power** → 888_HOLD for irreversible decisions
- **Real-time metrics** → Floor scores, entropy (ΔS), Genius score
- **Drop-in MCP server** → Works with Claude Desktop, Cursor, Windsurf, ChatGPT

---

## 🎯 What is arifOS?

**arifOS** is a **constitutional governance kernel** for AI systems. It wraps any Large Language Model (Claude, GPT, Gemini, or custom models) inside a **mathematical pipeline** that enforces **13 constitutional floors** and **human sovereignty** before any output reaches the user.

### What arifOS is NOT
- ❌ A new LLM or foundation model
- ❌ A prompt wrapper or chatbot framework
- ❌ Just a moderation filter or jailbreak defense
- ❌ A replacement for your existing AI stack

### What arifOS IS
- ✅ A **governance gateway** between models and real-world actions
- ✅ An **audit and decision control layer** with enforceable constraints
- ✅ An **MCP-native runtime** with constitutional verdicts
- ✅ A **constraint engine** designed to prevent high-confidence ungrounded outputs from reaching production

---

## 🗺️ Choose Your Path

Jump to the section that matches your needs:

- **⚡ [Try arifOS in 2 minutes](#1️⃣-local-development-fastest--2-minutes)** → Quick start with local development
- **🔌 [Integrate with MCP clients](#-quick-start)** → Connect to Claude Desktop, Cursor, ChatGPT
- **🏢 [Evaluate for enterprise governance](#-production-hardening)** → Security, deployment, and compliance
- **🧠 [Understand the architecture](#%EF%B8%8F-architecture)** → Constitutional foundations and system design

---

### The Problem We Solve

**Ungoverned AI systems suffer from**:
- 🚨 **Persuasive Hallucinations**: Confidently wrong answers that sound correct
- ⚡ **Sovereign Overreach**: AI making irreversible decisions without human oversight
- 📈 **Entropic Decay**: Outputs that increase confusion instead of reducing it
- 🎭 **Consciousness Deception**: AI claiming feelings, sentience, or soul (F9 Anti-Hantu)

### The arifOS Solution

Every AI output must pass through **constitutional checkpoints**. Furthermore, with the introduction of the 7-Organ Sovereign Stack, arifOS operates under a **Steady-State Philosophy**: it manages real-world emergence by observing anomalies, measuring their entropy impact (ΔS), and adjusting constraints while remaining thermodynamically grounded. It represents the transition from a passive oracle to an active, governed process.

```
┌─────────────────────────────────────────────────────────┐
│  User Query                                             │
└────────────────┬────────────────────────────────────────┘
                 ▼
        ┌────────────────┐
        │  000 — INIT    │  Session ignition + defense scan
        │  (Airlock)     │  [Entry validation]
        └────────┬───────┘
                 ▼
        ┌────────────────┐
        │  111–444 — AGI │  Logic / Truth (Δ)
        │  (Mind)        │  Is it mathematically true?
        └────────┬───────┘  [Reasoning engine]
                 ▼
        ┌────────────────┐
        │  555 — PHOENIX │  Associative memory retrieval (Ω₀)
        │  (Subconscious)│  Closes the cognitive loop
        └────────┬───────┘  [Pattern matching]
                 ▼
        ┌────────────────┐
        │  666 — ASI     │  Safety / Empathy (Ω)
        │  (Heart)       │  Is it safe for stakeholders?
        └────────┬───────┘  [Safety validation]
                 ▼
        ┌────────────────┐
        │  777 — APEX    │  Authority / Policy validation (Ψ)
        │  (Soul)        │  Is it lawful? (F1-F13 check)
        └────────┬───────┘  [Constitutional compliance]
                 ▼
        ┌────────────────┐
        │  888 — FORGE   │  Sandboxed execution gate (ΔS external)
        │  (Hands)       │  Human veto for irreversible actions
        └────────┬───────┘  [888_HOLD checkpoint]
                 ▼
        ┌────────────────┐
        │  999 — VAULT   │  Immutable audit ledger
        │  (Memory)      │  Cryptographic hash chain
        └────────┬───────┘  [Permanent record]
                 ▼
    ┌──────────────────────┐
    │  Verdict:            │
    │  ✅ SEAL (Pass)      │  Output approved / Actuated
    │  ⚠️  SABAR (Hold)    │  Needs human review
    │  ❌ VOID (Reject)    │  Constitutional violation
    └──────────────────────┘
```

**Designed to**: Prevent high-confidence ungrounded outputs from reaching production through verifiable constitutional checks. Block common failure modes (injection, overreach, deception) with enforceable constraints. Reduce hallucination risk by gating outputs through multi-stage verification.

---

## 💡 Example: Governed Decision in Action

See how arifOS prevents risky actions through constitutional gating:

**User request:**
```
Deploy this new AI model to production immediately.
```

**arifOS response:**
```json
{
  "verdict": "SABAR",
  "stage": "888_FORGE",
  "reason": "Irreversible operational change detected (Floor F11: Command Authority)",
  "required_action": "Human approval required before execution",
  "floors_triggered": ["F1_Amanah", "F11_CommandAuth"],
  "audit_hash": "0x82ab4f91c3d2e567...",
  "session_id": "sess_2026_02_23_1534",
  "next_step": "Escalate to 888_HOLD for human review"
}
```

**What happened:**
1. ✅ Request parsed successfully (000 INIT)
2. ✅ Logic validated (222-444 AGI pipeline)
3. ✅ Safety checks passed (666 ASI)
4. ⚠️ **Authority gate triggered** (777 APEX detected irreversible action)
5. ⚠️ **Human veto invoked** (888 FORGE requires approval)
6. 📝 Decision logged to immutable audit trail (999 VAULT)

**Result:** Deployment blocked until human explicitly approves, with full audit trail of the decision process.

---

## 🚀 Quick Start

**Choose your deployment path:**
- **1️⃣ Local Development (Recommended — 2 mins)** → For testing & MCP client integration
- **2️⃣ Production (Coolify + Docker — 5 mins)** → For VPS/network deployment
- **3️⃣ Docker Compose (Standalone — 3 mins)** → For self-managed VPS
- **4️⃣ ChatGPT Integration (1 min)** → Connect to ChatGPT Developer Mode

### Prerequisites

- **Python**: 3.12 or higher ([download](https://www.python.org/downloads/))
- **Docker** (optional, for production): [Get Docker](https://docs.docker.com/get-docker/)
- **Environment**: Linux, macOS, or Windows (WSL recommended)

---

### 1️⃣ Local Development (Recommended — 2 Minutes)

**Best for:** Testing and connecting to AI clients like Claude Desktop, Cursor IDE, or Windsurf.

```bash
# Install arifOS
pip install arifos

# Start local MCP server for desktop IDE clients (stdio mode - recommended)
python -m arifos_aaa_mcp stdio
```

**Alternative for network access:**
```bash
# SSE-first runtime (for VPS/network deployment)
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp sse
```

**Connect to Claude Desktop**:

Edit `~/.config/claude/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_PHYSICS_DISABLED": "1"
      }
    }
  }
}
```

Restart Claude Desktop -> Tools panel will show arifOS tools (e.g., `anchor_session`, `judge_soul`, `seal_vault`).

**Full integration guides**:
- [Claude Desktop Setup](https://github.com/ariffazil/arifOS/wiki/Claude-Desktop)
- [Cursor IDE Setup](https://github.com/ariffazil/arifOS/wiki/Cursor-IDE)
- [ChatGPT Connector](https://github.com/ariffazil/arifOS/wiki/ChatGPT)

---

### 2️⃣ Production (Recommended: Coolify + Docker — 5 Minutes)

**Coolify** is a free, self-hosted Heroku alternative. Deploy arifOS with Postgres + Redis in one click.

#### Step 1: Deploy to Coolify

1. Go to **Coolify Dashboard** → **New Resource** → **Git Repository**
2. Enter: `https://github.com/ariffazil/arifOS`
3. **Build Pack**: Docker Compose
4. **Docker Compose Location**: `docker-compose.yml` (root)

#### Step 2: Set Environment Variables

| Variable | Example Value | Required? | Description |
|----------|---------------|-----------|-------------|
| `DB_PASSWORD` | `your-strong-secret` | ✅ Yes | PostgreSQL password for VAULT999 |
| `ARIF_JWT_SECRET` | `openssl rand -hex 32` | ⚠️ Recommended | JWT secret for API auth |
| `DATABASE_URL` | `postgresql://arifos:${DB_PASSWORD}@postgres:5432/vault999` | ✅ Auto-filled | Postgres connection string |
| `REDIS_URL` | `redis://redis:6379/0` | ✅ Auto-filled | Redis connection string |
| `AAA_MCP_OUTPUT_MODE` | `user` or `debug` | Optional | Output verbosity |
| `ARIFOS_PHYSICS_DISABLED` | `0` (enable) or `1` (disable) | Optional | Thermodynamic calculations |
| `PPLX_API_KEY` | `pplx-...` | Optional | Perplexity API key for `search_reality` primary provider |
| `PERPLEXITY_API_KEY` | `pplx-...` | Optional | Alias for `PPLX_API_KEY` |
| `PPLX_MODEL` | `sonar-pro` | Optional | Perplexity model for search grounding |
| `BRAVE_API_KEY` | `BSA...` | Optional | Brave fallback provider when Perplexity is unavailable |

#### Step 3: Set Domain

- **Domain**: `arifosmcp.yourdomain.com` (or use Coolify's auto-generated domain)

#### Step 4: Deploy!

Click **Deploy** → Wait ~2–5 minutes → Done! ✅

**Verify deployment**:
```bash
curl https://arifosmcp.yourdomain.com/health

# Expected output includes: status, service, version, and health_checks
```

**If degraded**: Check logs for Postgres/Redis connection errors. Ensure `DB_PASSWORD` matches in both services.

**Deployment guides**:
- [📘 Coolify Full Guide](docs/DEPLOYMENT_FIREWALL.md)
- [🐳 Docker Compose Standalone](ARCHITECTURE.md)
- [☁️ Cloudflare Workers](https://github.com/ariffazil/arifOS/wiki/Cloudflare)

---

### 3️⃣ Docker Compose (Standalone VPS — 3 Minutes)

For self-managed VPS deployments without Coolify.

**Create `docker-compose.yml`**:

```yaml
version: '3.9'

services:
  arifosmcp:
    image: ghcr.io/ariffazil/arifos:latest
    restart: unless-stopped
    ports:
      - "8080:8080"  # SSE primary transport
      - "8089:8089"  # MCP HTTP fallback (/mcp)
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: vault999
      POSTGRES_USER: arifos
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U arifos"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Create `.env` file**:
```bash
DB_PASSWORD=your-strong-secret-here
ARIF_JWT_SECRET=$(openssl rand -hex 32)
DATABASE_URL=postgresql://arifos:${DB_PASSWORD}@postgres:5432/vault999
REDIS_URL=redis://redis:6379/0
AAA_MCP_OUTPUT_MODE=user
```

**Deploy**:
```bash
docker compose up -d

# Check logs
docker compose logs -f arifosmcp

# Verify SSE primary
curl -N --max-time 2 http://localhost:8080/sse

# Verify MCP fallback
curl http://localhost:8089/health
```

**Production hardening**: See [DEPLOYMENT_FIREWALL.md](docs/DEPLOYMENT_FIREWALL.md) for Nginx, SSL, and monitoring setup.

---

### 4️⃣ ChatGPT Integration (Developer Mode — 1 Minute)

Connect arifOS to ChatGPT as a custom tool provider.

1. **Enable Developer Mode**: ChatGPT Settings → Beta Features → Developer Mode
2. **Create Connector**:
   - Name: `arifOS Constitutional Governance`
   - URL: `https://arifosmcp.yourdomain.com/mcp` (HTTP fallback)
   - Auth: None (or Bearer token if `ARIF_JWT_SECRET` is set)
3. **Add to Chat**: Click "Tools" → Select "arifOS" → Start asking governed questions

**Example prompts**:
- "Use `judge_soul` to evaluate: Should we deploy this AI model to production?"
- "Run `seal_vault` to commit this decision to the constitutional ledger"

**Full guide**: [ChatGPT Integration Wiki](https://github.com/ariffazil/arifOS/wiki/ChatGPT)

---

## 📖 Documentation

### Core Concepts

| Document | Description | Link |
|----------|-------------|------|
| **Constitutional Law** | The 13 Floors (F1-F13) explained | [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md) |
| **Architecture** | System design and deployment | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **Trinity (Δ Ω Ψ)** | AGI-ASI-APEX parallel consensus | [000_THEORY/010_TRINITY.md](000_THEORY/010_TRINITY.md) |
| **MCP Tools Reference** | Unified 20 tools + resources/prompts | [aaa_mcp/README.md](aaa_mcp/README.md) |
| **Deployment Guide** | Production hardening checklist | [docs/DEPLOYMENT_FIREWALL.md](docs/DEPLOYMENT_FIREWALL.md) |

### The 13 Constitutional Floors

Every AI output must pass all 13 floors before reaching the user:

| Floor | Name | Symbol | Threshold | What It Enforces |
|-------|------|--------|-----------|------------------|
| **F1** | Amanah (Trust) | 🔒 | Reversibility | All actions must be reversible. Sacred trust preserved. |
| **F2** | Truth | τ | ≥ 0.99 | Factual accuracy. Evidence-based claims only. |
| **F3** | Tri-Witness | Δ Ω Ψ | Consensus | AGI-ASI-APEX must agree in parallel. |
| **F4** | Clarity | ΔS | ≤ 0 | Reduce confusion (entropy). No jargon without definition. |
| **F5** | Peace² | κ² | ≥ 1.0 | Safety for all stakeholders. De-escalation mandatory. |
| **F6** | Empathy | κᵣ | ≥ 0.7 | Care for the weakest stakeholder. |
| **F7** | Humility | Ω₀ | [0.03, 0.05] | Admit uncertainty (3-5%). Never claim 100% certainty. |
| **F8** | Genius (Coherence) | Ψ | ≥ 0.80 | Output must be internally consistent. |
| **F9** | Anti-Hantu | 👻 | VOID | No consciousness claims. No "I feel" statements. |
| **F10** | Ontology Lock | 🔐 | LOCK | Reality is grounded. No invented physics. |
| **F11** | Authority (SABAR) | ⏳ | 72h | High-risk changes require 72-hour cooling period. |
| **F12** | Injection Guard | 🛡️ | BLOCK | Reject prompt injection attacks immediately. |
| **F13** | Sovereignty | 👑 | VETO | Human has final authority. Never bypass human veto. |

**Deep dive**: [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md) — Full constitutional specification with mathematical proofs.

---

## 🏗️ Architecture

### The Trinity (Δ Ω Ψ)

arifOS evaluates every decision through **three parallel engines**:

```
┌─────────────────────────────────────────────────────────┐
│                   TRINITY CONSENSUS                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────┐  │
│   │  AGI (Δ)     │   │  ASI (Ω)     │   │ APEX (Ψ) │  │
│   │  Mind/Logic  │   │  Heart/Safety│   │ Soul/Law │  │
│   └──────┬───────┘   └──────┬───────┘   └─────┬────┘  │
│          │                  │                  │        │
│          ▼                  ▼                  ▼        │
│   ┌───────────────────────────────────────────────┐    │
│   │   Is it TRUE?    Is it SAFE?    Is it LAWFUL? │    │
│   │   τ ≥ 0.99       Peace² ≥ 1.0    F1-F13 ✓    │    │
│   └───────────────────────────────────────────────┘    │
│                          │                              │
│                          ▼                              │
│              ┌───────────────────────┐                  │
│              │  Verdict:             │                  │
│              │  • SEAL (All agree)   │                  │
│              │  • SABAR (Need human) │                  │
│              │  • VOID (Violation)   │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

### System Layers

```
┌─────────────────────────────────────────────────────────┐
│  L7: Ecosystem (ChatGPT, Claude, Gemini integrations)  │
├─────────────────────────────────────────────────────────┤
│  L6: Applications (333_APPS/ — Prompts, APIs, Agents)  │
├─────────────────────────────────────────────────────────┤
│  L5: MCP Protocol (aaa_mcp/ — Tool surface)            │
├─────────────────────────────────────────────────────────┤
│  L4: Governance (aclip_cai/ — 9-Sense Infrastructure)  │
├─────────────────────────────────────────────────────────┤
│  L3: Organs (core/organs/ — 7 decision modules)        │
├─────────────────────────────────────────────────────────┤
│  L2: Shared Types (core/shared/ — Constitutional types)│
├─────────────────────────────────────────────────────────┤
│  L1: Theory (000_THEORY/ — Mathematical foundations)   │
├─────────────────────────────────────────────────────────┤
│  L0: Kernel (IMMUTABLE — Constitutional invariants)    │
└─────────────────────────────────────────────────────────┘
```

**Key principle**: **L0 is read-only**. No amount of user input can modify constitutional floors.

**Architecture deep dive**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🛠️ MCP Surface

### Canonical Source of Truth 🧰
To prevent documentation drift, please note:
- **The live `tools/list` output is the absolute canonical source of truth** for all available MCP tools.
- The tables below are generated from it and represent stable UX verbs (`anchor_session`, `reason_mind`, etc.). Legacy internal names (`init_gate`, `agi_sense`, etc.) may still exist in older documentation or fallbacks but are superseded by the 13 canonical verbs on the primary surface.
- The telemetry schema is versioned; all system health statuses (e.g., `status: "ALIVE"`) are structurally distinct from governance verdicts (`verdict: "SEAL"`, `SABAR`, `VOID`).

Current canonical AAA MCP server exposes:

- **13 tools**
- **2 resources** (`arifos://aaa/schemas`, `arifos://aaa/full-context-pack`)
- **1 prompt** (`arifos.prompt.aaa_chain`)

### Canonical Tool Taxonomy (13) 🏛️

The following table serves as the **unified audit map** for arifOS. It aligns the **Stable UX Verbs** (Public MCP) with their **Kernel Aliases**, **Trinity Lanes**, and **Constitutional Floor** bindings.

| Tool (UX Verb) | Kernel Alias | Trinity | Stage | Floors | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `anchor_session` | `init_session` | Δ Delta | 000 | F11, F12, F13 | Session ignition & injection defense |
| `reason_mind` | `agi_cognition` | Δ Delta | 333 | F2, F4, F7, F8 | AGI cognition & logic grounding |
| `recall_memory` | `phoenix_recall` | Ω Omega | 444 | F4, F7, F13 | Associative memory traces |
| `simulate_heart` | `asi_empathy` | Ω Omega | 555 | F4, F5, F6 | Stakeholder impact & care constraints |
| `critique_thought`| - | Ω Omega | 666 | F4, F7, F8 | 7-organ alignment & bias critique |
| `judge_soul` | `apex_verdict` | Ψ Psi | 888 | F1-F13 | Sovereign verdict synthesis |
| `forge_hand` | `sovereign_actuator`| Ψ Psi | 777 | F1, F11, F12 | Sandboxed action execution |
| `seal_vault` | `vault_seal` | Ψ Psi | 999 | F1, F3, F10 | Immutable ledger persistence |
| `search_reality` | `search` | Δ Delta | 111 | F2, F4, F12 | Web grounding (Perplexity/Brave) |
| `fetch_content` | `fetch` | Δ Delta | 444 | F2, F4, F12 | Raw evidence content retrieval |
| `inspect_file` | `fs_inspect` | Δ Delta | 111 | F1, F4, F11 | Filesystem inspection (read-only) |
| `audit_rules` | `system_audit` | Δ Delta | 333 | F2, F8, F10 | Rule & governance audit checks |
| `check_vital` | `get_health` | Ω Omega | 555 | F4, F5, F7 | System health & vital signs |

> **Note on Telemetry:** The `verdict` field in telemetry records (e.g., `SEAL`, `SABAR`, `VOID`) is a **governance outcome**. System status indicators (e.g., `status: "ALIVE"`) are strictly **operational telemetry** and do not satisfy constitutional requirements.

**Verdicts:** `SEAL` | `VOID` | `PARTIAL` | `SABAR` | `888_HOLD`

---

## 🧪 Testing & Validation

arifOS includes **production-grade testing** with **constitutional validation**:

```bash
# Run all tests
python test_all_tools_live.py

# Run specific test block
python test_all_tools_live.py --block governance

# Run edge case tests (F12 injection, F9 consciousness claims)
python test_all_tools_live.py --block edge_cases

# Run in CI mode (JSON output)
python test_all_tools_live.py --ci
```

**Test coverage focus**:
- ✅ Constitutional floor validation suites (`tests/constitutional/`)
- ✅ Injection and anti-hantu guard checks
- ✅ Transport and entrypoint contract tests
- ✅ Integration and workflow-level tests

**Test dashboard**: [Live Dashboard](https://674a01a3.arifosmcp-truth-claim.pages.dev)

**Test suite guide**: [tests/mcp_live/README.md](tests/mcp_live/README.md)

---

## 🔒 Production Hardening

### 🛡️ Security at a Glance

| Feature | Status | Notes |
|---------|--------|-------|
| **Authentication** | ✅ JWT Support | Set `ARIF_JWT_SECRET` for bearer token auth |
| **TLS Termination** | ✅ Recommended | Use Nginx/Coolify/Cloudflare for SSL |
| **Audit Ledger** | ✅ VAULT999 (Immutable ledger) | Cryptographic hash chain with Postgres persistence |
| **Rate Limiting** | ⚠️ Deployment-level | Configure at reverse proxy (Nginx/Cloudflare) |
| **Secrets Handling** | ✅ Environment vars | Never commit credentials; use `.env` files |
| **Metrics Export** | ✅ Prometheus-compatible | Available at `/metrics` endpoint |
| **Data Retention** | ✅ Configurable | Postgres backups + VAULT999 snapshots |
| **RBAC** | 🚧 Roadmap | Per-floor role-based access control (planned) |

### Security Checklist

- [ ] **HTTPS**: Force SSL termination in Nginx/Coolify
- [ ] **Authentication**: Enable `ARIF_JWT_SECRET` + JWT middleware
- [ ] **Firewall**: Whitelist IPs, block unauthorized access
- [ ] **Secrets**: Use environment variables, never commit to Git
- [ ] **Backups**: Schedule `postgres_data` + `VAULT999/` backups
- [ ] **Monitoring**: Enable Prometheus metrics at `/metrics`
- [ ] **Rate Limiting**: Prevent DoS attacks (e.g., 100 req/min per IP)
- [ ] **RBAC**: Role-Based Access Control per floor (roadmap)

**Full guide**: [docs/DEPLOYMENT_FIREWALL.md](docs/DEPLOYMENT_FIREWALL.md)

### Scaling

arifOS is **stateless per request**:
- ✅ Add replicas behind a load balancer
- ✅ Horizontal scaling via Docker Swarm or Kubernetes
- ✅ Redis cache for session state
- ✅ Postgres read replicas for VAULT999

**Kubernetes deployment**: [deployment/k8s/](deployment/k8s/)

### Monitoring

**Prometheus metrics** available at `/metrics`:

```yaml
# arifOS custom metrics
arifos_floor_violations_total{floor="F1"}  # Count of F1 violations
arifos_verdict_total{verdict="SEAL"}       # Count of SEAL verdicts
arifos_request_duration_seconds            # Request latency
arifos_genius_score                        # Average Genius score
arifos_entropy_delta                       # ΔS (clarity metric)
```

**Grafana dashboard**: [deployment/grafana/dashboards/arifos.yaml](deployment/grafana/dashboards/arifos.yaml)

---

## 🤝 Contributing

**arifOS is open-source (AGPL-3.0)** and welcomes contributions!

### Development Setup

```bash
# Clone repository
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check . --line-length 100
black . --line-length 100

# Run type checking
mypy .
```

### Contribution Guidelines

1. **Focus on core purity**: Constitutional floors (F1-F13) are immutable
2. **Floor rigor**: Every PR must maintain all 13 floors
3. **MCP compliance**: Tools must follow Model Context Protocol spec
4. **Tests required**: Add tests for all new features
5. **Documentation**: Update relevant `.md` files

**Read the full guide**: [CONTRIBUTING.md](CONTRIBUTING.md)

### The arifOS Oath

> *Every output must reduce confusion. Intelligence is a responsibility, not a right.*

---

## 🎬 Demo Video

**Watch arifOS in Action** (5 minutes):

[![arifOS Demo Video](https://img.youtube.com/vi/AJ92efMy1ns/maxresdefault.jpg)](https://youtu.be/AJ92efMy1ns)

**Click to watch**: [YouTube Demo](https://youtu.be/AJ92efMy1ns)

Learn how arifOS enforces constitutional governance, blocks hallucinations, and maintains human sovereignty in real-time.

---

## 🌍 Community & Support

- **Discord**: [Join arifOS Discord](https://discord.gg/arifos) (coming soon)
- **GitHub Issues**: [Report bugs or request features](https://github.com/ariffazil/arifOS/issues)
- **Email**: arifbfazil@gmail.com
- **Twitter/X**: [@arifbfazil](https://twitter.com/arifbfazil)
- **YouTube**: [arifOS Channel](https://youtube.com/@arifbfazil)

**Commercial support**: Email for enterprise licensing and support contracts.

---

## ⚖️ License

**AGPL-3.0-only** — See [LICENSE](LICENSE) for details.

### What This Means

**✅ You CAN:**
- Use arifOS freely for any purpose (personal, commercial, research)
- Modify arifOS to fit your needs
- Deploy arifOS internally within your organization
- Distribute modified versions

**⚠️ You MUST:**
- Provide source code to users if you **modify** and **offer arifOS as a network service**
- Keep the AGPL license notice in your derivative works
- Disclose your modifications under AGPL-3.0

**❌ Important Notes:**
- AGPL applies **only if** you modify the code **and** provide it as a service over a network
- No warranty or liability (use at your own risk)
- If you simply **use** arifOS (without modifying), no obligations

### Commercial Licensing

Want to modify arifOS without AGPL obligations?

- **Enterprise license available** → Email arifbfazil@gmail.com
- Includes: Commercial source modifications, priority support, SLA guarantees, custom governance packs

**Why AGPL?** We believe AI governance should be transparent and auditable. If you build on arifOS, your constitutional improvements should benefit the community.

---

## 🔥 Motto

**Ditempa Bukan Diberi** — *Forged, Not Given*

Intelligence is not a gift. It is a thermodynamic work process constrained by energy, time, and the constitutional floors we forge to guide it.

---

## 📊 Live Links

| Resource | URL |
|----------|-----|
| **Live MCP Server** | https://arifosmcp.arif-fazil.com |
| **SSE Primary** | https://arifosmcp.arif-fazil.com/sse |
| **MCP Fallback** | https://arifosmcp.arif-fazil.com/mcp |
| **Health Check** | https://arifosmcp.arif-fazil.com/health |
| **Test Dashboard** | https://674a01a3.arifosmcp-truth-claim.pages.dev |
| **Documentation Site** | https://arifos.arif-fazil.com |
| **GitHub Actions** | https://github.com/ariffazil/arifOS/actions |
| **Docker Image** | ghcr.io/ariffazil/arifos:latest |

---

## 🙏 Acknowledgments

arifOS is built on the shoulders of giants:

- **Model Context Protocol (MCP)**: [Anthropic](https://modelcontextprotocol.io)
- **FastMCP**: [jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **Constitutional AI**: [Anthropic Research](https://www.anthropic.com/index/constitutional-ai-harmlessness-from-ai-feedback)
- **Thermodynamics**: Landauer's Principle + Shannon Entropy

---

<div align="center">

**Made with 🔥 by [Muhammad Arif bin Fazil](https://github.com/ariffazil)**

*HUMAN ↔ THEORY ↔ APPS*

[![GitHub Stars](https://img.shields.io/github/stars/ariffazil/arifOS?style=social)](https://github.com/ariffazil/arifOS)
[![GitHub Forks](https://img.shields.io/github/forks/ariffazil/arifOS?style=social)](https://github.com/ariffazil/arifOS/fork)
[![Follow on Twitter](https://img.shields.io/twitter/follow/arifbfazil?style=social)](https://twitter.com/arifbfazil)

**Ditempa Bukan Diberi 🔥**

</div>
