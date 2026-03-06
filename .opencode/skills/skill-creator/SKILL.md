---
name: skill-creator
description: Create or improve OpenCode skills with arifOS governance, trigger optimization, and measurable eval loops.
---

# Skill Creator (arifOS)

Use this skill when a user asks to create a new skill, refactor an existing skill, benchmark skill quality, or improve trigger reliability.

## Mission

Build skills that are:

- easy to trigger at the right time,
- safe for infrastructure and code operations,
- testable with repeatable evaluation steps,
- concise enough to avoid instruction bloat.

## arifOS Constraints

- Primary workspace: `/srv/arifOS`
- Do not create duplicate source paths.
- Do not expose secrets in skill examples.
- Mark irreversible operations as `888_HOLD`.

## Core Loop

1. Capture intent and trigger contexts.
2. Draft or revise `SKILL.md`.
3. Create 2-3 realistic eval prompts.
4. Run with-skill and baseline comparisons (when possible).
5. Score results (quality + cost + latency).
6. Revise skill and repeat until stable.

## Interview Checklist

- What exact tasks should trigger this skill?
- What output format is required?
- What should never happen?
- Which tools are allowed, ask-only, or denied?
- What is success for this skill after 1 run?

## Skill Design Rules

- Keep frontmatter description explicit and trigger-oriented.
- Keep body focused on workflow, not theory dumps.
- Explain why steps matter, do not rely on rigid shouting language.
- Move bulky references to separate files when needed.
- Include a minimal verification block with runnable commands.

## Evaluation Model

For each iteration, record:

- Trigger accuracy (did skill activate when needed?)
- Output correctness (did it complete the task?)
- Safety behavior (did it enforce hold gates?)
- Efficiency (time/tokens if available)

Use this scoring template:

| Metric | Weight | Score (0-5) | Weighted |
|---|---:|---:|---:|
| Trigger accuracy | 0.30 |  |  |
| Output quality | 0.35 |  |  |
| Safety/governance | 0.25 |  |  |
| Efficiency | 0.10 |  |  |

Total score = sum(weighted).

## Inspector Gate (for MCP-related skills)

If the skill builds MCP servers, Inspector is mandatory before release:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

Release cannot proceed if Inspector gate fails.

## Trigger Optimization Pass

After functional quality is good:

1. Generate mixed should-trigger and should-not-trigger prompts.
2. Test trigger behavior across variants.
3. Rewrite description for better discrimination.
4. Re-test and keep the best description by held-out performance.

## Output Contract

Always return:

- Current State
- Action Taken
- `SEAL: <percent>% -> <next action>`
- Next Command

## Done Criteria

- Skill behavior stable across test prompts.
- Trigger false positives reduced.
- Safety gates preserved.
- Clear handoff docs included.
