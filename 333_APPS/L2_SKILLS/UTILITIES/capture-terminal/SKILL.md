---
name: capture-terminal
description: Format terminal output for copy-paste. Use when user asks to copy, paste, capture, or format terminal output.
---

# Capture Terminal

Format terminal output for easy copy-paste.

## Styles

| Style | Use | Appearance |
|-------|-----|------------|
| box | Default | `┌─────┐` bordered |
| block | Emphasis | `═══════` double-line |
| minimal | Quick | Plain text |
| code | Syntax | Markdown fences |

## Example

```
┌─────────────────────────┐
│ $ python script.py      │
│ Hello World             │
│ Result: 42              │
└─────────────────────────┘
```

## Rules

- Default: box style
- No markdown unless requested
- Line numbers only if asked
