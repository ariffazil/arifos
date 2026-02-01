# L4_TOOLS — Production MCP Tools

**Level 4 | ~80% Coverage (illustrative) | Medium-High Complexity**

> *"Tools are workflows with code — programmatic enforcement."*

---

## 🎯 Purpose

L4_TOOLS uses the **Model Context Protocol (MCP)** to expose the 000-999 metabolic loop as **9 callable tools** that any LLM can invoke. This is the current reference design for arifOS.

**Endpoints shown are examples** (local/dev); verify before treating them as live.

---

## 📈 Effectiveness Spectrum

```
Coverage:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░ ~80% (illustrative)
Cost:      ~$0.10-0.15 per operation (illustrative)
Setup:     ~2 hours (illustrative)
Autonomy:  Medium (AI decides when to call)
```

---

## 🔧 The 9 Canonical Tools

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AAA MCP SERVER v55.2                             │
│                    codebase/mcp/sse.py                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  init_gate (000-IGNITION)                                           │
│    ⚠️ F11: Authority check (stub)                                    │
│    ✅ F12: Injection scan (Guard)                                   │
│    └── Session creation + budget allocation                         │
│                                                                     │
│  agi_sense (111-SENSE)                                              │
│    ✅ F12: Injection Defense                                        │
│    └── Intent detection & lane routing                              │
│                                                                     │
│  agi_think (222-THINK)                                              │
│    ✅ F4: Clarity (Hypothesis generation)                           │
│    └── Exploration without commitment                               │
│                                                                     │
│  agi_reason (333-REASON)                                            │
│    ✅ F2: Truth verification τ≥0.99                                 │
│    ✅ F4: Clarity check ΔS≤0                                        │
│    ✅ F7: Humility Ω₀∈[0.03,0.05]                                   │
│    └── F10: Ontology validation                                     │
│                                                                     │
│  asi_empathize (555-EMPATHY)                                        │
│    ✅ F5: Peace² ≥1.0                                               │
│    ✅ F6: Empathy κᵣ≥0.70                                           │
│    └── Stakeholder impact analysis                                  │
│                                                                     │
│  asi_align (666-ALIGN)                                              │
│    ✅ F9: Anti-Hantu (Ethics check)                                 │
│    └── Policy & legal alignment                                     │
│                                                                     │
│  apex_verdict (888-JUDGE)                                           │
│    ⚠️ F3: Tri-Witness requires multi-agent context                  │
│    ⚠️ F8: Genius depends on upstream bundles                        │
│    └── Final constitutional judgment                                │
│                                                                     │
│  reality_search (GROUNDING)                                         │
│    ✅ F7: Humility (External citations)                             │
│    └── Brave Search API integration                                 │
│                                                                     │
│  vault_seal (999-SEAL)                                              │
│    ✅ F1: Amanah (Immutability)                                     │
│    └── Merkle DAG ledger commitment                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Implementation Location

**Primary Source:** `codebase/mcp/` (canonical implementation)

**Local Mirror:** `333_APPS/L4_TOOLS/mcp/` (for documentation completeness)

| Component | Primary Location | Local Mirror | Status |
|-----------|-----------------|--------------|--------|
| MCP Server | `codebase/mcp/server.py` | `mcp/server.py` | ✅ Production |
| SSE Transport | `codebase/mcp/sse.py` | `mcp/sse.py` | ✅ Production |
| Tool Registry | `codebase/mcp/core/tool_registry.py` | — | ✅ Production |
| Handlers | `codebase/mcp/tools/canonical_trinity.py` | — | ✅ Production |
| Constitutional Metrics | `codebase/enforcement/` | — | ✅ Production |

> **Note:** Files in `333_APPS/L4_TOOLS/mcp/` are mirrors for documentation completeness. The canonical source remains in `codebase/mcp/`.

---

## 🛡️ Constitutional Floors Enforced

| Floor | Enforcement | Mechanism | Status |
|-------|-------------|-----------|--------|
| F1 Amanah | ⚠️ Partial | Reversibility checks per handler | Active |
| F2 Truth | ✅ | Kernel scoring + schemas | Active |
| F3 Tri-Witness | ⚠️ Partial | Needs multi-agent context | Partial |
| F4 Clarity | ✅ | Schema/type validation | Active |
| F5 Peace² | ⚠️ Partial | Safety heuristics | Active |
| F6 Empathy | ⚠️ Partial | Stakeholder heuristics | Active |
| F7 Humility | ✅ | Confidence caps, external search | Active |
| F8 Genius | ⚠️ Partial | Depends on AGI/ASI inputs | Partial |
| F9 Anti-Hantu | ⚠️ Partial | Anomaly detection heuristics | Active |
| F10 Ontology | ⚠️ Partial | Ontology gate in kernels | Active |
| F11 Command Auth | ⚠️ Stub | AuthorityVerifier permissive | Stub |
| F12 Injection | ✅ | InjectionGuard + patterns | Active |
| F13 Sovereign | ⚠️ Requires human token | Partial |

---

## 🚀 Deployment History

### v53.0 — MCP Genesis (Archived)
- Initial MCP server implementation
- 3 basic tools (_init_, _agi_, _vault_)
- stdio transport only

### v54.0 — Hardening (Archived)
- All 7 tools complete
- Constitutional enforcement hardened
- Rate limiting added

### v55.0-SEAL — Current (reference)
- Example endpoint: https://arif-fazil.com (verify availability)
- Full 9-tool suite in code (Split AGI/ASI/APEX)
- VAULT999 integration present in codebase
- Deep Health Checks & Schema Enforcement enabled in code

---

## 📊 Endpoints (examples — verify before use)

| Endpoint | URL | Status |
|----------|-----|--------|
| Health Check | `https://arif-fazil.com/health` | 📋 Example |
| MCP SSE | `https://arif-fazil.com/mcp` | 📋 Example |
| Dashboard | `https://arif-fazil.com/dashboard` | 📋 Example |
| Metrics | `https://arif-fazil.com/metrics/json` | 📋 Example |

---

## 📊 Use Cases

| Scenario | Tool(s) | Benefit |
|----------|---------|---------|
| Safety evaluation | `asi_empathize` | F1, F5, F6 enforcement |
| Code generation | `agi_reason` + `apex_verdict` | F2, F4, F8 verified |
| Full audit | `init_gate` → ... → `vault_seal` | Complete 000-999 cycle |
| Fact-checking | `reality_search` | External verification |
| Session sealing | `vault_seal` | Immutable record |

---

## 🔗 Next Steps

### Immediate (v55.1)
- [ ] Universal transport layer (stdio/sse/http/websocket)
- [ ] Hardening of F11/F12 stubs

### Future (v56.0)
- [ ] Pluggable session backends (Redis, PostgreSQL)
- [ ] Enterprise SSO integration
- [ ] Multi-tenant architecture

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v55.2 (reference)  
**Live:** [arif-fazil.com](https://arif-fazil.com) *(example endpoint — verify)*  
**Creed:** DITEMPA BUKAN DIBERI
