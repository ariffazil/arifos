<div align="center">

<img src="https://raw.githubusercontent.com/ariffazil/arifOS/main/sites/library/static/img/banner_sovereign.png" width="100%" alt="arifOS Ecosystem Banner">

# 🌐 arifOS Ecosystem: THE BODY
### **The World’s First Production-Grade Constitutional AI Governance MCP Server.**

**[📚 THE MIND (Theory)](https://github.com/ariffazil/arifOS)** • **[🏛️ THE BODY (Engine)](https://github.com/ariffazil/arifosmcp)** • **[👤 THE SURFACE (Portal)](https://github.com/ariffazil/ariffazil)**

*Ditempa Bukan Diberi — Forged, Not Given [ΔΩΨ | ARIF]*

---

[![Status](https://img.shields.io/badge/Status-Stationary%20%26%20Enforced-00ffcc.svg?style=flat-square)](https://arifosmcp.arif-fazil.com/health)
[![Architecture](https://img.shields.io/badge/Architecture-Trinity%20ΔΩΨ-7c3aed.svg?style=flat-square)](https://arifos.arif-fazil.com/theory-000)
[![Version](https://img.shields.io/badge/Release-2026.03.13--FORGED-blue.svg?style=flat-square)](https://github.com/ariffazil/arifosmcp/commits/main)
[![Tests](https://img.shields.io/badge/Tests-330+%20Passed-success.svg?style=flat-square)](./tests/)
[![License: AGPL 3.0](https://img.shields.io/badge/License-AGPL%203.0-lightgrey.svg?style=flat-square)](./LICENSE)

---

**A high-performance Model Context Protocol (MCP) implementation of the arifOS Governance Kernel.**  
*13 Immutable Floors • Trinity Engine • VAULT999 Merkle Ledger*

**[→ QUICKSTART](#-quick-start-guide)** | **[→ PROJECT TOPOGRAPHY](#-project-topography-analogous-to-filesystem)** | **[→ TOOL CANON](#-the-canonical-v13-tool-set)** | **[→ ARCHITECTURE](#-the-two-server-architecture)** | **[→ npm @arifos/mcp](https://www.npmjs.com/package/@arifos/mcp)**

</div>

---

## 🏛️ The Core Concept: TCP for AI Agents

**MCP** is the **IP layer** — it provides universal tool-calling conventions.  
**arifOS** is the **TCP layer** — it provides reliability, safety, and order.

In the current AI landscape, agents act as unconstrained statistical engines. They can delete production databases, halluncinate sources, or leak secrets because they lack a **Constitutional Kernel**. `arifosmcp` provides that kernel. It wraps any agentic step in a mathematically enforced metabolic loop, ensuring that intent is verified and consequence is reversible.

### 🧩 System Topography (Analogous to Filesystem)

This repository is structured analogous to the arifOS metabolic organs. Every folder mapped below corresponds to a functional layer of the governance stack:

```mermaid
graph TD
    User([User / AI Agent]) --> Transport[arifosmcp/transport/ - Entry Points]
    Transport --> Router[arifosmcp/runtime/ - Stage 444 Router]
    Router --> Brain[core/ - The Metabolic Kernel]
    
    subgraph "Metabolic Kernel (The Brain)"
        Brain --> Init[core/organs/_0_init.py - F11/F12 Guard]
        Init --> Mind[core/organs/_1_agi.py - Δ Mind Layers]
        Mind --> Heart[core/organs/_2_asi.py - Ω Heart Layers]
        Heart --> Apex[core/organs/_3_apex.py - Ψ Soul Layers]
        Apex --> Vault[core/organs/_4_vault.py - 999 Ledger]
    end
    
    Vault --> Commit[(VAULT999/ - Immutable JSON Ledger)]
    Brain --> Shared[core/shared/ - RUKUN AGI Pillars]
    Brain --> Infrastructure[infrastructure/ - VPS & Docker]
```

---

## 🚀 Quick Start Guide

### 1. Unified Environment Support
arifOS uses `uv` for lightning-fast environment management.
```powershell
# Install dependencies
uv pip install -e ".[dev]"

# Run the Kernel (Governance Surface)
python -m arifosmcp.runtime stdio

# Run the Console (Sensory Surface)
python -m arifosmcp.intelligence.cli http
```

### 2. Standard MCP Configuration
Connect your agent (Claude, Cursor, Kimi) to the `THE BODY`:

```json
{
  "mcpServers": {
    "arifos-kernel": {
      "command": "python",
      "args": ["-m", "arifosmcp.runtime", "stdio"],
      "env": {
        "DATABASE_URL": "postgresql://arifos_admin:password@localhost:5432/arifos_vault",
        "REDIS_URL": "redis://localhost:6379/0"
      }
    }
  }
}
```

---

## 📂 Project Topography: Analogous to Filesystem

### 1. [arifosmcp/](file:///C:/arifosmcp/arifosmcp/) — The Transport Surface
The primary namespace for the MCP delivery layer.
- **[runtime/](file:///C:/arifosmcp/arifosmcp/runtime/)**: The entry point for the "arifos" kernel server.
  - `server.py`: The Main FastAPI/FastMCP hub.
  - `tools.py`: Wrappers for the 9 canonical kernel tools.
  - `resources.py`: Unified resource registry (canon://, governance://).
  - `public_registry.py`: The "Source of Truth" for what is exposed to external agents.
- **[intelligence/](file:///C:/arifosmcp/arifosmcp/intelligence/)**: The "aclip-cai" sensory console.
  - `cli.py`: Entry point for sensory tool surface.
  - `console_tools.py`: Implementations of `system_health`, `process_list`, `fs_inspect`, `log_tail`, `net_status`, `config_flags`, `chroma_query`, etc.
  - `forge_guard`: The intelligence-level gating engine.

### 2. [core/](file:///C:/arifosmcp/core/) — The Metabolic Kernel
The pure logic brain of the system, written to be transport-agnostic.
- **[organs/](file:///C:/arifosmcp/core/organs/)**: Active constitutional enforcement layers.
  - `_0_init.py`: Stage 000 (Airlock). Injection defense and identity binding.
  - `_1_agi.py`: Stage 111-333 (Mind). Truth probes and entropy calculation.
  - `_2_asi.py`: Stage 444-666 (Heart). Empathy simulation and reversibility check.
  - `_3_apex.py`: Stage 777-888 (Soul). Final soul-check and human-seal gating.
  - `_4_vault.py`: Stage 999 (Memory). Ledger signing and sealing.
- **[shared/](file:///C:/arifosmcp/core/shared/)**: The RUKUN AGI Foundations.
  - `physics.py`: Laws of thermodynamics applied to code.
  - `atlas.py`: The governance roadmap.
  - `types.py`: Pydantic contracts for the entire ecosystem.
- **[state/](file:///C:/arifosmcp/core/state/)**: Persistence management.
  - `session_manager.py`: Owning the lifecycle of every governed session.
- **[governance_kernel.py](file:///C:/arifosmcp/core/governance_kernel.py)**: The main state machine for 13-floor enforcement.

### 3. [infrastructure/](file:///C:/arifosmcp/infrastructure/) — The Civilization Web
Configuration for deployment and persistence.
- **`docker-compose.yml`**: The production stack orchestrator.
- **`grafana/`**: Canonical dashboards for Trinity health (Mind/Heart/Soul).
- **`prometheus/`**: Telemetry scraping for entropy metrics.
- **`deploy_from_git.sh`**: The hardened auto-deploy hook for CI/CD.

### 4. [tests/](file:///C:/arifosmcp/tests/) — The Verification Suite
330+ tests ensuring stationary stability of the kernel.
- **`tests/03_constitutional/`**: Tests for F1-F13 floor enforcement.
- **`tests/01_unit/`**: Component-level robustness checks.
- **`tests/02_integration/`**: End-to-end metabolic loop verification.

---

## 🏛️ The Two-Server Architecture

arifOS is deployed as two distinct MCP surfaces to separate **Governance** from **Sensory Input**.

| Server | Entry Point | Role | Purpose |
| :--- | :--- | :--- | :--- |
| **arifos** | `arifosmcp.runtime` | **The Kernel** | Critical path governance (F1-F13). |
| **aclip-cai** | `arifosmcp.intelligence.cli` | **The Console** | Sensory feedback and system inspection. |

---

## 🛠️ The Canonical v13 Tool Set (Kernel Surface)

This is the public contract of the arifOS kernel, as defined in [public_registry.py](file:///C:/arifosmcp/arifosmcp/runtime/public_registry.py).

### 1. **`arifOS_kernel` (Stage 444_ROUTER)**
The main entry point for governed work.
- **Input**: `query` (str), `risk_tier` (enum: low, med, high).
- **Output**: `RuntimeEnvelope` with a verdict (SEAL, VOID, 888_HOLD).
- **Function**: Routes the query through the full metabolic loop (000→999).

### 2. **`search_reality` (Stage 111_SENSE)**
- **Role**: Factual grounding.
- **Function**: Queries real-world sources before the internal reasoning starts.

### 3. **`session_memory` (Stage 555_MEMORY)**
- **Role**: Long-term continuity.
- **Function**: Store/Retrieve/Forget reasoning artifacts across sessions.

### 4. **`bootstrap_identity` (Stage 000_INIT)**
- **Role**: Identity Binding (F11).
- **Function**: Validates the human actor and creates a nonce-verified session.

### 5. **`verify_vault_ledger` (Stage 999_VAULT)**
- **Role**: Immutable Audit.
- **Function**: Verifies the SHA-256 Merkle chain integrity of the ledger.

---

## 🛡️ Constitutional Implementation (The `core/` Brain)

### 1. **The Metabolic Loop (000 → 999)**
Every request travels through a fixed sequence of stages defined in [core/pipeline.py](file:///C:/arifosmcp/core/pipeline.py):
- **000 (Ignition)**: Nonce-verified identity check via [_0_init.py](file:///C:/arifosmcp/core/organs/_0_init.py).
- **111 (Reality Search)**: Fact-finding before reasoning.
- **333 (Judgment)**: Constitutional floor synthesis via [judgment.py](file:///C:/arifosmcp/core/judgment.py).
- **888 (Human Veto)**: Holding destructive actions for sovereign audit.
- **999 (Sealing)**: Committing the trace to [VAULT999/](file:///C:/arifosmcp/VAULT999/).

### 2. **The 13 Floors (F1-F13)**
Enforced in [governance_kernel.py](file:///C:/arifosmcp/core/governance_kernel.py):
- **F1 (Amanah)**: Ensures reversibility. No action is taken that cannot be undone in `THE BODY` (git/rollback).
- **F2 (Truth)**: Claims matched against `search_reality` output. Minimum threshold $\tau \ge 0.99$.
- **F4 (Clarity)**: Entropy tracking via [physics/](file:///C:/arifosmcp/core/physics/). Redundant paths are pruned.
- **F11 (Command Auth)**: Strict identity binding. Prevents unauthorized "prompt-spoofing."
- **F13 (Sovereign)**: The 888_HOLD protocol. Requires explicit human SEAL for destructive ops.

---

## 🚢 Deployment & Infrastructure

The `THE BODY` is production-hardened for a $15/mo VPS environment (Hostinger/Railway).

- **Docker Stack**: [docker-compose.yml](file:///C:/arifosmcp/docker-compose.yml) orchestates 11 services including Traefik, Qdrant, Redis, and Prometheus.
- **Health Checks**: Every service has a Docker healthcheck integrated with the `check_vital` tool.
- **Logging**: All transport logs are sent to `arifosmcp.transport.log` with a rotation policy.

---

## 🧪 Testing & Reliability

arifOS maintains **60%+ Coverage** across 330+ tests.
```bash
# General tests
pytest tests/ -v

# Critical path (Constitutional Floors)
pytest tests/03_constitutional/ -v

# Verification of Ledger
python scripts/verify_vault_merkle.py
```

---

## 🧭 Repository Identity: THE BODY

This repository is **The Execution Engine**.
*   **THE MIND (Theory)**: The 13 Floors and Trinity Theory at [arifOS](https://github.com/ariffazil/arifOS).
*   **THE SURFACE (Portal)**: The human bridge and architect context at [ariffazil](https://github.com/ariffazil/ariffazil).

**DITEMPA BUKAN DIBERI.**  
*Forged, Not Given [ΔΩΨ | ARIF]*
