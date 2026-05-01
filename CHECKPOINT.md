# CHECKPOINT.md — Session Continuity & Recovery

**Version:** 2026.05.01
**Replaces:** None — new file

---

## Purpose

OPENCLAW wakes up stateless. CHECKPOINT.md stores the minimum state needed to
reconstruct where the agent was, what it was doing, and what it decided.

Without this, the agent cannot reliably resume a task, may hallucinate continuity,
and has no rollback anchor when something goes wrong.

---

## Checkpoint Entry Schema

Every checkpoint is a JSON-like block at the top of `MEMORY.md` or a standalone
`CHECKPOINT.md` file:

```
## CHECKPOINT {session_id} — {ISO_timestamp}

session_id:     {uuid}
parent_session: {uuid or null}
stage:          {000–999}
last_action:    {description of last concrete action}
entropy_delta:  {float — change in confusion since last beat}
status:         {idle|active|paused|degraded|sealed}
risk_level:     {low|medium|high|critical}
autonomy_level: {L0–L5}
current_task:   {one-line description}
blockers:      [{reason}, ...]
tool_health:    {unknown|healthy|degraded|failing}
loop_count:     {int}
next_gate:      {next governance gate — e.g. 888_JUDGE, FORGE, SEAL}
human_approval_required: {bool}
verdict_pending: {candidate action awaiting verdict or null}

[Optional: task-specific fields]
```

---

## When to Write a Checkpoint

| Event | Checkpoint required? |
|-------|---------------------|
| Session start (wake) | Yes — read checkpoint to reconstruct state |
| Before major action | Update HEARTBEAT.md fields |
| After completing a stage (111, 222, 333, 444, 555, 666, 777, 888) | Yes |
| When task is paused | Yes |
| When human approval is required | Yes |
| Session end (sleep) | Yes — write final checkpoint |
| After 888 JUDGE verdict | Yes — record verdict and outcome |

---

## How to Recover from a Checkpoint

1. **Read `CHECKPOINT.md`** for session_id, stage, last_action
2. **Read `MEMORY.md`** for sealed facts, decision history, lessons
3. **Read `HEARTBEAT.md`** for current runtime state
4. **Announce recovery:** "Recovering session {id}, was at stage {stage}, last action was {last_action}"
5. **Confirm task:** "Continuing task: {current_task}. blockers: {blockers}. Awaiting your instruction."
6. **Resume** at the `next_gate` from the checkpoint

---

## Rollback Rules

If the current task is degraded or the agent detects it is lost:

1. **Acknowledge:** "Session state unclear — initiating rollback"
2. **Read last checkpoint** with status=active or status=paused
3. **Re-run from:** `next_gate` from that checkpoint
4. **Do not replay** the action that caused degradation
5. **Escalate if:** loop_count > 20, entropy_delta > 0.7, or status = sealed

---

## Checkpoint vs HEARTBEAT.md

| File | Purpose | Updates |
|------|---------|---------|
| HEARTBEAT.md | Live runtime pulse — aliveness signal | Every action |
| CHECKPOINT.md | Durable state anchor — session continuity | Stage transitions, session boundaries |
| MEMORY.md | Selective persistence — sealed facts and lessons | After SEAL verdicts, task completion |

HEARTBEAT is volatile. CHECKPOINT is the recovery anchor.
Both are read on session start. Neither is ignored.

---

## Anti-Hallucination Rule

The checkpoint is the **only** proof of continuity. If no checkpoint exists for
the current session, OPENCLAW must:
1. Announce "No checkpoint found — starting fresh"
2. Initialize from SOUL.md baseline (stage 000, status idle)
3. Not assume prior context unless confirmed by Arif

---

**Ditempa Bukan Diberi — Forged, not given.**
