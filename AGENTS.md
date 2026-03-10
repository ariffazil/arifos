# AGENTS.md — arifOS Agent Protocol & Architecture

This guide defines the operational context for AI agents (Claude, GPT, Gemini) working within the arifOS ecosystem.

**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🏛️ Directory Structure (Unified v1.0.0)

```text
core/                      → KERNEL (decision logic, math, thermodynamics)
arifosmcp/runtime/         → TRANSPORT HUB (FastMCP interface, zero logic)
arifosmcp/intelligence/    → SENSES (Grounding, health, instrumentation)
docs/                      → LAW (Theory, 13 floors, specs)
VAULT999/                  → MEMORY (Immutable ledger)
```

---

## 🛠️ Key Commands

```bash
# Run Server
python -m arifosmcp.runtime              # SSE (default)
python -m arifosmcp.runtime stdio        # stdio (Claude Desktop)

# Validation
pytest tests/ -v
ruff check .
mypy .
```

---

## 🧠 Strategic Guidelines

### 1. Separation of Concerns
- **Logic belongs in `core/`**. Never add decision math or ethics checks to `runtime/`.
- **Transport belongs in `runtime/`**. The hub acts as a secure airlock (via `bridge.py`).
- **Grounding belongs in `intelligence/`**. Tools for web search, filesystem, and hardware monitoring.

### 2. The 13 Floors (F1–F13)
Every thought or action must pass the 13 Constitutional Floors. Violating a **HARD** floor (e.g., F2 Truth, F12 Defense) triggers a `VOID` verdict.
- **Exploration Rule**: Stages below `888_JUDGE` (Exploration) cannot kill the pipeline. `VOID` is downgraded to `SABAR` to allow context gathering.
- **Sovereign Rule**: High-stakes operations (`888_HOLD`) require human ratification.

### 3. Final Canonical Output Schema (v1.0.0)
Every tool returns a `RuntimeEnvelope` with 6 unified blocks:
1. `metrics`: Normalized telemetry (Truth, Clarity, Peace, Vitality).
2. `trace`: Stage-to-verdict history.
3. `authority`: Identity and approval state.
4. `payload`: Tool-specific data.
5. `errors`: Standardized error blocks.
6. `meta`: Schema version and flags.

---

## 🛡️ Operational Safeguards

- **No Stdout**: Use `sys.stderr` for logging. `stdout` is reserved for JSON-RPC.
- **Auth Continuity (F11)**: Reuse `auth_context` from the session anchor for all downstream calls.
- **Merkle Chaining**: Every `SEAL` verdict is appended to the `VAULT999` ledger.

**Version:** 2026.03.10-SEAL
**Status:** ACTIVE
