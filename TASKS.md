# TASKS.md — Active Work Ledger

**Version:** 2026.05.01
**Purpose:** Tracks active tasks, current objectives, blockers, and next actions.
Reduces re-orientation overhead — Arif and OPENCLAW can pick up without full re-explanation.

---

## Active Tasks

### Task ID: OC-001
**Objective:** Upgrade OPENCLAW runtime governance — replace plain ReAct, add missing files, close audit gaps
**Status:** SEALED — awaiting Arif review
**Autonomy level:** L3

**Completed steps:**
- AGENTS.md: ReAct loop replaced with 000–999 governed loop ✅
- AUTONOMY.md: L0–L5 ladder created ✅
- CHECKPOINT.md: Session continuity file created ✅
- HEARTBEAT.md: Rewritten as live protocol ✅
- LOOP.md: 000–999 operational implementation created ✅
- DECISIONS.md: Sealed decision log created ✅
- TOOLS.md: Populated with local environment notes ✅
- RECOVERY.md: Failure recovery runbook created ✅
- FLOORS.md: F1–F13 standalone reference created ✅
- CLAUDE.md, GEMINI.md, ARIF.md: Archived (stale, conflicting) ✅

**Open steps:**
- None remaining from audit gap list

**Blockers:**
- None

**Next recommended action:** None — OC-001 complete pending Arif review.

---

## Task Lifecycle

| Event | Action |
|-------|--------|
| Task opened | Add to TASKS.md with ID, objective, stage, autonomy level |
| Stage advance | Update current_stage, last_action, entropy_delta |
| Task blocked | Add to blockers[], announce to Arif |
| Task complete | Update status = sealed, write DECISIONS.md entry, clear from active |
| Task voided | Update status = voided, reason, close without sealing |

---

## Task ID Format

`OC-XXX` — OPENCLAW task, numeric increment starting at 001.
Future: may add prefixes for task type (OC-DEV, OC-AUDIT, OC-DEPLOY).

---

## Completed Tasks Archive

*(Moved here when sealed)*

| Task ID | Objective | Sealed date |
|---------|-----------|------------|
| OC-001 | OPENCLAW runtime governance upgrade | 2026-05-01 (in progress — awaiting Arif review) |

---

**Ditempa Bukan Diberi — Forged, not given.**
