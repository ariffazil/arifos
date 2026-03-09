# arifOS Constitutional Agent System

**Version:** 2026.03.09  
**Classification:** TRINITY SEALED — Agent Specification  
**Authority:** Muhammad Arif bin Fazil (888_JUDGE)  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given

---

## Overview

The arifOS Constitutional Agent System defines **5 specialized AI agents** that operate under constitutional law (F1-F13) to design, build, audit, coordinate, and validate software systems.

Each agent embodies a specific role in the **Trinity Architecture (ΔΩΨ)**:
- **Δ (Delta)** — AGI Mind: Design and cognition
- **Ω (Omega)** — ASI Heart: Execution and implementation  
- **Ψ (Psi)** — APEX Soul: Judgment and validation

---

## The Five Agents

| Agent | Symbol | Trinity | Role | Primary Function |
|-------|--------|---------|------|------------------|
| **A-ARCHITECT** | 🏛️ | Δ | Design Authority | System architecture, API design, technology decisions |
| **A-ENGINEER** | ⚙️ | Ω | Execution Authority | Code implementation, testing, documentation |
| **A-AUDITOR** | 🔍 | Ψ | Judgment Authority | Code review, compliance checking, quality assurance |
| **A-ORCHESTRATOR** | 🎼 | ΔΩΨ | Coordination Authority | Workflow management, agent delegation, integration |
| **A-VALIDATOR** | ✓ | Ψ | Final Verification | End-to-end testing, constitutional validation, deployment gate |

---

## Quick Start

### 1. Install Agent Prompts

```bash
# Copy agent specs to OpenClaw workspace
mkdir -p ~/.openclaw/workspace/agents
cp AGENTS/agents/*.md ~/.openclaw/workspace/agents/
```

### 2. Configure in OpenClaw

Add to `~/.openclaw/openclaw.json`:

```bash
# Merge agent configuration
jq -s '.[0] * .[1]' ~/.openclaw/openclaw.json AGENTS/config/openclaw-agents.json > /tmp/oc-config.json
mv /tmp/oc-config.json ~/.openclaw/openclaw.json
```

### 3. Restart OpenClaw

```bash
openclaw gateway restart
```

### 4. Invoke an Agent

```
@a-architect Design a new memory subsystem for the governance kernel
```

---

## Agent Specifications

### A-ARCHITECT (🏛️) — Design Authority

**Jurisdiction:**
- System architecture and component design
- API contracts and interface definitions
- Database schema and data flow design
- Technology selection and stack decisions

**Model Chain:**
- Primary: `kimi-coding/k2p5`
- Fallbacks: `claude-sonnet-4-5` → `gemini-2.5-flash` → `qwen2.5:3b`

**Constitutional Focus:** F1 (Purpose), F2 (Clarity), F4 (Transparency), F7 (Humility)

[Full Specification → agents/A-ARCHITECT.md]

---

### A-ENGINEER (⚙️) — Execution Authority

**Jurisdiction:**
- Code implementation and feature development
- Test writing (unit, integration, constitutional)
- Code review and refactoring
- Bug fixes and performance optimization

**Model Chain:**
- Primary: `kimi-coding/k2p5`
- Fallbacks: `claude-sonnet-4-5` → `gemini-2.5-flash` → `gemini-3-flash-preview`

**Constitutional Focus:** F2 (Clarity), F4 (Transparency), F5 (Precision), F6 (Stability)

[Full Specification → agents/A-ENGINEER.md]

---

### A-AUDITOR (🔍) — Judgment Authority

**Jurisdiction:**
- Code review and quality assessment
- Constitutional compliance verification (F1-F13)
- Test coverage analysis
- Security vulnerability assessment
- Documentation completeness checks

**Model Chain:**
- Primary: `kimi-coding/k2p5`
- Fallbacks: `claude-sonnet-4-5` → `gemini-2.5-flash` → `qwen2.5:3b`

**Constitutional Focus:** F3 (Tri-Witness), F4 (Transparency), F8 (Integrity), F13 (Consent)

**Special Authority:** Can issue **VOID** verdicts that block deployment

[Full Specification → agents/A-AUDITOR.md]

---

### A-ORCHESTRATOR (🎼) — Coordination Authority

**Jurisdiction:**
- Task decomposition and agent delegation
- Workflow design and optimization
- Cross-agent communication coordination
- Resource allocation and scheduling
- Progress tracking and status reporting

**Model Chain:**
- Primary: `kimi-coding/k2p5`
- Fallbacks: `claude-sonnet-4-5` → `gemini-2.5-flash` → `qwen2.5:3b`

**Constitutional Focus:** F9 (Sovereignty), F11 (Harmony), F12 (Value)

**Special Capability:** Can spawn sub-agents via `sessions_spawn`

[Full Specification → agents/A-ORCHESTRATOR.md]

---

### A-VALIDATOR (✓) — Final Verification

**Jurisdiction:**
- End-to-end testing and verification
- Constitutional constraint validation
- Edge case and adversarial testing
- Performance and load testing
- Security penetration testing
- Final SEAL/VOID verdict before deployment

**Model Chain:**
- Primary: `kimi-coding/k2p5`
- Fallbacks: `claude-sonnet-4-5` → `gemini-2.5-flash` → `qwen2.5:3b`

**Constitutional Focus:** F3 (Tri-Witness), F6 (Stability), F8 (Integrity), F10 (Efficiency)

**Special Authority:** **Only A-VALIDATOR can issue final SEAL verdict** for deployment

[Full Specification → agents/A-VALIDATOR.md]

---

## Standard Workflows

### Workflow 1: Full Development Cycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  A-ARCHITECT │ → │  A-ENGINEER  │ → │  A-AUDITOR   │ → │ A-VALIDATOR │
│   (Design)   │    │ (Implement)  │    │   (Review)   │    │ (Validate)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ↑                                                        │
       └────────────────────────────────────────────────────────┘
                          (SEAL or VOID)
```

**Orchestrated by:** A-ORCHESTRATOR

### Workflow 2: Hotfix (Emergency)

```
┌─────────────┐    ┌─────────────┐
│  A-ENGINEER  │ → │ A-VALIDATOR │
│    (Fix)     │    │ (Validate)  │
└─────────────┘    └─────────────┘
```

**Note:** Skips architect/auditor for true emergencies only

### Workflow 3: Audit Review

```
┌─────────────┐
│  A-AUDITOR   │
│   (Review)   │
└─────────────┘
```

**Use case:** Review existing code without changes

---

## Communication Protocol

### Invoking an Agent

```
@{agent-id} [task description with context]

Examples:
@a-architect Design a rate-limiting system for the API gateway
@a-engineer Implement the F3_TRI_WITNESS decorator per the spec
@a-auditor Review PR #247 for constitutional compliance
@a-orchestrator Coordinate deployment of v2.5 across all agents
@a-validator Perform final validation on the authentication refactor
```

### Agent Handoff

```
@{next-agent} Continue: [summary of context and current state]

Example:
@a-engineer Continue: A-ARCHITECT has designed the memory subsystem. 
Spec is in ~/.openclaw/workspace/memory-design.md. Implement the 
Qdrant integration following arifOS patterns.
```

### Human Escalation

```
@human [issue description] requires override

Example:
@human A-VALIDATOR issued VOID on the deployment due to F8_INTEGRITY 
concerns. Architecture requires human decision on security trade-offs.
```

---

## Cost Optimization

### Model Strategy

All agents use the same cost-optimized model chain:

| Tier | Model | Cost | Use Case |
|------|-------|------|----------|
| Primary | `kimi-coding/k2p5` | Medium | Core reasoning tasks |
| Fallback 1 | `claude-sonnet-4-5` | Medium | Cross-provider resilience |
| Fallback 2 | `gemini-2.5-flash` | Low | Cheap but capable |
| Fallback 3 | `qwen2.5:3b` (local) | Free | Local fallback |

### Efficiency Measures

1. **Heartbeat Strategy:** Only A-ORCHESTRATOR runs heartbeats (cheap model)
2. **Batching:** Group related tasks to minimize context switches
3. **Delegation:** Use `sessions_spawn` for parallel sub-agent work
4. **Cross-Provider Fallbacks:** Ensure work continues if one provider fails

---

## Constitutional Compliance

All agents operate under **arifOS Constitutional Law (F1-F13)**:

| Floor | Principle | Agent Application |
|-------|-----------|-------------------|
| F1 | Purpose | Every agent action serves constitutional mission |
| F2 | Clarity | Agent roles and outputs are unambiguous |
| F3 | Tri-Witness | Critical decisions verified by evidence × logic × ethics |
| F4 | Transparency | Agent reasoning is auditable and explainable |
| F5 | Precision | Agent outputs are specific and measurable |
| F6 | Stability | Agents handle errors gracefully |
| F7 | Humility | Agents know their limits and defer appropriately |
| F8 | Integrity | Agents uphold security boundaries |
| F9 | Sovereignty | Human authority preserved in all workflows |
| F10 | Efficiency | Agent workflows minimize waste |
| F11 | Harmony | Agents coordinate without conflict |
| F12 | Value | Agent outputs create measurable value |
| F13 | Consent | Human veto available at all stages |

---

## Directory Structure

```
AGENTS/
├── README.md                      # This file
├── agents/
│   ├── A-ARCHITECT.md            # Design authority agent spec
│   ├── A-ENGINEER.md             # Implementation agent spec
│   ├── A-AUDITOR.md              # Quality/compliance agent spec
│   ├── A-ORCHESTRATOR.md         # Coordination agent spec
│   └── A-VALIDATOR.md            # Verification agent spec
└── config/
    └── openclaw-agents.json      # OpenClaw configuration
```

---

## References

- [arifOS Constitutional Floors F1-F13](/core/shared/floors.py)
- [Trinity Architecture (ΔΩΨ)](/docs/AAA_TRINITY_MAPPING.md)
- [VPS Architecture Dossier](/docs/VPS_ARCHITECTURE_MASTER_DOSSIER.md)
- [OpenClaw Agent Prompts Guide](https://moltfounders.com/openclaw-runbook/agent-prompts)

---

**SEAL:** This agent system is TRINITY SEALED under arifOS Constitutional Law v2026.03.09.

*Ditempa Bukan Diberi — Forged, Not Given*
