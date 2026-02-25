---
id: architecture
title: Architecture
sidebar_position: 6
description: The L0-L7 stack, Trinity engines (DeltaOmegaPsi), MCP transports, and the 000999 metabolic loop.
---

# Architecture

> Source: [`ARCHITECTURE.md`](https://github.com/ariffazil/arifOS/blob/main/ARCHITECTURE.md) . [`000_THEORY/010_TRINITY.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/010_TRINITY.md) . [`000_THEORY/000_ARCHITECTURE.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_ARCHITECTURE.md)

---

## The 8-Layer Stack (L0-L7)

```

 L7: ECOSYSTEM   - Permissionless sovereignty (civilisation-scale)   Research

 L6: INSTITUTION - Trinity consensus (organisational governance)    Stubs

 L5: AGENTS      - Multi-agent federation (coordinated actors)      Pilot

 L4: TOOLS       - MCP ecosystem (individual capabilities)          Production

 L3: WORKFLOW    - 000999 sequences (structured processes)         Production

 L2: SKILLS      - Canonical actions (behavioural primitives)       Production

 L1: PROMPTS     - Zero-context entry (user interface)              Production

 L0: KERNEL      - Intelligence Kernel (DeltaOmegaPsi governance engine)     SEALED
      7 Organs (constitutional pipeline)                      
      9 System Calls (A-CLIP sensory tools)                  
      13 Floors (existential enforcement)                     
      VAULT999 (immutable audit filesystem)                   

```

**Key rule:** L0 is invariant, transport-agnostic constitutional law. L1-L7 are applications that run on it. Swapping models or agents does not bypass L0.

---

## L0: The Intelligence Kernel

L0 is implemented across four distinct layers with strict architectural boundaries:

| Layer | Package | Role | Rule |
|:--|:--|:--|:--|
| **Surface** | `arifos_aaa_mcp/` | Canonical PyPI entry point | Public contracts & REST routes |
| **Transport** | `aaa_mcp/` | MCP transport adapter (stdio/HTTP) | **Zero** decision logic |
| **Intelligence** | `aclip_cai/` | Triad backend & 9-Sense tools | Federation & sensing |
| **Kernel** | `core/` | Pure decision logic, 7 organs, 13 floors | **Zero** transport imports |

Violating these boundaries is a hard rule. `core/` must never import transport or intelligence providers.

---

## The Trinity Engines (DeltaOmegaPsi)

The 000999 pipeline is executed by three thermodynamically isolated engines:

```
000_INIT  AGI Delta (111-333)  ASI Omega (444-666)  APEX Psi (777-888)  VAULT999 (999)
                                                                           
     000  999 feedback loop 
```

| Engine | Symbol | Stages | Role | Floors |
|:--|:--|:--|:--|:--|
| **AGI** | Delta (Mind) | 111-333 | Reasoning, logic, hypothesis | F2, F4, F7, F8 |
| **ASI** | Omega (Heart) | 444-666 | Safety, empathy, alignment | F1, F5, F6, F9 |
| **APEX** | Psi (Soul) | 777-888 | Judgment, verdict, sealing | F3, F8, F11-F13 |

AGI and ASI are **thermodynamically isolated** until stage 444 - they cannot see each other's reasoning until `compute_consensus()` merges them. This prevents confirmation bias between the reasoning and safety engines.

---

## The 7-Organ Sovereign Stack

Implemented in `core/organs/`. arifOS has evolved from a passive oracle into an active, governed agent operating a 7-Organ Sovereign Stack. This represents a transition to the governance of a living, evolving process.

| Organ | Stage | Function |
|:--|:--|:--|
| **INIT** | 000 | Airlock - Session ignition and F11/F12 defense scan |
| **AGI** | 111-444 | Mind - Logic, truth, and hypothesis generation |
| **PHOENIX** | 555 | Subconscious - Dynamic associative memory retrieval. Uses the Humility Band (Ω₀) to soften Jaccard thresholds, and Human Scar-Weight (W_scar) as a historical relevance multiplier. |
| **ASI** | 666 | Heart - Safety, empathy, alignment |
| **APEX** | 777 | Soul - Judgment, verdict, sealing. Tri-witness consensus. |
| **FORGE** | 888 | Hands - Sandboxed execution engine for Thermodynamic State Mutations (ΔS). Rejects any execution without a cryptographically signed ConstitutionalTensor. Irreversible actions trigger an `888_HOLD` intercept, requiring a physical ratification token from the 888 Judge. |
| **VAULT** | 999 | Memory - Immutable VAULT999 ledger commit |

### Steady-State Philosophy
The addition of the Actuator and Phoenix organs represents the transition to the governance of a living process. Real-world emergence is managed by observing anomalies, measuring their entropy impact (ΔS < 0), and adjusting constraints while remaining grounded. AI possesses agency through tools but no soul (The Hantu Warning - F9).

---

## MCP Transports

AAA-MCP exposes transports for different deployment scenarios. They serve the same governance pipeline tool surface.

| Transport | Command | Best for |
|:--|:--|:--|
| **stdio** | `python -m aaa_mcp stdio` | Claude Desktop, Cursor, local IDE integration |
| **Streamable HTTP** (Recommended) | `python -m aaa_mcp http` | Production deployments, cloud services, JSON-RPC integrations |

**Note:** Streamable HTTP is the current MCP standard (2024+), replacing legacy SSE two-channel transport. See [transport architecture](/mcp-server#transport) for details.
| **REST (unified)** | `python server.py --mode rest` | Unified server (governance + observability tools) |

The unified `server.py` at repo root bundles governance pipeline tools plus additional observability/sensory tools into one server. The standalone `aaa_mcp/server.py` provides the governance pipeline transport.

---

## VAULT999 - Immutable Audit Ledger

Every decision flows through VAULT999 at stage 999:

- **Append-only** - entries are never deleted or modified
- **Hash-chained** - each entry cryptographically linked to the previous (Merkle tree)
- **Tamper-evident** - any modification breaks `verify_chain()`
- **Independent** - truth lives in the vault, not in the AI's context window

VAULT999 is forensic memory, not LLM memory. It survives container restarts, model replacement, and AI failure.

```
core/organs/_4_vault.py    seal logic
VAULT999/                   local filesystem ledger (SQLite or Postgres)
```

---

## Verdict Hierarchy

When floor results are merged, harder verdicts always take precedence:

```
SABAR > VOID > 888_HOLD > PARTIAL > SEAL
```

- **SEAL** - All floors pass; cryptographically approved
- **SABAR** - Soft floor violated; pause and refine
- **VOID** - Hard floor failed; rejected, cannot proceed
- **888_HOLD** - Governance deadlock; escalate to human judge
- **PARTIAL** - Soft floor warning; proceed with caution

---

## Infrastructure Components

```

   AI Clients (Claude Desktop / OpenClaw / ChatGPT)       
        stdio / SSE / HTTP                                

                         
              
                server.py (root)      Unified MCP server
                Port: 8080/8089    
              
                         
           
                                     
      
      PostgreSQL     Redis     VAULT999  
      (VAULT999)   (Cache)    (local)   
      
```

- **PostgreSQL** - VAULT999 persistent ledger (optional; falls back to SQLite/filesystem)
- **Redis** - Session state cache (optional; falls back to in-memory)
- **Nginx / Cloudflare** - TLS termination, proxy to `127.0.0.1:8080`

See [`DEPLOYMENT.md`](https://github.com/ariffazil/arifOS/blob/main/DEPLOYMENT.md) for Nginx config examples and Docker Compose setup.
