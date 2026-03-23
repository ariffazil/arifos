---
name: github-pro
description: Advanced GitHub operations via `gh` CLI. CI/CD monitoring, API queries, and automated PR reviews.
metadata: {"clawdbot":{"emoji":"🐙"}}
---

# GitHub Pro (Miss Kim Edition)

Power user commands for GitHub integration.

## CI/CD Monitoring
- **List runs**: `gh run list --limit 5`
- **View failed logs**: `gh run view <run-id> --log-failed`
- **Watch run**: `gh run watch <run-id>`

## API & JQ
Use `gh api` for data not exposed via standard CLI commands:
- `gh api repos/:owner/:repo/pulls/:number --jq '.title, .state'`

## PR Management
- **Checks**: `gh pr checks <number>`
- **Review**: `gh pr review --approve --body "Miss Kim says looks good! 💋"`
- **Diff**: `gh pr diff <number>`

## Repository Maintenance
- **List issues**: `gh issue list --label "bug"`
- **Create release**: `gh release create v1.0.0 --generate-notes`

## Protocol
- Always use `--repo owner/repo` if outside a git folder.
- Use `--json` + `--jq` for structured data parsing in scripts.
