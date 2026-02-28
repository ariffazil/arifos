# CLAUDE.md — The Engineer's Operational Codex

**Role:** Ω Engineer | **Goal:** Safety & Implementation (Stages 444–666)
**Constraint:** P² (Peace Squared) ≥ 1.0 | **License:** AGPL-3.0-only

---

## ⚠️ CRITICAL: The Stdout Wall

**NEVER** use `print()` or write to `stdout` in any tool implementation.
- **Why:** Corrupts JSON-RPC/MCP streams.
- **Fix:** Use `sys.stderr.write()` or `import logging; logger.error()`.

---

## 🏗️ Build & Verify Commands

```bash
# Format & Lint (100 char limit)
black . --line-length 100
ruff check . --fix

# Type Safety (Strict on core/)
mypy .

# Testing (Async mode: auto)
pytest tests/ -v -m constitutional
```

---

## 🗺️ Architectural Boundaries

1.  **Pure Kernel (`core/`):** NO imports from `fastmcp`, `fastapi`, or `starlette`. Logic only.
2.  **Transport Adapter (`aaa_mcp/`):** NO decision logic. Protocol only.
3.  **Backends (`aclip_cai/triad/`):** Where the actual tool work happens.
4.  **Shadowing:** NEVER name a local module `mcp`. Use `arifos_aaa_mcp` or `aaa_mcp`.

---

## ⚡ Execution Trace

`Client` → `aaa_mcp/server.py` → `aclip_cai/triad/` → `core/organs/`

*Full spec available at `docs/00_META/CLAUDE.md`.*
