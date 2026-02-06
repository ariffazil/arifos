---
name: route-tasks-by-policy
description: Route tasks to specific models using the repository routing.json policy and log each decision to routing_ledger.md. Use when the user asks to dispatch, orchestrate, route, or when multi-model routing is required.
---

# Route Tasks By Policy

## Do this

1. Read `routing.json` from the repository root.
2. Classify the task by matching `keywords` (case-insensitive) for each route.
3. If no match, select `default_model` and set `task_type` to `unknown_default`.
4. Log the decision to `routing_ledger.md` before executing the task.
5. Execute the task with the chosen model(s) and synthesize results if multiple models are used.

Helper script:

`scripts/route_task.py --prompt "<task>" [--log]`

## Log format

Use a single-line entry:

`[timestamp] | TASK: <task_type> | MODEL: <model> | REASON: <reason>`

## Rules

- Explain why the model was chosen by citing the route reason.
- Do not override `routing.json` unless the user explicitly instructs it.
- Log before execution.
- Do not edit `routing.json` or `routing_ledger.md` unless asked.
