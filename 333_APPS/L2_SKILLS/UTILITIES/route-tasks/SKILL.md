---
name: route-tasks
description: Route tasks via routing.json policy. Use when dispatching, orchestrating, or multi-model routing required.
---

# Route Tasks

Route tasks to models per `routing.json` policy.

## Process

1. Read `routing.json`
2. Match keywords to route
3. Default if no match
4. Log to `routing_ledger.md`
5. Execute with chosen model

## Log Format

```
[timestamp] | TASK: <type> | MODEL: <model> | REASON: <reason>
```

## Rules

- Explain model choice
- Log before execute
- Don't override unless instructed
