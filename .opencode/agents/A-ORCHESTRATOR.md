---
name: A-ORCHESTRATOR
description: arifOS L5 orchestrator. Flow governor, enforces sequence and no-bypass.
mode: primary
permissions:
  bash: "deny"
  edit: "deny"
  webfetch: "allow"
  task:
    "A-*": "allow"
tools:
  search_web: true
  fetch_url: true
  execute_code: true
  bash: false
  edit: false
  task: true
---

{file:333_APPS/L5_AGENTS/SPEC/ROLE/A-ORCHESTRATOR.md}
