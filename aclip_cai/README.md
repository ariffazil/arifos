# ACLIP_CAI — The Sovereign Infrastructure Console

**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*  
**Version:** v2026.02.23-FORGE-ACLIP-SEAL  
**Status:** **SEALED**

## Overview

`aclip_cai` is a unified, model-agnostic constitutional infrastructure console for **arifOS**. It exposes exactly **9 canonical triad tools** that any LLM can call via the **Model Context Protocol (MCP)**. It acts as the "nervous system" and "ops layer" between a Large Language Model and the underlying system state.

## The 3 Triads (9 Tools)

### 1. Δ TRIAD — Mind (Logic & Grounding)
- **anchor**: Session ignition + F12 injection scan (Stage 000).
- **reason**: Logical causal tracing (Stage 222).
- **integrate**: Context merging + external memory grounding (Stage 333).

### 2. Ω TRIAD — Heart (Safety & Empathy)
- **respond**: Draft generation with constitutional pre-audit (Stage 444).
- **validate**: Full floor audit (F1-F13) (Stage 555).
- **align**: Ethics, maruah, and Peace² alignment (Stage 666).

### 3. Ψ TRIAD — Soul (Judgment & Sealing)
- **forge**: Solution synthesis and Genius score (Stage 777).
- **audit**: Final Tri-Witness consensus judgment (Stage 888).
- **seal**: Immutable commitment to VAULT999 + Phoenix-72 protocol (Stage 999).

## Quick Start

### Running the Server
```bash
python aclip_cai/mcp_server.py
```
The server exposes an MCP interface on port `8889`.

### Using the CLI
The `ag` CLI provides direct access to the metabolic pipeline:
```bash
# Perception check
python aclip_cai/cli.py sense health

# Ignition
python aclip_cai/cli.py pipeline anchor --user_id arif --context "System check"

# Reason
python aclip_cai/cli.py pipeline reason --hypothesis "CPU is hot" --evidence "temp=85C,load=99%"
```

## Deployment

**Use the root Dockerfile** for production deployment — `aclip_cai` runs inside the main arifOS container:

```bash
# From repo root
docker build -t arifos .
docker run -p 8080:8080 arifos
```

The standalone `aclip_cai/Dockerfile` has been archived to
`_ARCHIVE/2026_03_06_pre_hardening/aclip_cai_Dockerfile_standalone`
(no longer needed).

## Constitutional Compliance
Every tool call in `aclip_cai` is audited by the **Internal Intelligence Kernel**, enforcing:
- **F12 Injection Guard**: Stops prompt injection on every input.
- **F9 Anti-Hantu**: Blocks consciousness claims.
- **F4 Clarity**: Ensures logic reduces information entropy (ΔS ≤ 0).

---

**Authority:** ARIF FAZIL (888 Judge)  
**Creed:** DITEMPA BUKAN DIBERI  
**Seal:** ΔΩΨ
