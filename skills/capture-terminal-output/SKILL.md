---
name: capture-terminal-output
description: Format terminal output for easy copy-paste with clean boxes, minimal blocks, or code fences when requested. Use when the user asks to copy, paste, capture, or format terminal output.
---

# Capture Terminal Output

## Trigger when

- User says "copy this output" or "paste this"
- User says "capture terminal" or "format for copy"
- User shares terminal output and asks for a clean, copyable format

## Format options

- Default: clean box with borders
- Terminal block: double-line border
- Minimal: plain lines for quick copy
- Code fence: only if the user asks for code or syntax highlighting

Helper script:

`scripts/format_output.py --style box|block|minimal|code [--line-numbers]`

## Examples

Clean box (default):

```
┌─────────────────────────────────────────┐
│  $ python script.py                     │
│  Hello World                            │
│  Result: 42                             │
└─────────────────────────────────────────┘
```

Terminal block:

```
═══════════════════════════════════════════
  $ git status
  On branch main
  nothing to commit, working tree clean
═══════════════════════════════════════════
```

Minimal:

```
$ echo "Quick output"
Quick output
```

## Rules

- Keep output copy-paste friendly.
- Avoid markdown unless requested.
- Add line numbers only if requested.
