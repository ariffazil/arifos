# SABAR — Thermodynamic Cooling State

**SABAR** (Malay: *patience, composure under pressure*) is the fourth constitutional verdict in arifOS, alongside SEAL, HOLD, and VOID.

---

## What SABAR Means

SABAR is a **non-terminal cooling state**. It signals that the system detected instability — ambiguity, contradiction, insufficient grounding, or overload — but the condition is temporary and does not require human intervention.

> *The system is not broken. The system is not asking for help. The system is cooling.*

---

## SABAR vs. HOLD vs. VOID

| Verdict | Meaning | Human needed? | Retry? | Cause |
|---------|---------|--------------|--------|-------|
| **SEAL** | Approved and committed | No | N/A | Operation succeeded |
| **HOLD** | Awaiting human decision | Yes | After human input | Authority/scope gap |
| **SABAR** | Thermodynamic cooling | No | Yes, after delay | Instability, ambiguity |
| **VOID** | Permanent rejection | No | No | Constitutional violation |

**The critical distinction:**
- HOLD blocks until a human acts. It escalates.
- SABAR blocks temporarily then auto-resolves. It cools.
- VOID terminates the intent. It does not retry.

---

## When SABAR Is Emitted

SABAR occurs when:

1. **Ambiguity score too high** — `ambiguity_score ≥ 0.5` in the entropy budget
2. **Contradiction detected** — `contradiction_count > 0` in the reason/critique loop
3. **Grounding insufficient** — reality compass returned no anchoring evidence
4. **Constitutional VOID before stage 888** — pre-judge void is elevated to SABAR (non-terminal)
5. **Qdrant write failed** — vector store temporarily unavailable (engineering_memory)
6. **agi_mind synthesis under entropy pressure** — reason output is unstable

---

## Retry Policy

Every SABAR response includes:

```json
{
  "status": "sabar",
  "payload": {
    "sabar_reason": "Ambiguity score 0.72 exceeds threshold 0.50",
    "retry_after_seconds": 30,
    "cooling_cause": "ambiguity_or_instability",
    "guidance": "System is cooling. Retry after 30s. No human input required."
  }
}
```

**Caller behavior:**
- Wait `retry_after_seconds` before retrying the same call
- Do not escalate to human — SABAR resolves without human action
- If SABAR persists after 3 retries with identical input, reconsider the query structure

---

## Observability

SABAR events are tracked in Prometheus:

```
arifos_sabar_events_total{tool="agi_mind", cause="ambiguity_or_instability"} 3
arifos_sabar_events_total{tool="engineering_memory", cause="qdrant_write_failed"} 1
```

These appear on the Grafana dashboard under **Verdict Distribution**.

---

## In the Metabolic Pipeline

SABAR maps to specific pipeline positions:

| Stage | SABAR meaning |
|-------|--------------|
| `111_SENSE` | Input parsing failed — insufficient structure |
| `222_REASON` | AGI mind synthesis unstable |
| `333_CRITIQUE` | ASI heart detected contradiction |
| `444_ROUTER` | Pipeline routing ambiguous |
| `555_MEMORY` | Vector store unavailable |
| `<888_JUDGE` | Pre-judge VOID elevated to SABAR |

Stage 888 (`888_JUDGE`) and above may emit VOID directly. Below 888, constitutional violations surface as SABAR to allow cooling and retry before final judgment.

---

## The Thermodynamic Basis

SABAR is grounded in the APEX stability formula:

```
G = (A × P × X × E²) × |ΔS| / C ≥ 0.80
```

When G falls below threshold due to high entropy (ΔS > 0), the system enters SABAR rather than VOID. This follows from the principle that **entropy can be reduced through cooling** — not every high-entropy moment is a violation.

> *SABAR is the system saying: I measured disorder. I am restoring order. Wait.*

---

*Last updated: 2026-03-22*
*See also: POSITIONING.md, LICENSING.md, contracts_v2.py `ToolEnvelope.sabar()`*
