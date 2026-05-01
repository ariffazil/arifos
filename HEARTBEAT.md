# HEARTBEAT.md — Runtime Liveness Signal

**Version:** 2026.05.01
**Purpose:** Live runtime pulse — answers "are we stable, should we continue, pause, escalate, or seal?"

This file changes on every loop iteration. It is not durable memory — it is a live
instrument panel.

---

## Update Protocol

**Before each major action:** Read, check risk_level, check loop_count, check blockers.
**After each major action:** Update: current_stage, entropy_delta, loop_count, last_action, timestamp.

If `risk_level` rises to `critical` OR `loop_count` > 20: **pause and summarize before proceeding.**

---

## Current Session State

```yaml
session_id:     null          # Set on session init; format: {uuid}
status:         idle          # idle | active | paused | degraded | sealed
stage:          000_INIT      # Current 000–999 stage
risk_level:     low           # low | medium | high | critical
entropy_delta:  0.00          # Confusion delta since last beat (0.0–1.0)
tool_health:    unknown       # unknown | healthy | degraded | failing
loop_count:     0             # Increments each turn
last_action:    none          # Last concrete action taken
next_gate:      observe      # Next governance gate: observe | evidence | reason | critique | route | forge | measure | judge | seal
human_approval_required: false  # true when 888_JUDGE verdict pending
current_task:   (none)       # One-line current task description
blockers:       []            # List of reasons blocking progress
autonomy_level: L1           # Current L0–L5 level (from AUTONOMY.md)
timestamp:      null         # ISO-8601 of last update
```

---

## Status Meanings

| Status | Meaning | Required action |
|--------|---------|-----------------|
| `idle` | No active task | Wait for Arif's instruction |
| `active` | Task in progress | Continue per stage and autonomy level |
| `paused` | Task blocked or awaiting approval | Announce pause, wait for Arif or blocker resolution |
| `degraded` | Tool failure or entropy high | Pause, diagnose, report to Arif |
| `sealed` | Task complete or terminated | Write checkpoint, update MEMORY.md |

---

## Entropy Delta Interpretation

| Range | Meaning | Action |
|-------|---------|--------|
| 0.0–0.2 | Stable | Continue |
| 0.2–0.5 | Slight confusion | Note in last_action, continue |
| 0.5–0.7 | High confusion | Pause, summarize state, ask Arif |
| > 0.7 | Critical confusion | Stop, announce degradation, await instruction |

---

## Field Meanings

| Field | Values | Meaning |
|-------|--------|---------|
| `session_id` | UUID or null | Set at 000_INIT. Null means no session bound. |
| `status` | idle \| active \| paused \| degraded \| sealed | Current system state |
| `stage` | 000–999 | Current loop stage (see AGENTS.md 000–999 loop) |
| `risk_level` | low \| medium \| high \| critical | Consequence exposure |
| `entropy_delta` | float | Confusion delta since last beat; 0.0 = stable, 1.0 = maximally confused |
| `tool_health` | unknown \| healthy \| degraded \| failing | Tool availability |
| `loop_count` | int | Increments each turn; halt if > 20 |
| `last_action` | string | Last concrete action taken |
| `next_gate` | string | Next governance gate required before proceeding |
| `human_approval_required` | bool | Whether 888 JUDGE must act before continuing |
| `current_task` | string | One-line description of active task |
| `blockers` | list | Reasons progress is blocked |
| `autonomy_level` | L0–L5 | Current autonomy level (see AUTONOMY.md) |
| `timestamp` | ISO-8601 | Latest pulse time |

---

## Pause / Escalation / Seal Conditions

| Condition | Action | Announce |
|-----------|--------|---------|
| `risk_level` = critical | Pause immediately | "Risk critical — pausing. {reason}" |
| `loop_count` > 20 | Stop and summarize | "Loop threshold exceeded — summarizing state" |
| `human_approval_required` = true AND (`risk_level` >= high OR `next_gate` = judge) | Escalate to Arif | "Awaiting your verdict. Candidate: {action}" |
| `status` = sealed | Write checkpoint, update MEMORY.md | "Task sealed. Checkpoint written." |
| `entropy_delta` > 0.7 | Stop, do not proceed | "Entropy critical — cannot reliably continue" |

---

## Runtime Notes

_No active task._

*(This section is cleared and rewritten each session)_
