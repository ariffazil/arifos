# arifOS Agent Guide (v64.2-GAGI)

**Canon:** `C:/Users/User/arifOS/AGENTS.md`
**Version:** v64.2-GAGI
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
| **Tooling** | `uv` (package manager), `ruff`, `black`, `pytest`, `mypy` |

## 🤖 OpenCode Agent Setup

For VPS deployment with OpenCode, ensure:

1. **MCP servers**: Install missing npm packages (`@modelcontextprotocol/server-fetch`, `@modelcontextprotocol/server-git`)
2. **Docker permissions**: Add user to `docker` group for container tools
3. **Configuration**: Update `~/.config/opencode/opencode.json` to reduce server count (keep only `aaa-mcp`, `filesystem`, `fetch`, `git`)
4. **Tool names**: Use the 9 canonical tool names (`anchor`, `reason`, `integrate`, `respond`, `validate`, `align`, `forge`, `audit`, `seal`)
5. **Cross‑platform paths**: Use `python3` and relative `cwd` in `mcp.json`

See [docs/opencode-agent.md](docs/opencode-agent.md) for detailed troubleshooting.

---

## 🚀 Build, Lint, and Test Commands

### Setup
```bash
# Install dependencies
pip install -e ".[dev]"
```

### Formatting, Linting, and Type Checking
```bash
# Format code with Black
black . --line-length 100

# Lint code with Ruff
ruff check . --line-length 100

# Type check with MyPy
mypy .
```

### Testing
All agents MUST write tests for new functionality.

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_e2e_core_to_aaa_mcp.py -v

# Run a specific test class
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName -v

# Run a specific test method
pytest tests/test_e2e_core_to_aaa_mcp.py::TestClassName::test_method_name -v

# Run tests skipping physics (faster)
ARIFOS_PHYSICS_DISABLED=1 pytest tests/
```

### Local Development
```bash
# Run AAA-MCP (The Brain) via stdio
python -m aaa_mcp stdio

# Run AAA-MCP (The Brain) via sse
python -m aaa_mcp sse

# Run ACLIP-CAI (The Senses)
python -m aclip_cai.server
```

---

## 📝 Code Style & Conventions

- **Imports:** Use `from core.judgment import ...` for kernel modules first. Follow with standard library and third-party imports.
- **Formatting:** Code is formatted with `black` using a line length of 100 characters.
- **Typing:** Use `pydantic` v2 models for all I/O. All functions must have type hints.
- **Async:** All I/O-bound tools and functions MUST be `async`.
- **Naming:**
    - Modules: `lowercase_with_underscores`.
    - Classes: `PascalCase`.
    - Functions/Variables: `snake_case`.
    - Constants: `UPPERCASE_WITH_UNDERSCORES`.
- **Error Handling:** Never swallow errors. For MCP tools, return a `{"verdict": "VOID", "error": "..."}` payload. Raise exceptions for internal logic errors.
- **Constitutional Floors:** Decorate tools with enforced floors using `@constitutional_floor("F2", "F4")`. The `@mcp.tool()` decorator should be the outer decorator.

---

## 🤖 Agent & Copilot Guidelines

### High-Stakes Operations (888_HOLD)
The agent MUST trigger an `888_HOLD` and wait for human confirmation for high-stakes operations such as:
- Database operations (DROP, TRUNCATE, DELETE without WHERE)
- Production deployments
- Mass file changes (>10 files)
- Credential/secret handling
- Git history modification (rebase, force push)

### Code-Level Floor Violations
Refer to the following table for common code smells and their fixes related to constitutional floors:

| Floor | Code Smell | Fix |
|---|---|---|
| F1 | Mutates input, hidden side effects | Pure functions, explicit returns |
| F2 | Fabricated data, fake metrics | Empty/null when unknown |
| F3 | Contract mismatch, type lies | Use canonical interfaces |
| F4 | Magic numbers, obscure logic | Named constants, clear params |
| F5 | Destructive defaults, no backup | Safe defaults, preserve state |
| F6 | Only happy path, cryptic errors | Handle edge cases, clear messages |
| F7 | False confidence, fake computation | Admit uncertainty, cap confidence |
| F8 | Bypasses governance, invents patterns | Use established systems |
| F9 | Deceptive naming, hidden behavior | Honest names, transparent logic |

---

## 🔐 Security Considerations

1.  **F11 Authority:** `init_session` must validate tokens. See `codebase/guards/nonce_manager.py`.
2.  **F12 Injection:** Inputs must be scanned for adversarial patterns. See `codebase/guards/injection_guard.py`.
3.  **F1 Reversibility:** High-stakes actions (DB writes) usually require `888_HOLD`.
4.  **Secrets:** Use environment variables. Never commit keys.
5.  **Ontology Guard:** Prevent claims of consciousness or soul. See `codebase/guards/ontology_guard.py`.

---
**Status:** ALIVE & OBSERVANT
