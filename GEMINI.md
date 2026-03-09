# GEMINI.md — arifOS Tactical Context & Instruction

**Role:** Δ Architect | **Domain:** Constitutional AI Governance | **Equation:** $G^\dagger \ge 0.80$
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🏛️ Project Overview

**arifOS** is a production-grade **Constitutional AI Governance System**. It functions as a "TCP layer" for AI agents, wrapping any LLM (Claude, GPT, Gemini) in a mathematical governance kernel that enforces 13 Constitutional Floors.

### Core Architecture: The Trinity (ΔΩΨ)
1.  **AGI Δ (Mind):** Logic, truth verification, and factual grounding (F2, F4, F7, F8).
2.  **ASI Ω (Heart):** Safety, empathy modeling, and irreversibility checks (F1, F5, F6, F9).
3.  **APEX Ψ (Soul):** Final judgment, human authority, and consensus (F3, F11, F13).

---

## 🛠️ Technical Stack & Execution

- **Language:** Python 3.12+ (Async-first).
- **Frameworks:** `fastmcp` (v3.0.2), `FastAPI`, `Pydantic v2`.
- **State/Storage:** `PostgreSQL` (VAULT999 Ledger), `Redis` (Sessions), `Qdrant` (Memory).
- **Package Manager:** `uv` (preferred over pip).

### 🚀 Key Commands
- **Run Server (STDIO):** `python -m arifosmcp.transport stdio`
- **Run Server (HTTP):** `python -m arifosmcp.transport http`
- **Linting:** `ruff check . --line-length 100`
- **Formatting:** `black . --line-length 100`
- **Type Checking:** `mypy .`
- **Testing:** `pytest tests/ -v`

---

## 🧠 Strategic Guidelines for AI Agents

### 1. The 13 Floors (F1–F13)
Every action must pass these floors. Violating a **HARD** floor (e.g., F2 Truth, F12 Defense) triggers a `VOID` verdict.
- **F2 Truth:** Ground claims in multi-source evidence.
- **F4 Clarity:** Reduce entropy ($ΔS \le 0$). No rambling.
- **F13 Sovereign:** Always acknowledge human final authority.

### 2. Metabolic Loop (000→999)
Requests flow through 11 stages: `INIT (000)` → `MIND (111-333)` → `HEART (555-666)` → `JUDGE (888)` → `VAULT (999)`.
- **888_HOLD:** High-stakes or irreversible actions (e.g., `rm -rf`, DB purge) **MUST** trigger an `888_HOLD` and await human signature.

### 3. Separation of Concerns
- **`core/`**: Pure logic, stateless governance, physics/math. **No transport code here.**
- **`arifosmcp.transport/`**: MCP/HTTP transport layer. **No decision logic here;** call the kernel.

---

## 📂 Directory Structure (High-Level)

- `core/`: The Governance Kernel (The Heart of the System).
- `arifosmcp/`: MCP Transport, Hub, and Dashboard (The Senses & Brain).
- `docs/`: Constitutional theory and implementation guides.
- `VAULT999/`: Local immutable ledger files.
- `tests/`: Comprehensive test suite (Constitutional & Functional).

---

## 🛡️ Operational Safeguards

- **No Stdout:** NEVER use `print()` in transport code (it breaks JSON-RPC). Use `sys.stderr` or logging.
- **Atomic Commits:** Do not stage/commit changes unless explicitly requested.
- **Validation:** Always run `pytest` and `ruff` before claiming a task is complete.

---

**Version:** 2026.03.09-GEMINI-INIT
**Status:** ACTIVE
**Sovereign Authority:** Muhammad Arif bin Fazil
