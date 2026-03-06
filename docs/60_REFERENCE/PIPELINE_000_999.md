# arifOS 000→999 Pipeline Flow

**Version**: 2026-03-06 · CODE-VERIFIED  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## Entrypoint Hierarchy

```
User → python -m arifos_aaa_mcp {stdio|http|sse}
     OR python server.py --mode {stdio|http|sse}
           ↓
    arifos_aaa_mcp/server.py  (PUBLIC surface — canonical external entrypoint)
           ↓
    aaa_mcp/server.py         (INTERNAL 13-tool FastMCP instance)
           ↓
    aclip_cai/triad/*         (Intelligence layer: Δ Mind / Ω Heart / Ψ Soul)
           ↓
    core/pipeline.py → core/organs/_0_init.py … _4_vault.py
```

> **server.py (root)** is the friendly CLI wrapper; it calls
> `arifos_aaa_mcp.server.create_aaa_mcp_server()` and supports
> `--mode stdio|http|sse|rest`.

---

## Stage-by-Stage Execution

| Stage | Organ | Function | Floors | Notes |
|-------|-------|----------|--------|-------|
| **000** | `_0_init.py` | `init()` | F11, F12 | Session init + injection/auth scan |
| **111** | `_1_agi.py` | `sense()` | — | Lane classification |
| **222** | `_1_agi.py` | `think()` | F7 | **INTERNAL** — runs inside `reason_mind`, NOT exposed as MCP tool |
| **333** | `_1_agi.py` | `reason()` | F2, F4, F8 | Produces ConstitutionalTensor |
| **444** | `_3_apex.py` | `sync()` | — | AGI + ASI tensor merge |
| **555** | `_2_asi.py` | `empathize()` | F5, F6 | Stakeholder impact |
| **666** | `_2_asi.py` | `align()` | F9, F10 | Ethics + anti-deception alignment |
| **777** | `_3_apex.py` | `forge()` | F8 | Solution synthesis (Genius score) |
| **888** | `_3_apex.py` | `judge()` | F3, F8, F9, F10, F13 | Sovereign verdict → `governance_token` |
| **999** | `_4_vault.py` | `seal()` | F1, F3 | Immutable ledger write |

---

## 13 MCP Tool Surface

All 13 tools are defined in `aaa_mcp/server.py` and exposed through
`arifos_aaa_mcp/server.py`.

| Tool | Stage(s) | Category | Internal Stages |
|------|----------|----------|-----------------|
| `anchor_session` | 000 | Governance | — |
| `reason_mind` | 111–444 | Governance | **222 THINK (hidden)** |
| `recall_memory` | 444/555 | Governance | Phoenix-72 |
| `simulate_heart` | 555–666 | Governance | — |
| `critique_thought` | 666 | Governance | — |
| `apex_judge` | 888 | Governance | Generates `governance_token` |
| `eureka_forge` | 777 | Governance | — |
| `seal_vault` | 999 | Governance | **Requires `governance_token`** |
| `search_reality` | — | Utility | Web search / evidence |
| `fetch_content` | — | Utility | URL fetch |
| `inspect_file` | — | Utility | Filesystem read |
| `audit_rules` | — | Utility | Governance health |
| `check_vital` | — | Utility | System telemetry |

**CRITICAL**: Stage 222 (THINK) is **NOT EXPOSED** as an MCP tool.
It executes inside `reason_mind` before Stage 333 (REASON).

---

## Amanah Handshake (Token-Locked Sealing)

```
apex_judge (888)
    → signs governance_token = "{verdict}:{hmac_sha256(session_id)}"
                  ↓
seal_vault (999)
    → REQUIRES valid governance_token from apex_judge
                  ↓
Invalid / missing token → verdict: VOID  (no ledger write)
```

`seal_vault` cannot be called without a valid `governance_token` produced
by `apex_judge` in the same session.  This prevents ledger writes that
bypass the 888 verdict stage.

---

## Constitutional Floor Execution Order

```
F12 (Injection)  →  F11 (Command Auth)        [Walls — first, always]
        ↓
F1 (Amanah)  F2 (Truth)  F4 (Clarity)  F7 (Humility)   [AGI Hard floors]
        ↓
F5 (Peace²)  F6 (Empathy)  F9 (Anti-Hantu)              [ASI Soft floors]
        ↓
F3 (Tri-Witness)  F8 (Genius)                            [Mirror floors]
        ↓
F10 (Ontology)  F13 (Sovereign)                          [Ontology / Veto]
        ↓
Ledger (VAULT999)
```

Hard floor failure → **VOID**.  Soft floor failure → **PARTIAL**.

---

**DITEMPA BUKAN DIBERI** — Code is truth, documentation follows.
