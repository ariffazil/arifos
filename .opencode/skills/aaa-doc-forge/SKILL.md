---
name: aaa-doc-forge
description: Forge mission-critical documentation with AAA governance, mandatory contrast analysis, Godel-lock contradiction audit, and Eureka extraction. Trigger for specs, RFCs, proposals, architecture decisions, runbooks, migration plans, and any high-stakes doc rewrite.
---

# AAA Doc Forge

Single unified documentation skill for arifOS.

## Constitutional Intent

- F2 Truth: no unsupported claims.
- F4 Clarity: reduce entropy in every revision.
- F1 Amanah: mark irreversible recommendations as `888_HOLD`.
- F11/F13: human ratification remains final for high-stakes decisions.

## Trigger Scope

Use this skill whenever user asks to:

- draft or revise technical/business docs,
- compare architecture or strategy options,
- produce decision records,
- audit a document for contradictions/gaps,
- prepare final publish-ready documentation.

## Required Workflow

### 1) Context Anchor

Collect only what is needed:

1. doc type
2. audience
3. target decision/outcome
4. constraints (time/cost/risk/security)
5. required format/template

### 2) Structure Forge

Build skeleton first:

- Purpose
- Current Reality
- Options
- Decision Criteria
- Recommended Path
- Risks and Mitigations
- Rollout and Verification

### 3) Contrast Analysis (Mandatory)

Return table with at least 2 options (prefer 3):

| Option | Benefits | Risks | Cost/Complexity | Reversibility | Fit |
|---|---|---|---|---|---|

### 4) Godel-Lock Audit (Mandatory)

Check for:

1. internal contradiction
2. hidden assumptions
3. unsupported claims
4. scope leakage

Audit output:

- `LOCK_PASS` = no critical contradiction.
- `LOCK_WARN` = contradictions/gaps still present.

### 5) Eureka Extraction (Mandatory)

Extract 1-3 non-obvious insights:

- insight
- why it matters now
- action that changes because of it

### 6) Reader Reality Test

Simulate fresh-reader understanding:

- likely misunderstandings
- unanswered questions
- ambiguous sections to tighten

Revise until decision-ready.

## Output Contract (Always)

1. Current State
2. Draft/Revision
3. Contrast Analysis
4. Godel-Lock Audit
5. Eureka Insights
6. `SEAL: <percent>% -> <next action>`
7. Next Command

## Guardrails

- No secret output.
- No fake certainty.
- No verbose filler.
- No bypass of `888_HOLD` for irreversible posture changes.

## Minimal Verification

```bash
cd /srv/arifOS
git status -sb
```
