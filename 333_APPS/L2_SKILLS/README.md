# L2_SKILLS — 13 Unified Skills (v60.3-ARIF)

Level 2 | 13 Unified Skills | ΔS ≤ 0

> *DITEMPA BUKAN DIBERI — Skills unified, not scattered.*

---

## Architecture Overview

The 13 unified skills consolidate the previous scattered skill structure into a cohesive architecture:
- **9 Organ+Verb Skills**: Map 5 constitutional organs to 9 canonical verbs
- **4 Meta Skills**: Cross-cutting concerns (law, protocol, infrastructure, AI/memory)

```
┌─────────────────────────────────────────────────────────┐
│                   13 UNIFIED SKILLS                     │
│              (Organ+Verb + Meta Layer)                  │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐      ┌──────▼──────┐    ┌─────▼──────┐
   │Organ+Verb│      │    Meta     │    │   Meta     │
   │  (9)     │      │   Layer     │    │  Layer     │
   └────┬─────┘      └──────┬──────┘    └─────┬──────┘
        │                   │                 │
   ┌────▼────┐         ┌────▼────┐      ┌─────▼─────┐
   │Δ Ω Ψ   │         │Canon    │      │Infra/AI   │
   │Init     │         │Protocol │      │           │
   └─────────┘         └─────────┘      └───────────┘
```

---

## Organ+Verb Layer (9 Skills)

These map 5 constitutional organs to 9 canonical verbs (some organs have multiple verbs):

| # | Skill | Organ | Verb | Stage | Description | Primary Floors |
|---|-------|-------|------|-------|-------------|----------------|
| 1 | **init-anchor** | 000_INIT | anchor | 000 | Session ignition, injection defense | F4, F11, F12 |
| 2 | **agi-reason** | 111-444_AGI | reason | 222 | AGI cognition, thinking | F2, F4, F7, F8 |
| 3 | **agi-integrate** | 111-444_AGI | integrate | 333 | Context mapping, atlas | F2, F7, F8, F10 |
| 4 | **asi-respond** | 555-666_ASI | respond | 444 | Compassionate output | F4, F5, F6 |
| 5 | **asi-validate** | 555-666_ASI | validate | 555 | Defense, F1/F5/F6 check | F1, F5, F6 |
| 6 | **asi-align** | 555-666_ASI | align | 666 | Harmony, bias critique | F5, F6, F9 |
| 7 | **apex-forge** | 777-888_APEX | forge | 777 | Crystallize execution | F1, F2, F4, F8 |
| 8 | **apex-audit** | 777-888_APEX | audit | 888 | Judge all floors | F1-F13 |
| 9 | **vault-seal** | 999_VAULT | seal | 999 | Immutable commit | F1, F3, F11 |

### Organ Flow

```
000_INIT ──┬──► init-anchor (000)
           │
111-444_AGI┼──► agi-reason (222)
  (Δ Mind) ├──► agi-integrate (333)
           │
555-666_ASI┼──► asi-respond (444)
 (Ω Heart) ├──► asi-validate (555)
           ├──► asi-align (666)
           │
777-888_APEX├──► apex-forge (777)
  (Ψ Soul) ├──► apex-audit (888)
           │
999_VAULT ──┴──► vault-seal (999)
```

---

## Meta Layer (4 Skills)

| # | Skill | Description | Consolidates |
|---|-------|-------------|--------------|
| 10 | **constitution-canon** | F1-F13 canonical law, thresholds | constitution-canon |
| 11 | **mcp-protocol** | 14 MCP tools, transport, envelopes | mcp-protocol |
| 12 | **civ-core** | VPS infrastructure, observability, deploy | vps-civ-core + observability + deploy-pipeline |
| 13 | **ai-memory** | AI gateway, vectors, thermo-ops safety | ai-gateway + memory-vectors + thermo-ops |

---

## Directory Structure

```
333_APPS/L2_SKILLS/
├── README.md                    # This file
├── CONSOLIDATION_v60.md         # Migration documentation
├── skill_templates.yaml         # 9 verb templates
├── mcp_tool_templates.py        # Python wrappers
│
├── constitution-canon/          # Skill 10: F1-F13 law
│   └── SKILL.md
├── mcp-protocol/                # Skill 11: 14 tools
│   └── SKILL.md
│
├── init-anchor/                 # Skill 1: 000_INIT + anchor
│   └── SKILL.md
├── agi-reason/                  # Skill 2: AGI + reason
│   └── SKILL.md
├── agi-integrate/               # Skill 3: AGI + integrate
│   └── SKILL.md
├── asi-respond/                 # Skill 4: ASI + respond
│   └── SKILL.md
├── asi-validate/                # Skill 5: ASI + validate
│   └── SKILL.md
├── asi-align/                   # Skill 6: ASI + align
│   └── SKILL.md
├── apex-forge/                  # Skill 7: APEX + forge
│   └── SKILL.md
├── apex-audit/                  # Skill 8: APEX + audit
│   └── SKILL.md
├── vault-seal/                  # Skill 9: VAULT + seal
│   └── SKILL.md
│
├── civ-core/                    # Skill 12: Infrastructure
│   └── SKILL.md
└── ai-memory/                   # Skill 13: AI + Memory + Safety
    └── SKILL.md
```

**Total: 13 skill directories + 4 metadata files = 17 entries**

---

## Quick Reference: Skill Invocation

### Organ+Verb Skills

```python
# 000_INIT — Session ignition
await skills.init_anchor.anchor(query, session_id)

# 111-444_AGI — Mind operations
await skills.agi_reason.think(query, session_id)           # 222
await skills.agi_integrate.map_context(query, session_id)  # 333

# 555-666_ASI — Heart operations
await skills.asi_respond.generate(plan, stakeholders)      # 444
await skills.asi_validate.check_safety(plan, context)      # 555
await skills.asi_align.critique(plan, session_id)          # 666

# 777-888_APEX — Soul operations
await skills.apex_forge.execute(command, session_id)       # 777
await skills.apex_audit.judge(agi_result, asi_result)      # 888

# 999_VAULT — Final commitment
await skills.vault_seal.commit(session_id, verdict)        # 999
```

### Meta Skills

```python
# 10 — Constitution
await skills.constitution_canon.check_floor("F1")

# 11 — MCP Protocol
await skills.mcp_protocol.call("arifos_aaa_metabolic_loop")

# 12 — Infrastructure
await skills.civ_core.health_check()
await skills.civ_core.deploy()

# 13 — AI + Vector Memory (VM)
# You do not "remember" anything biologically. You query Vector Memory.
await skills.ai_memory.query_vector_memory(query, session_id)  # MCP tool: vector_memory
await skills.ai_memory.route_model("claude")
await skills.ai_memory.hold("888_HOLD")
```

---

## Constitutional Floors by Skill

| Skill | Floors | Constitutional Band |
|-------|--------|---------------------|
| init-anchor | F4, F11, F12 | Ψ Init |
| agi-reason | F2, F4, F7, F8 | Δ Mind |
| agi-integrate | F2, F7, F8, F10 | Δ Mind |
| asi-respond | F4, F5, F6 | Ω Heart |
| asi-validate | F1, F5, F6 | Ω Heart |
| asi-align | F5, F6, F9 | Ω Heart |
| apex-forge | F1, F2, F4, F8 | Ψ Soul |
| apex-audit | F1-F13 (All) | Ψ Soul |
| vault-seal | F1, F3, F11 | Ψ Soul |
| constitution-canon | F1-F13 | Law |
| mcp-protocol | F4, F11, F12 | Protocol |
| civ-core | F1, F5, F11, F12 | Infrastructure |
| ai-memory | F1, F4, F7, F8, F13 | Intelligence |

---

## Consolidation History

**Before:** 24+ scattered skill directories (entropy chaos)
- Individual floor guardians (f1-amanah, f3-tri-witness, etc.)
- Separate organ directories (delta-mind, omega-heart, psi-soul)
- Infrastructure fragmentation (vps-civ-core, observability, deploy-pipeline)
- AI/Vector Memory fragmentation (ai-gateway, memory-vectors, thermo-ops)
- Redundant flow control (trinity-flow, trinity-governance-core)

**After:** 13 unified skills (crystal clarity)
- 9 organ+verb combinations (clear mapping)
- 4 meta skills (consolidated concerns)
- Unified infrastructure (civ-core)
- Unified AI/memory (ai-memory)

**Entropy Reduction:** 24 → 13 skills (46% reduction)

---

## 888_HOLD Triggers by Skill

| Skill | 888_HOLD Conditions |
|-------|---------------------|
| init-anchor | Injection bypass, authority elevation |
| agi-reason | Truth bypass, uncertainty override |
| agi-integrate | Ontology bypass, context tampering |
| asi-respond | Empathy bypass, harmful output |
| asi-validate | Irreversible operations, CRITICAL risk |
| asi-align | Consciousness claims, severe bias |
| apex-forge | Dangerous commands, destructive git ops |
| apex-audit | F3 consensus failure, F13 sovereign override |
| vault-seal | Token verification failure, ledger corruption |
| civ-core | Production deployment, DB migrations |
| ai-memory | Mass operations, conflicting evidence |

---

## Backend Mappings

| Skill | Backend Path | MCP Tool |
|-------|--------------|----------|
| init-anchor | `aclip_cai/triad/psi/anchor.py` | `arifos_aaa_anchor_session` |
| agi-reason | `aclip_cai/triad/delta/reason.py` | `arifos_aaa_reason_mind` |
| agi-integrate | `aclip_cai/triad/delta/integrate.py` | — |
| asi-respond | `aclip_cai/triad/omega/respond.py` | `arifos_aaa_simulate_heart` |
| asi-validate | `aclip_cai/triad/omega/validate.py` | — |
| asi-align | `aclip_cai/triad/omega/align.py` | `arifos_aaa_critique_thought` |
| apex-forge | `aclip_cai/triad/psi/forge.py` | `arifos_aaa_eureka_forge` |
| apex-audit | `aclip_cai/triad/psi/audit.py` | `arifos_aaa_apex_judge` |
| vault-seal | `aclip_cai/triad/psi/seal.py` | `arifos_aaa_seal_vault` |

---

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v60.3-UNIFIED-13  
**Creed:** DITEMPA BUKAN DIBERI  
**Entropy:** ΔS = -46% (24→13)  
**Architecture:** 13 Skills → 9 Verbs → 5 Organs → 3 Trinity → 1 Constitution

---
