---
name: docs-first
description: "Universal pre-action skill: before ANY config change, code fix, or system edit, fetch and read the latest official documentation and release notes for the target software. Blocks stale-knowledge errors. Use BEFORE any change to any system — OpenClaw, Docker, Nginx, PostgreSQL, Python packages, or any software. Triggers on: 'fix', 'change', 'update', 'configure', 'edit config', 'upgrade', 'install', 'migrate', or any modification request."
---

# Docs-First — Read Before You Write

**Universal law: Never change what you haven't read the manual for.**

An agent's training data is frozen. Software updates daily. Acting on stale knowledge with full confidence is the most dangerous failure mode.

## When This Skill Activates

ANY request to change, fix, update, configure, or edit ANY system. No exceptions.

## The Workflow

### Step 1: Identify the Target

What software or system is being changed?
- Name (e.g. "OpenClaw", "PostgreSQL", "Docker", "Nginx")
- Component (e.g. "cron config", "auth settings", "SSL cert")

### Step 2: Check Running Version

Run the version command for the target system:

```bash
# Examples — adapt to the actual system
openclaw status              # OpenClaw
docker --version             # Docker
nginx -v                     # Nginx
psql --version               # PostgreSQL
python --version             # Python
node --version               # Node.js
pip show <package>           # Python package
npm list <package>           # Node package
cat /etc/os-release          # OS
```

Record the exact version string. This is ground truth.

### Step 3: Fetch Latest Docs

Use `web_fetch` or `web_search` to get the **current** official documentation:

```
Docs sources (in priority order):
1. Local docs (bundled with the software, e.g. /app/docs/)
2. Official docs site (e.g. docs.openclaw.ai, docs.docker.com)
3. GitHub repo README / CHANGELOG / releases page
4. Release notes for the specific version
```

**Always check the changelog/release notes between the installed version and latest.**

### Step 4: Compare Knowledge

Before proceeding, explicitly state:
- **Installed version**: what's actually running
- **Docs version**: what version the fetched docs describe
- **Knowledge version**: what version your training data covers
- **Delta**: any differences, breaking changes, deprecations, or new features

If there's a mismatch:
- Flag it clearly: "⚠️ My knowledge may be stale for this version"
- Use the fetched docs as the source of truth, not cached knowledge
- Cite the specific doc section for any config guidance

### Step 5: Proceed or Halt

| Situation | Action |
|---|---|
| Docs match knowledge | Proceed with change |
| Docs newer than knowledge | Proceed, but cite fetched docs only |
| Can't fetch docs | HALT — tell human "I can't verify my knowledge is current" |
| Breaking changes between versions | HALT — show breaking changes, ask human to decide |

## Output: Current Truth Sheet

For every docs-first check, produce a brief summary:

```markdown
## Current Truth — [Software Name]
- **Running**: v2026.3.2
- **Docs checked**: docs.example.com (fetched [date])
- **Breaking changes since last known**: [none / list]
- **Relevant doc section**: [URL or path]
- **Confidence**: HIGH (docs match) / MEDIUM (minor gaps) / LOW (can't verify)
```

## What This Skill Does NOT Do

- Does not make changes (that's config-guardian or the agent's normal workflow)
- Does not replace domain expertise (just grounds it in current docs)
- Does not block urgent hotfixes (but flags the risk of acting without docs)

## Why This Exists

The Stale Knowledge Paradox: an agent trained on v2 docs confidently misconfigures v3.
The fix is simple — read the manual first. Every time. No exceptions.

Like checking the well log before interpreting the seismic line.
