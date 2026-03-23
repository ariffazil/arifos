# AGENTS.md — slk Development Guide

This is the full loop for working on slk. Follow this every time you add, change, or fix something.

## Project Structure

```
slk/
├── bin/slk.js          # CLI entry point — command routing, help text, aliases
├── src/
│   ├── api.js          # Slack API wrapper — fetch, auth headers, pagination
│   ├── auth.js         # Credential extraction — Keychain, LevelDB, token cache
│   ├── commands.js     # All command implementations (read, send, saved, etc.)
│   └── drafts.js       # Draft-specific commands (create, list, drop)
├── package.json        # Version, bin mapping, metadata
├── README.md           # Full documentation for users
├── SKILL.md            # Agent skill file (used by Moltbot/ClawdBot)
├── AGENTS.md           # This file — dev guide for AI agents
└── CLAUDE.md           # Quick reference for Claude Code / Codex
```

## The Full Loop: Adding a New Feature

### 1. Write the Code

Add your command implementation in `src/commands.js`:
- Export an async function
- Use `slackApi()` or `slackPaginate()` from `api.js`
- Use existing helpers: `getUsers()`, `resolveChannel()`, `formatTs()`, `userName()`
- Follow the existing pattern: fetch data → format → console.log output
- Handle errors with `console.error` + `process.exit(1)`

If your new API endpoint needs POST (most Slack endpoints do), add it to the `writeMethods` array in `src/api.js`.

### 2. Wire Up the CLI

In `bin/slk.js`:
- Add the command to the `HELP` string (with alias and description)
- Add a `case` in the `switch` block
- Follow the pattern: validate args → call command function → handle aliases

### 3. Test It

```bash
# Run directly (no install needed)
node bin/slk.js <your-command>

# Or if globally linked:
slk <your-command>

# Test edge cases:
# - No args (should show usage)
# - Invalid channel
# - Auth expired (should auto-refresh)
```

### 4. Update Documentation

**All three must be updated:**

1. **README.md** — Add to:
   - Commands table
   - Quickstart examples (if user-facing)
   - Flags table (if new flags)
   - Agent usage patterns (if relevant)

2. **SKILL.md** — Add to the commands list under the appropriate section (Read/Activity/Write/Drafts)

3. **bin/slk.js HELP** — Already done in step 2, but double-check alignment with README

### 5. Bump Version

```bash
npm version patch --no-git-tag-version   # 0.1.2 → 0.1.3 (bugfix/small feature)
npm version minor --no-git-tag-version   # 0.1.3 → 0.2.0 (new feature)
npm version major --no-git-tag-version   # 0.2.0 → 1.0.0 (breaking change)
```

Use `patch` for most changes. Use `minor` for significant new features.

### 6. Git Commit & Push

```bash
git add -A
git commit -m "feat: short description of what changed

- Detail 1
- Detail 2
- Bumped to x.y.z"
git push
```

Commit message prefixes:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that doesn't add/fix

### 7. Publish to npm

```bash
# Create .npmrc with publish token
echo "//registry.npmjs.org/:_authToken=${NPM_PUBLISH_TOKEN}" > .npmrc
npm publish
rm .npmrc   # Clean up — don't commit the token!
```

The `NPM_PUBLISH_TOKEN` env var is set in `~/.local/keys/env.sh`.

### 8. Update Local Moltbot Skill

```bash
cp SKILL.md ~/moltbot/skills/slk/SKILL.md
```

This ensures Moltbot's local skill stays in sync with the published version.

## Quick Reference: One-liner Full Deploy

```bash
cd ~/Lab/slk
# ... make changes ...
npm version patch --no-git-tag-version
git add -A && git commit -m "feat: description" && git push
echo "//registry.npmjs.org/:_authToken=${NPM_PUBLISH_TOKEN}" > .npmrc && npm publish && rm .npmrc
cp SKILL.md ~/moltbot/skills/slk/SKILL.md
```

## API Notes

- **Undocumented endpoints:** Slack has many internal APIs not in public docs. Use POST method. Examples: `saved.list`, `client.counts`, `users.prefs.get`, `drafts.create`.
- **Auth:** All requests need both `Authorization: Bearer xoxc-...` header AND `Cookie: d=xoxd-...` cookie. The `slackApi()` wrapper handles this.
- **Pagination:** Use `slackPaginate()` for list endpoints that support cursor-based pagination.
- **Channel resolution:** `resolveChannel()` accepts names or IDs. Always use it for user-facing commands.

## Testing Auth

If auth breaks:
```bash
rm ~/.local/slk/token-cache.json
slk auth
```
Make sure Slack desktop app is running.
