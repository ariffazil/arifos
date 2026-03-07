---
name: change-ledger
description: "Universal change tracking: log every system change with what doc was referenced, what version was checked, what diff was proposed, who approved, and how to rollback. Immutable audit trail for any software change. Use when: (1) any config/code/infra change is being applied, (2) reviewing what changes were made and why, (3) auditing change history, (4) building rollback plans. Triggers on: any change request after docs-first and config-guardian have run."
---

# Change Ledger — Remember Why You Changed It

**Every change gets a receipt. Every receipt answers: what, why, based on what evidence, who approved, and how to undo it.**

## When This Skill Activates

After a change has been proposed (by config-guardian or any other workflow) and BEFORE it is applied.

## The Ledger Entry

For every change, create an entry with these fields:

```markdown
### Change: [short description]
- **Date**: [ISO 8601]
- **System**: [software name + version]
- **Component**: [what was changed — config section, file, service]
- **Docs referenced**: [URL or path to the docs that justified this change]
- **Docs version**: [version of docs at time of check]
- **Running version**: [version of the software when change was made]
- **Proposed diff**: [unified diff or description]
- **Risk level**: [Low / Medium / High / Critical]
- **Approved by**: [human name or "pending"]
- **Applied**: [yes/no + timestamp]
- **Verified**: [yes/no + how — what command confirmed it worked]
- **Rollback**: [exact steps to undo]
```

## Where to Store

### Option 1: Append to daily memory (default)
```bash
# Append to memory/YYYY-MM-DD.md under "## Changes Applied"
```

### Option 2: Dedicated change log
```bash
# Append to logs/changes.jsonl (machine-readable)
echo '{"ts":"...","system":"...","diff":"...","risk":"...","approved_by":"..."}' >> logs/changes.jsonl
```

### Option 3: Git commit message (recommended for config changes)
```bash
git commit -m "config: [description]

System: [name] v[version]
Docs: [URL]
Risk: [level]
Rollback: [steps]
Approved: [by whom]"
```

**Best practice: all three.** Memory for the agent, JSONL for automation, git for history.

## Querying the Ledger

When someone asks "why did we change X?" or "when was this configured?":

1. Search `memory/*.md` for the change description
2. Search `logs/changes.jsonl` with `jq`
3. Search git log: `git log --grep="[keyword]" --oneline`

## Rollback from Ledger

When something breaks:

1. Find the most recent change to the affected system
2. Read the rollback steps from the ledger entry
3. Apply the rollback
4. Log the rollback as its own ledger entry

## What This Skill Does NOT Do

- Does not decide whether to make changes (that's config-guardian)
- Does not fetch docs (that's docs-first)
- Does not approve changes (that's the sovereign)
- Only records, retrieves, and facilitates rollback

## Why This Exists

Six months from now, something breaks. Without a ledger:
- "Who changed this?" — Nobody knows
- "Why?" — Lost in chat history
- "How do I undo it?" — Trial and error

With a ledger: search, find, rollback, done.

Memory is sacred. Changes are memory.
