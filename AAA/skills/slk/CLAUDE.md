# CLAUDE.md — Quick Reference for Claude Code / Codex

## What is slk?

Slack CLI for macOS. Auto-auth from Slack desktop app (session cookies, no bot install). Zero dependencies.

## Key Files

- `src/commands.js` — All command logic. Add new commands here.
- `src/api.js` — `slackApi()` and `slackPaginate()`. Add POST endpoints to `writeMethods` array.
- `src/auth.js` — Keychain + LevelDB credential extraction. Rarely needs changes.
- `src/drafts.js` — Draft commands (create/list/drop).
- `bin/slk.js` — CLI entry point. Command routing + help text.

## Adding a Feature

1. Add function in `src/commands.js` (export async)
2. If new API needs POST → add to `writeMethods` in `src/api.js`
3. Add case + alias in `bin/slk.js` switch block
4. Add to HELP string in `bin/slk.js`
5. Update `README.md` (commands table, examples, flags if any)
6. Update `SKILL.md` (commands list)
7. `npm version patch --no-git-tag-version`
8. `git add -A && git commit -m "feat: ..." && git push`
9. `echo "//registry.npmjs.org/:_authToken=${NPM_PUBLISH_TOKEN}" > .npmrc && npm publish && rm .npmrc`
10. `cp SKILL.md ~/moltbot/skills/slk/SKILL.md`

## Testing

```bash
node bin/slk.js <command>   # Direct run
slk <command>               # If globally linked
```

## Patterns

- Use `getUsers()` for user ID → name resolution (cached)
- Use `resolveChannel(nameOrId)` for channel name/ID handling
- Use `formatTs(ts)` for Slack timestamp → human date
- Errors: `console.error()` + `process.exit(1)`
- Output: `console.log()` with emoji prefixes

## Auth

Session-based (`xoxc-` token + `xoxd-` cookie). Auto-extracted from Slack desktop app on macOS.
Cache: `~/.local/slk/token-cache.json`. Delete to force re-extract.

## npm Publish Token

`NPM_PUBLISH_TOKEN` env var from `~/.local/keys/env.sh`. Use `.npmrc` trick (create before publish, delete after).
