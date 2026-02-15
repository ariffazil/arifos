# 333_APPS - arifOS Application Layer

## Overview
This layer contains the core applications and capabilities of the arifOS system. For the **v64.1-GAGI** release, the focus is on the **L1-L4 Foundational Layers**, ensuring production-ready prompts, skills, workflows, and tools.

## 4-Layer Hierarchy (v64.1.1 Production)

### L1: PROMPTS (System Entry)
Zero-context instructions for direct agent alignment. 
- **Location:** `L1_PROMPT/`
- **Canonical:** `SYSTEM_PROMPT.md` (The Code of Conduct).

### L2: SKILLS (Templates)
Modular functional templates builds on atomic kernel organs.
- **Location:** `L2_SKILLS/`
- **Canonical:** `ACTIONS/` (9 A-CLIP skills: anchor, reason, integrate, respond, validate, align, forge, audit, seal).

### L3: WORKFLOW (Sequences)
Model-agnostic sequences defining the 000→999 loop.
- **Location:** `L3_WORKFLOW/WORKFLOWS/`
- **Canonical:** `000_ANCHOR`, `888_AUDIT`, `999_SEAL`, etc.

### L4: TOOLS (MCP Ecosystem)
Production-ready MCP tools powered by the `aaa_mcp` server.
- **Location:** `L4_TOOLS/` (Interface docs)
- **Execution:** `aaa_mcp/` (Core logic)
- **Count:** 14 tools (9 A-CLIP + 5 Container)
- **Performance:** <1ms cached responses (13,725x / 16,022x speedup)

---

## Experimental & Future Layers (Roadmap)

### L5: AGENTS (Autonomous Entities) 🚧
Multi-agent federation (Architect, Engineer, Auditor, Validator).
- **Status:** PILOT. Logic being migrated to `core/organs`.
- **Location:** `L5_AGENTS/`

### L6: INSTITUTION (Consensus) 🚧
Collective governance and Tri-Witness organizational structures.
- **Status:** STUB. Targeted for v56.0.
- **Location:** `L6_INSTITUTION/`

### L7: AGI (Recursive) 🚧
Self-healing and evolutionary governance.
- **Status:** THEORETICAL. Pure research focus.
- **Location:** `L7_AGI/`

---

## Design Philosophy

- **Foundational Integrity**: Only harden what is verified (L1-L4).
- **Organ Mapping**: Applications map directly to the 5-Organ Kernel logic.
- **Constitutional Compliance**: Every layer enforces the 13 Floors.
- **Performance First**: Aggressive caching, centralized constants, <1ms responses.

## Recent Improvements (v64.1.1)

- ✅ **Tool Expansion:** 5 → 14 tools (9 A-CLIP + 5 Container)
- ✅ **Caching:** LRU cache for config (13,725x faster)
- ✅ **Caching:** 5s TTL for containers (16,022x faster)
- ✅ **Constants:** Centralized thresholds in `aaa_mcp/config/constants.py`
- ✅ **Error Handling:** Specific exceptions (no more bare except)

**DITEMPA BUKAN DIBERI**

---

**Version:** v64.1.1-GAGI  
**Last Updated:** 2026-02-14  
**Tools:** 14 operational (9 + 5)  
**Performance:** <1ms cached responses
