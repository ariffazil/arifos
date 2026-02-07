# WORKFLOW_REPO_STEWARD.md
STATUS: APPROVED
OWNER: Architect
ROLE_CHAIN: Architect -> Auditor -> Engineer

## Purpose
Maintain code hygiene and prevent entropy accumulation in arifOS repositories by summarizing activity, suggesting fixes, and ensuring dependencies are secure.

## Inputs
- **GitHub (`gh` CLI):** Issues, Pull Requests, Security Alerts (Dependabot).
- **Filesystem (`git` MCP):** Local repo status (dirty/clean), stale branches.
- **Healthcheck:** CVE scans for current stack (Node, Ubuntu).

## Outputs
- **Channel:** Telegram (@AGI_ASI_bot)
- **Format:** Weekly summary message:
  - 🛠️ **Repo Health** (Open Issues, Stale PRs)
  - 🔒 **Security** (CVEs, Dependabot alerts)
  - 🧹 **Cleanup** (Suggest deleting merged branches)
  - 📈 **Velocity** (Commits/week)

## Tools (by role)
- **Architect:** `sequential-thinking` (workflow logic), `filesystem`.
- **Engineer:** `github` (read-only issues/PRs), `git` (local status), `healthcheck`, `cron`.
- **Auditor:** `filesystem` (spec review), `arifOS-judge`.

## Schedule
- **Time:** 09:00 MYT (Every Monday)
- **Cron Expression:** `0 9 * * 1`
- **Agent:** `repo-steward` (or `main`)
- **Session:** Isolated

## Engineer Implementation
- **Cron ID:** `repo-steward-v1`
- **Command:** `openclaw cron add --name "repo-steward" --schedule "0 9 * * 1" --payload "systemEvent: Generate and send the Repo Steward summary as per WORKFLOWS/WORKFLOW_REPO_STEWARD.md."`

## Floors / Constraints
- **F1 Amanah:** Read-only analysis; no auto-merging PRs or closing issues without approval.
- **F2 Truth:** Cite specific issue numbers/PR links. No hallucinated bugs.
- **F7 Humility:** Suggest fixes as "Estimate Only" unless verified by tests.
- **F9 Anti-Hantu:** Report as a tool/bot, not a colleague.

## Audit Log
- **2026-02-07:** STATUS set to DRAFT by Architect.
- **2026-02-07:** STATUS set to APPROVED by Auditor (Compliance: F1/F2/F7/F9 verified).
