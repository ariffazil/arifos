# slk 💬 — Slack CLI for macOS, so your agents can read and send messages

`slk` is a Slack command-line tool for macOS that auto-extracts auth from the Slack desktop app. Read channels, send messages, search, manage drafts, track unreads, and view pins — no tokens, no OAuth, no config.

Built for AI agents and terminal workflows. Zero dependencies. Zero setup.

> **Not affiliated with Slack.** This is an independent Slack CLI built for personal productivity and agent automation. It uses session credentials from the Slack desktop app and works only on macOS. Use at your own discretion.

## Install

```bash
npm install -g slkcli
```

One-shot (no install):

```bash
npx slkcli auth
```

**Requirements:** macOS, Slack desktop app (installed and logged in), Node.js 18+.

## Agent Skill

Add to your AI agent (Claude Code, Codex, Moltbot, etc.):

```bash
# ClawdHub
clawdhub install slack-personal

# skills.sh
npx skills add therohitdas/slkcli
```

Browse on [ClawdHub](https://www.clawhub.ai/therohitdas/slack-personal).

## Quickstart

```bash
# Verify your session works
slk auth

# List channels
slk channels

# Read the last 20 messages in a channel
slk read general
slk read C08A8AQ2AFP        # by channel ID

# Send a message
slk send general "Hello from slk"

# Search across the workspace
slk search "deployment failed"

# Check what's unread
slk unread

# See starred items and VIP users
slk starred

# See saved for later items
slk saved

# See pinned messages in a channel
slk pins general

# Read a thread
slk thread general 1234567890.123456

# React to a message
slk react general 1234567890.123456 thumbsup
```

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `slk auth` | | Test authentication, show user/team info |
| `slk channels` | `ch` | List all channels with member counts |
| `slk dms` | `dm` | List DM conversations with IDs |
| `slk users` | `u` | List workspace users with statuses |
| `slk read <channel> [count]` | `r` | Read recent messages (default: 20) |
| `slk send <channel> <message>` | `s` | Send a message to a channel |
| `slk search <query> [count]` | | Search messages across the workspace |
| `slk thread <channel> <ts> [count]` | `t` | Read thread replies (default: 50) |
| `slk react <channel> <ts> <emoji>` | | Add an emoji reaction to a message |
| `slk activity` | `a` | Show all channel activity with unread/mention counts |
| `slk unread` | `ur` | Show only channels with unreads (excludes muted) |
| `slk starred` | `star` | Show VIP users and starred items |
| `slk saved [count]` | `sv` | Show saved for later items (active by default, `--all` includes completed) |
| `slk pins <channel>` | `pin` | Show pinned items in a channel |

### Flags

| Flag | Description |
|------|-------------|
| `--ts` | Show raw Slack timestamps (useful for getting ts to read threads) |
| `--threads` | Auto-expand all threads when reading messages |
| `--from YYYY-MM-DD` | Read messages from this date onwards |
| `--to YYYY-MM-DD` | Read messages until this date |
| `--no-emoji` | Disable emoji in output (or set `NO_EMOJI=1`) |
| `--all` | Include completed items in `slk saved` |

```bash
# Get timestamps to use with thread command
slk read general 10 --ts
# Output: [1/30/2026, 11:41:19 AM ts:1769753479.788949] User [3 replies]:

# Then read that thread
slk thread general 1769753479.788949
```

### Drafts

Drafts sync to Slack — they appear in the Slack editor UI.

| Command | Description |
|---------|-------------|
| `slk draft <channel> <message>` | Draft a channel message |
| `slk draft thread <channel> <ts> <message>` | Draft a thread reply |
| `slk draft user <user_id> <message>` | Draft a DM |
| `slk drafts` | List all active drafts |
| `slk draft drop <draft_id>` | Delete a draft |

### Channel resolution

Channels can be specified by **name** or **ID** in any command:

```bash
slk read general           # by name
slk read ai-coding         # by name
slk read C08A8AQ2AFP       # by ID
```

### DMs

Read, send, and react to DMs using `@username` or user ID:

```bash
# List all DM conversations
slk dms

# Read DMs by username
slk read @andrej 50
slk read @nikhil 100 --threads    # auto-expand threads

# Read DMs with date range
slk read @andrej 100 --from 2026-02-01 --to 2026-02-07 --threads

# Send DM
slk send @andrej "hey, check this out"

# React to DM message
slk react @andrej 1769753479.788949 fire

# By user ID (U...)
slk read U07RQTFCLUC 50
```

## Authentication

`slk` uses the credentials already stored by the Slack desktop app. No OAuth flows, no manual token management.

### Keychain access prompt

On first run, macOS will show a Keychain dialog asking whether to allow access to "Slack Safe Storage":

- **Allow** — grants one-time access. You'll be prompted again next time slk needs to decrypt the cookie.
- **Always Allow** — grants permanent access for this binary. No future prompts.
- **Deny** — blocks access. slk cannot authenticate.

> **Caution:** Choosing "Always Allow" means any process running as your user that invokes the `slk` binary (or the `security` command targeting "Slack Safe Storage") can read the encryption key without a prompt. This is convenient but reduces the security boundary — any code running in your terminal (scripts, agents, other CLI tools) could trigger credential extraction silently. On a personal machine this is a reasonable trade-off. On a shared or managed machine, prefer "Allow" so you get prompted each time and maintain visibility into access.

### How it works

1. **Cookie decryption** — Reads the encrypted `d` cookie from Slack's SQLite cookie store (`Cookies` file). Decrypts it using the "Slack Safe Storage" key from the macOS Keychain via PBKDF2 + AES-128-CBC. Supports both direct-download and Mac App Store keychain account names.

2. **Token extraction** — Scans Slack's LevelDB storage (`Local Storage/leveldb/`) for `xoxc-` session tokens. Uses both direct regex scanning and a Python fallback for Snappy-compressed entries. The Slack data directory is auto-detected (direct download or App Store sandbox).

3. **Validation** — Tests each candidate token against `auth.test` with the decrypted cookie. The first valid pair is used.

4. **Auto-refresh** — On `invalid_auth`, credentials are re-extracted and the request is retried once automatically.

### Token caching

Validated tokens are cached to avoid re-extracting on every invocation:

| | |
|---|---|
| **Cache file** | `~/.local/slk/token-cache.json` |
| **Format** | `{ "token": "xoxc-...", "ts": 1706000000000 }` |
| **Behavior** | Load cache → validate with Slack API → use if valid, otherwise re-extract from LevelDB |
| **In-memory** | Within a single process, credentials are cached in memory after first load |

### Credential resolution order

```
1. In-memory cache (same process)
2. Disk cache (~/.local/slk/token-cache.json) → validate → use if ok
3. Fresh extraction from Slack desktop app → validate → cache → use
```

### What it reads from your system

| Data | Source | Purpose |
|------|--------|---------|
| Keychain password | `security find-generic-password -s "Slack Safe Storage"` | Derive AES key for cookie decryption |
| Encrypted cookie | `<slack-data-dir>/Cookies` (SQLite) | Decrypt the `d` session cookie (`xoxd-`) |
| Session token | `<slack-data-dir>/Local Storage/leveldb/` | Extract `xoxc-` token |

## Agent usage patterns

`slk` is designed to be used by AI agents. Common patterns:

```bash
# Check auth before doing anything
slk auth

# Get channel list, find the right one
slk channels

# Read recent context from a channel
slk read engineering 50

# Search for something specific
slk search "PR review needed"

# Check what needs attention
slk unread

# See pinned context in a channel
slk pins engineering

# Send a message
slk send engineering "Build passed on main"

# Read a thread for full context
slk thread engineering 1706000000.000000

# Draft a message for human review (appears in Slack UI)
slk draft engineering "Here's the summary of today's standup..."
```

**Exit codes:** `0` on success, `1` on error. Errors are printed to stderr.

## How it was installed

The `bin` field in `package.json` maps `slk` to `./bin/slk.js`:

```json
{ "bin": { "slk": "./bin/slk.js" } }
```

Running `npm install -g` creates a symlink in your PATH:

```
/opt/homebrew/bin/slk -> ../lib/node_modules/slkcli/bin/slk.js
```

## Development

```bash
git clone https://github.com/therohitdas/slk.git
cd slk
node bin/slk.js auth       # run directly
npm link                   # symlink globally for development
```

## Notes

- **macOS only** — uses Keychain and Electron storage paths specific to macOS.
- **Both Slack variants supported** — works with the direct download (`~/Library/Application Support/Slack/`) and the Mac App Store version (`~/Library/Containers/com.tinyspeck.slackmacgap/.../Slack/`). The correct path is auto-detected at runtime.
- **Slack desktop app required** — must be installed and logged in. The app does not need to be running for cached tokens.
- **Zero dependencies** — uses only Node.js built-in modules (`crypto`, `fs`, `child_process`, `fetch`).
- **Session-based** — uses `xoxc-` tokens (user session), not bot tokens. This means you act as yourself.
- **Mute-aware** — `activity` and `unread` commands respect your mute settings.
