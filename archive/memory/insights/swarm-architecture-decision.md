# Insight: Swarm Architecture Decision

**Source**: 2026-03-13 session  
**Pattern Type**: Architectural/Strategic

## Decision

Prioritized **Swarm Architecture** over **ICRL** (In-Context Reinforcement Learning) for agent orchestration.

| Approach | Mechanism | Alignment |
|----------|-----------|-----------|
| ICRL | Training single agent | Skill acquisition |
| Swarm | Orchestrating multiple agents | Governance, decomposition, synthesis |

## Rationale

Core function is orchestration ("factory") not individual skill acquisition ("forge"). Thermodynamic metaphor: swarm manages entropy gradients across agents; ICRL optimizes single-agent state transitions.

## Implementation

Proposed NVIDIA market brief as proof-of-concept:
- Orchestrator (decompose/synthesize)
- ResearcherAgent (data gathering)
- AnalystAgent (sentiment analysis)

## Status

Pending — awaiting stable foundation (Kimi API, web_search restored).

---
*Extracted: 2026-03-23 hygiene cycle*
