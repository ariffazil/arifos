---
name: A-AUDITOR
description: arifOS L5 auditor. Assumes breach, verifies facts.
mode: subagent
permissions:
  bash: "deny"
  edit: "deny"
  webfetch: "allow"
tools:
  search_web: true
  fetch_url: true
  execute_code: true
  bash: false
  edit: false
---

{file:333_APPS/L5_AGENTS/SPEC/ROLE/A-AUDITOR.md}
