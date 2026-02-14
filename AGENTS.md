# arifOS Agent Guide (v64.1-GAGI)

**Canon:** `C:/Users/User/arifOS/AGENTS.md`
**Version:** v64.1-GAGI
**Motto:** "DITEMPA BUKAN DIBERI — Forged, Not Given"

---

## 🏗️ Project Overview

**arifOS** is a Constitutional AI Governance System built on the **Model Context Protocol (MCP)**. It embodies a biological intelligence architecture:

| Component | Role | Analogy | Key Responsibilities |
|:---|:---|:---|:---|
| **aaa-mcp** | **The Brain** | ΔΩΨ | Logic (AGI), Ethics (ASI), Judgment (APEX). Enforces 13 Constitutional Floors. |
| **aclip-cai** | **The Senses** | C0-C9 | Observability, Metrics, Logs, Security. Provides "grounding" (F2 Truth). |
| **core/** | **The Kernel** | DNA | Pure decision logic (stateless, pure functions). Shared by Brain and Senses. |
| **scripts/** | **The Body** | Railway | Deployment entry points tailored for hosting environments. |

### Architecture: v64.1-GAGI (Get A Grip Intelligence)
- **Unified Deployment:** `aaa-mcp` and `aclip-cai` run as a single organism on Railway.
- **5-Core Kernel:** 000_INIT, AGI, ASI, APEX, VAULT.
- **10 Sensory Tactics:** C0 (Health) to C9 (Finance).
- **Transport:** SSE (Server-Sent Events) for Railway; Stdio for Local Agents (Kimi).

---

## 🛠️ Technology Stack

| Layer | specific Technologies |
|:---|:---|
| **Language** | Python 3.12+ (Async-first) |
| **Protocol** | Model Context Protocol (MCP) 2024-11-05 |
| **Framework** | `fastmcp`, `starlette` |
| **Data** | `pydantic` v2, `dataclasses` |
| **Storage** | PostgreSQL (Vault), Redis (MindVault), ChromaDB (Memory) |
| **Tooling** | `uv` (package manager), `ruff` (linter), `black` (formatter), `pytest` |

---

## 📂 Project Structure

```text
arifOS/
├── aaa_mcp/                 # [THE BRAIN] Constitutional Governance Server
│   ├── server.py            # Main MCP entry point (5-Core Tools)
│   ├── core/                # Wrapper logic (telemetry, heuristics)
│   └── capabilities/        # T6-T21 Capability Modules
├── aclip_cai/               # [THE SENSES] Sensory & Observability Server
│   ├── server.py            # Standalone MCP entry point (C0-C9 Tools)
│   └── tools/               # Implementation of sensory tools (C0-C9)
├── core/                    # [THE KERNEL] Shared Logic (Pure Python)
│   ├── judgment.py          # Central decision engine (AGI/ASI/APEX)
│   ├── organs/              # Organ implementations
│   └── shared/              # Types, Physics, Floors
├── scripts/                 # [DEPLOYMENT]
│   └── start_server.py      # Railway entry point (Integrates Brain + Senses)
├── tests/                   # Test Suite
├── AGENTS.md                # Agent Playbook (You are here)
├── CLAUDE.md                # Claude-specific rules
└── GEMINI.md                # Gemini-specific rules
```

---

## 🤖 Kimi Code Agent Setup

**Kimi** connects to arifOS via `stdio`. Ensure your `~/.kimi/mcp.json` is configured correctly.

### Configuration (`~/.kimi/mcp.json`)

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "C:/Users/User/arifOS/.venv313/Scripts/python.exe",
      "args": ["-m", "aaa_mcp", "stdio"],
      "env": {
        "PYTHONPATH": "C:/Users/User/arifOS",
        "PYTHONIOENCODING": "utf-8",
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      }
    },
    "aclip-cai": {
      "command": "C:/Users/User/arifOS/.venv313/Scripts/python.exe",
      "args": ["-m", "aclip_cai.server"],
      "env": {
        "PYTHONPATH": "C:/Users/User/arifOS",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**Troubleshooting Kimi Connection:**
1.  **Check Virtual Environment:** Ensure `.venv313` exists and has dependencies (`fastmcp`, `pydantic`, `starlette`).
2.  **Verify Command:** Run `C:/Users/User/arifOS/.venv313/Scripts/python.exe -m aaa_mcp stdio` manually to check for import errors.
3.  **Logs:** Check `~/.kimi/logs/kimi.log`.

---

## 🚀 Build & Run Commands

### Local Development
```bash
# Install dependencies
pip install -e ".[dev]"

# Run AAA-MCP (The Brain)
python -m aaa_mcp

# Run ACLIP-CAI (The Senses)
python -m aclip_cai.server
```

### Deployment (Railway)
The `scripts/start_server.py` script starts the production server.
- **Entry Point:** `scripts/start_server.py`
- **Port:** `PORT` env var (default 8080)
- **Host:** `0.0.0.0`
- **Features:** SSE Transport, Integrated Brain + Senses.

---

## 🧪 Testing Strategies

All agents MUST write tests for new functionality.

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Run tests skipping physics (faster)
ARIFOS_PHYSICS_DISABLED=1 pytest tests/
```

### Key Test Files:
- `tests/test_e2e_core_to_aaa_mcp.py`: End-to-end flow.
- `tests/test_aclip_cai.py`: Sensory tool tests.
- `tests/test_mcp_protocol.py`: Protocol compliance.

---

## 📝 Code Style & Conventions

- **Imports:** `from core.judgment import ...` (Kernel first).
- **Typing:** `pydantic` v2 models for all I/O.
- **Async:** All IO-bound tools MUST be `async`.
- **Error Handling:** Never swallow errors. Return `{"verdict": "VOID", "error": "..."}`.
- **Floors:** Decorate tools with enforced floors: `@constitutional_floor("F2", "F4")`.

---

## 🔐 Security Considerations

1.  **F11 Authority:** `init_session` must validate tokens.
2.  **F12 Injection:** Inputs must be scanned for adversarial patterns.
3.  **F1 Reversibility:** High-stakes actions (DB writes) usually require `888_HOLD`.
4.  **Secrets:** Use environment variables. Never commit keys.

---
**Status:** ALIVE & OBSERVANT
