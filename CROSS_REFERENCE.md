# arifOS Cross-Reference — Navigation Aid

**Purpose:** Find related concepts across documents  
**Version:** 2026.03.13-FORGED

---

## By Concept

### 13 Constitutional Floors

| Floor | Primary Doc | See Also | In Body |
|-------|-------------|----------|---------|
| **F1 Amanah** | `0_KERNEL/FLOORS/F01_AMANAH.md` | `AGENTS/EUREKA_COMPENDIUM.md` | `arifosmcp/AGENTS/capability-manifest.yaml` |
| **F2 Truth** | `0_KERNEL/FLOORS/F02_TRUTH.md` | `PATTERNS/README.md` (P-003) | `arifosmcp/core/shared/floors.py` |
| **F3 Witness** | `0_KERNEL/FLOORS/F03_WITNESS.md` | `PATTERNS/README.md` (P-003) | `arifosmcp/AGENTS/execution_controller.py` |
| **F4 Clarity** | `0_KERNEL/FLOORS/F04_CLARITY.md` | `0_KERNEL/ROOT/K111_PHYSICS.md` | `arifosmcp/core/physics/` |
| **F5 Peace²** | `0_KERNEL/FLOORS/F05_PEACE.md` | `0_KERNEL/ROOT/K555_HEART.md` | — |
| **F6 Empathy** | `0_KERNEL/FLOORS/F06_EMPATHY.md` | `0_KERNEL/ROOT/K555_HEART.md` | `arifosmcp/AGENTS/event-bus.yaml` |
| **F7 Humility** | `0_KERNEL/FLOORS/F07_HUMILITY.md` | `PATTERNS/README.md` (P-007) | — |
| **F8 Genius** | `0_KERNEL/FLOORS/F08_GENIUS.md` | `0_KERNEL/_ARCHIVE/05_GENIUS_EQUATION.md` | `arifosmcp/core/governance/` |
| **F9 Anti-Hantu** | `0_KERNEL/FLOORS/F09_ANTIHANTU.md` | `AGENTS/EUREKA_COMPENDIUM.md` | `.pre-commit-config.yaml` |
| **F10 Ontology** | `0_KERNEL/FLOORS/F10_ONTOLOGY.md` | `AGENTS/A400_SUPERPOWERS.md` | — |
| **F11 Authority** | `0_KERNEL/FLOORS/F11_AUTH.md` | `PATTERNS/README.md` (P-002) | `arifosmcp/AGENTS/agent-identity.yaml` |
| **F12 Injection** | `0_KERNEL/FLOORS/F12_INJECTION.md` | `PATTERNS/README.md` (P-002) | `arifosmcp/core/organs/_0_init.py` |
| **F13 Sovereign** | `0_KERNEL/FLOORS/F13_SOVEREIGN.md` | `AGENTS/EUREKA_COMPENDIUM.md` | `arifosmcp/AGENTS/execution_controller.py` |

### Trinity Architecture (ΔΩΨ)

| Concept | Mind | Body | Pattern |
|---------|------|------|---------|
| **AGI Mind (Δ)** | `0_KERNEL/ROOT/K111_PHYSICS.md` | `arifosmcp/aclip_cai/` | P-001 Metabolic Loop |
| **ASI Heart (Ω)** | `0_KERNEL/ROOT/K555_HEART.md` | `arifosmcp/AGENTS/event-bus.yaml` | P-006 Event-Driven |
| **APEX Soul (Ψ)** | `0_KERNEL/ROOT/K777_APEX.md` | `arifosmcp/core/organs/_3_apex.py` | P-005 Receipt-First |
| **VAULT** | `0_KERNEL/ROOT/K999_VAULT.md` | `arifosmcp/VAULT999/` | P-010 Forensic Replay |

### The 4 Agents

| Agent | Spec | Trinity | Capability | In Body |
|-------|------|---------|------------|---------|
| **A-ARCHITECT** | `AGENTS/A100_ARCHITECT.md` | Δ | READ-PLAN | `arifosmcp/AGENTS/agent-identity.yaml` |
| **A-ENGINEER** | `AGENTS/A200_ENGINEER.md` | Ω | EDIT-WRITE | `arifosmcp/AGENTS/agent-identity.yaml` |
| **A-AUDITOR** | `AGENTS/AGENTS.md` | Ψ | READ-REVIEW | `arifosmcp/AGENTS/agent-identity.yaml` |
| **A-VALIDATOR** | `AGENTS/AGENTS.md` | Ψ | DEPLOY-SEAL | `arifosmcp/AGENTS/agent-identity.yaml` |

---

## By Document Type

### Theory & Philosophy
| Document | Contains | Related |
|----------|----------|---------|
| `EUREKA_COMPENDIUM.md` | 10 core insights | All FLOORS, all AGENTS |
| `0_KERNEL/ROOT/K000_ROOT.md` | Core philosophy | `0_KERNEL/FLOORS/K000_LAW.md` |
| `0_KERNEL/ROOT/K111_PHYSICS.md` | Δ AGI Mind | `0_KERNEL/ROOT/K555_HEART.md` |
| `0_KERNEL/ROOT/K555_HEART.md` | Ω ASI Heart | `0_KERNEL/ROOT/K777_APEX.md` |
| `0_KERNEL/ROOT/K777_APEX.md` | Ψ APEX Soul | `AGENTS/A400_SUPERPOWERS.md` |

### Specifications
| Document | Contains | Related |
|----------|----------|---------|
| `0_KERNEL/spec/K111_SPEC.md` | MCP protocol spec | `0_KERNEL/ROOT/mcp/QUICK_REF.md` |
| `0_KERNEL/ROOT/mcp/QUICK_REF.md` | 13 tools quick ref | `0_KERNEL/spec/K111_SPEC.md` |

### Operations
| Document | Contains | Related |
|----------|----------|---------|
| `OPERATION/O_DEPLOY_MASTER.md` | Deployment guide | `OPERATION/O_MONITORING.md` |
| `OPERATION/O_MONITORING.md` | Observability | `OPERATION/O_ACLIP_BRIDGE.md` |

---

## By Pattern

| Pattern | Location | Implementation |
|---------|----------|----------------|
| **P-001 Metabolic Loop** | `PATTERNS/README.md` | `arifosmcp/core/organs/` |
| **P-002 AKI Airlock** | `PATTERNS/README.md` | `arifosmcp/core/kernel/` |
| **P-003 Tri-Witness** | `PATTERNS/README.md` | `arifosmcp/AGENTS/execution_controller.py` |
| **P-004 Dry-Run** | `PATTERNS/README.md` | `arifosmcp/AGENTS/capability-manifest.yaml` |
| **P-005 Receipt-First** | `PATTERNS/README.md` | `arifosmcp/AGENTS/execution_controller.py` |
| **P-006 Event-Driven** | `PATTERNS/README.md` | `arifosmcp/AGENTS/event-bus.yaml` |
| **P-007 Capability Manifest** | `PATTERNS/README.md` | `arifosmcp/AGENTS/capability-manifest.yaml` |
| **P-008 Memory Ledger** | `PATTERNS/README.md` | `arifosmcp/AGENTS/memory-ledger.yaml` |
| **P-009 Constitutional Decorator** | `PATTERNS/README.md` | `arifosmcp/aaa_mcp/server.py` |
| **P-010 Forensic Replay** | `PATTERNS/README.md` | `arifosmcp/AGENTS/forensic-replay.yaml` |

---

## Mind ↔ Body Bridge

### From Mind to Body
| Mind Concept | Body Implementation |
|--------------|---------------------|
| `0_KERNEL/FLOORS/` | `arifosmcp/core/shared/floors.py` |
| `AGENTS/EUREKA_COMPENDIUM.md` | `arifosmcp/AGENTS/README.md` |
| `AGENTS/A000_HUB.md` | `arifosmcp/AGENTS/agent-identity.yaml` |
| `AGENTS/AGENTS_BRIDGE.md` | `arifosmcp/AGENTS/execution_controller.py` |
| `PATTERNS/README.md` | Throughout `arifosmcp/` codebase |

### From Body to Mind
| Body Implementation | Mind Theory |
|---------------------|-------------|
| `arifosmcp/core/governance_kernel.py` | `0_KERNEL/ROOT/K777_APEX.md` |
| `arifosmcp/aaa_mcp/server.py` | `0_KERNEL/spec/K111_SPEC.md` |
| `arifosmcp/VAULT999/` | `0_KERNEL/ROOT/K999_VAULT.md` |
| `arifosmcp/tests/` | `AGENTS/A110_CANON.md` (Testing) |

---

## Quick Lookup Table

### "Where is X defined?"

| X | Location |
|---|----------|
| **13 Floors** | `0_KERNEL/FLOORS/K000_LAW.md` |
| **Genius Equation** | `0_KERNEL/_ARCHIVE/05_GENIUS_EQUATION.md` |
| **MCP Tools** | `0_KERNEL/ROOT/mcp/QUICK_REF.md` |
| **Agent Roles** | `AGENTS/A000_HUB.md` |
| **TCP Analogy** | `AGENTS/EUREKA_COMPENDIUM.md` |
| **Trinity** | `AGENTS/EUREKA_COMPENDIUM.md` |
| **Metabolic Loop** | `0_KERNEL/ROOT/K000_ROOT.md` |
| **AKI Boundary** | `AGENTS/EUREKA_COMPENDIUM.md` |
| **888_HOLD** | `AGENTS/A110_CANON.md` |
| **VAULT999** | `0_KERNEL/ROOT/K999_VAULT.md` |

---

## Search Index

### Search for "Truth"
- `0_KERNEL/FLOORS/F02_TRUTH.md`
- `AGENTS/EUREKA_COMPENDIUM.md` (F2 section)
- `PATTERNS/README.md` (P-003)

### Search for "Deploy"
- `OPERATION/O_DEPLOY_MASTER.md`
- `AGENTS/AGENTS.md` (VALIDATOR spec)
- `PATTERNS/README.md` (P-004, P-005)

### Search for "Agent"
- `AGENTS/` (entire folder)
- `TEMPLATES/AGENT_SPEC.md`
- `arifosmcp/AGENTS/` (runtime)

### Search for "Pattern"
- `PATTERNS/README.md` (all 10 patterns)
- Throughout codebase as comments

---

*Use Ctrl+F in this document to find connections.*

*DITEMPA BUKAN DIBERI — Forged, Not Given*
