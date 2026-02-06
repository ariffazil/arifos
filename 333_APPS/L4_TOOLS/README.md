# L4_TOOLS — MCP Tool Layer (v55.5-HARDENED)

**Level 4 | 80% Coverage | Medium-High Complexity**

> *"Tools are workflows with code — programmatic enforcement via MCP."*

---

## 🎯 Purpose

L4_TOOLS exposes the arifOS Metabolic Loop as **9 callable MCP tools** that any LLM can invoke. This is the programmatic interface to constitutional governance.

**Key Insight:** This layer is **documentation only**. The actual implementation lives in `aaa_mcp/`.

---

## 📈 Effectiveness Spectrum

```
Coverage:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80%
Cost:      ~$0.10-0.15 per operation
Setup:     2 hours (full integration)
Autonomy:  Medium (AI decides when to call)
```

---

## 📁 Directory Structure (v55.5-HARDENED)

```
L4_TOOLS/
├── README.md                    # This file (documentation)
├── MANIFEST.md                  # Deployment guide
│
└── mcp-configs/                 # Platform-specific MCP configs
    ├── antigravity/             # Gemini/Antigravity config
    ├── claude/                  # Claude Desktop config
    ├── codex/                   # OpenAI Codex config
    └── kimi/                    # Kimi config

ACTUAL IMPLEMENTATION → aaa_mcp/
├── __init__.py                  # Package entry
├── __main__.py                  # CLI entrypoint
├── server.py                    # MCP Server (stdio)
├── bridge.py                    # Constitutional bridge
├── core/                        # Core infrastructure
│   ├── session_manager.py
│   └── tool_registry.py
├── tools/                       # 9 Tool implementations
│   ├── handlers.py              # Tool handlers
│   └── sse_handlers.py          # SSE-specific handlers
├── services/                    # Business logic
├── transports/                  # Transport adapters
│   ├── stdio.py
│   └── sse.py
└── sessions/                    # Session management
```

---

## 🔧 The 9 Canonical MCP Tools

| # | Tool | Stage | Trinity | Floors Enforced | Status |
|---|------|-------|---------|-----------------|--------|
| 1 | `init_gate` | 000 | Gate | F11, F12 | ✅ Production |
| 2 | `agi_sense` | 111 | Δ Mind | F12 | ✅ Production |
| 3 | `agi_think` | 222 | Δ Mind | F4 | ✅ Production |
| 4 | `agi_reason` | 333 | Δ Mind | F2, F4, F7, F10 | ✅ Production |
| 5 | `asi_empathize` | 555 | Ω Heart | F5, F6, F9 | ✅ Production |
| 6 | `asi_align` | 666 | Ω Heart | F9 | ✅ Production |
| 7 | `apex_verdict` | 888 | Ψ Soul | F3, F8, F11 | ✅ Production |
| 8 | `reality_search` | — | External | F7, F10 | ✅ Production |
| 9 | `vault_seal` | 999 | Seal | F1 | ✅ Production |

### Tool Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    arifOS MCP Server v55.5                          │
│                    aaa_mcp/server.py                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  init_gate (000-IGNITION)                                           │
│    ✅ F11: Authority check                                          │
│    ✅ F12: Injection scan                                           │
│                                                                     │
│  agi_sense (111-SENSE) → agi_think (222) → agi_reason (333)        │
│    ✅ F2: Truth τ≥0.99  ✅ F4: Clarity ΔS≤0  ✅ F7: Humility        │
│                                                                     │
│  asi_empathize (555-EMPATHY) → asi_align (666-ALIGN)               │
│    ✅ F5: Peace²  ✅ F6: Empathy κᵣ  ✅ F9: Anti-Hantu              │
│                                                                     │
│  apex_verdict (888-JUDGE) → vault_seal (999-SEAL)                  │
│    ✅ F3: Tri-Witness  ✅ F8: Genius  ✅ F1: Amanah                  │
│                                                                     │
│  reality_search (GROUNDING)                                         │
│    ✅ F7: Humility (External verification)                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Implementation Links

**Canonical Source:** [`aaa_mcp/`](../../aaa_mcp/)

| Component | Location | Lines |
|-----------|----------|-------|
| MCP Server | `aaa_mcp/server.py` | ~950 |
| Bridge | `aaa_mcp/bridge.py` | ~950 |
| Tool Handlers | `aaa_mcp/tools/handlers.py` | ~500 |
| Core Kernels | `codebase/agi/`, `codebase/asi/`, `codebase/apex/` | ~2000 |
| Session Manager | `aaa_mcp/sessions/session_ledger.py` | ~300 |

---

## 🚀 Running the MCP Server

```powershell
# From arifOS root
cd C:\Users\User\arifOS
.\venv\Scripts\Activate.ps1

# stdio transport (Claude Code, Claude Desktop)
python -m aaa_mcp

# SSE transport (Railway, remote clients)
python -m aaa_mcp sse
```

**Workflow Reference:** See [`/.agent/workflows/run-mcp-server.md`](../../.agent/workflows/run-mcp-server.md)

---

## 🛡️ Constitutional Floors Enforced

| Floor | Enforcement | Mechanism | Status |
|-------|-------------|-----------|--------|
| F1 Amanah | ✅ Active | Reversibility checks | Production |
| F2 Truth | ✅ Active | Kernel scoring | Production |
| F3 Tri-Witness | ⚠️ Partial | Multi-agent context needed | Partial |
| F4 Clarity | ✅ Active | Schema validation | Production |
| F5 Peace² | ⚠️ Partial | Safety heuristics | Active |
| F6 Empathy | ⚠️ Partial | Stakeholder heuristics | Active |
| F7 Humility | ✅ Active | Confidence caps | Production |
| F8 Genius | ⚠️ Partial | Depends on AGI/ASI | Partial |
| F9 Anti-Hantu | ⚠️ Partial | Anomaly detection | Active |
| F10 Ontology | ⚠️ Partial | Ontology gate | Active |
| F11 Command Auth | ⚠️ Stub | Permissive stub | Stub |
| F12 Injection | ✅ Active | InjectionGuard | Production |
| F13 Sovereign | ⚠️ Partial | Human token needed | Partial |

---

## 📋 MCP Client Configurations

Platform-specific configs are in `mcp-configs/`:

| Platform | Config | Location |
|----------|--------|----------|
| Claude Desktop | `mcp.json` | `mcp-configs/claude/` |
| Antigravity/Gemini | `mcp.json` | `mcp-configs/antigravity/` |
| Codex | `mcp.json` | `mcp-configs/codex/` |
| Kimi | `mcp.json` | `mcp-configs/kimi/` |

---

## 🚀 Deployment History

### v53.x — MCP Genesis (Archived)
- Initial 3 tools
- stdio only

### v54.x — Production (Archived)
- 7 tools complete
- SSE transport added

### v55.5-HARDENED — Current ✅
- **9 canonical tools**
# stdio/SSE transports
- Renamed package: `mcp/` → `aaa_mcp/`
- Full constitutional enforcement active

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v55.5-HARDENED  
**Last Updated:** 2026-02-06  
**Creed:** DITEMPA BUKAN DIBERI

---

## ✅ Reality Check

| Component | Status | Evidence |
|-----------|--------|----------|
| 9 MCP Tools | ✅ Production | Schema tests pass |
| AGI Engine (Δ) | ✅ Production | 510 LOC |
| ASI Engine (Ω) | ✅ Production | 569 LOC |
| APEX Kernel (Ψ) | ✅ Production | 754 LOC |
| Hard Floors | ✅ Enforced | F1,F4,F7,F10,F12 |
| **Coverage** | **80%** | **As designed** |

---

## 🔗 Related Documents

- [`aaa_mcp/README.md`](../../aaa_mcp/README.md) — MCP package documentation
- [`/.agent/workflows/run-mcp-server.md`](../../.agent/workflows/run-mcp-server.md) — Server startup guide
- [`../L3_WORKFLOW/`](../L3_WORKFLOW/) — Workflow orchestration
- [`../L2_SKILLS/ACTIONS/`](../L2_SKILLS/ACTIONS/) — Atomic actions
