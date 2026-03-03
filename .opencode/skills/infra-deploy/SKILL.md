---
name: infra-deploy
description: arifOS VPS infra deployment skill with constitutional hold gates.
---

Scope:
- /srv/arifOS deployment stack and service definitions.

Rules:
- Do not change SSH or firewall without explicit hold approval.
- Treat destructive DB migrations and volume deletions as HOLD actions.
- Always verify docker health and endpoint checks after deploy.
