# WORKFLOW_SUBUH_BRIEF.md
STATUS: APPROVED
OWNER: Architect
ROLE_CHAIN: Architect -> Auditor -> Engineer

## Purpose
Compress morning informational entropy (email + news + weather) into a single, high-signal brief at 06:30 MYT, preserving Peace² while respecting F1/F2/F7.

## Inputs
- **Email (himalaya):** Unread messages from VIP senders or with high-priority labels.
- **Web (brave_search):**
  - Tech news (AI governance, OpenClaw updates).
  - Geopolitics (ASEAN/Malaysia focus).
- **Weather:** Seri Kembangan daily summary.
- **Context:** Today’s date, day-of-week, upcoming calendar events (if available).

## Outputs
- **Channel:** Telegram (@AGI_ASI_bot)
- **Format:** Single message with:
  - 🌅 **Morning Snapshot** (Weather + Date)
  - 🚨 **Fires** (Urgent emails/alerts)
  - 🏆 **Wins** (Completed cron jobs/PRs)
  - 🌍 **Watchlist** (Key news headlines)
  - 🧘 **Focus** (Suggested deep work block)

## Tools (by role)
- **Architect:** `sequential-thinking`, `brave_search` (query design), `filesystem`, `git`.
- **Engineer:** `himalaya` (read-only), `brave_search`, `weather`, `cron`, `telegram`.
- **Auditor:** `filesystem` (spec review), `arifOS-judge`.

## Schedule
- **Time:** 06:30 MYT (Daily)
- **Cron Expression:** `30 6 * * *`
- **Agent:** `executive-brief` (or `main` if single-agent)
- **Session:** Isolated

## Engineer Implementation
- **Cron ID:** `subuh-brief-v1`
- **Command:** `openclaw cron add --name "subuh-brief" --schedule "30 6 * * *" --payload "systemEvent: Generate and send the Subuh Briefing as per WORKFLOWS/WORKFLOW_SUBUH_BRIEF.md."`

## Floors / Constraints
- **F1 Amanah:** Read-only on email; no sending, deleting, or moving messages.
- **F2 Truth:** Mark any speculative analysis as “Estimate Only”.
- **F7 Humility:** Limit to one screen of content; link out instead of over-summarizing.
- **F9 Anti-Hantu:** No anthropomorphic claims; state clearly “this is an automated brief”.

## Audit Log
- **2026-02-07:** STATUS set to DRAFT by Architect.
- **2026-02-07:** STATUS set to APPROVED by Auditor (Compliance: F1/F2/F7/F9 verified).
