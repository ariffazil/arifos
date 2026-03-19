"""Fix < and <= in markdown to use HTML entities for MDX compatibility."""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

count = 0
for root, dirs, files in os.walk(os.path.join(BASE, "docs")):
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".docusaurus", "build")]
    for fname in files:
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        original = content

        # Replace < followed by a space or digit (not HTML tags like <a> or <em>)
        # This handles patterns like "< 0.85", "<= 0", etc.
        content = re.sub(r"<(?=\s*\d)", r"&lt;", content)
        content = re.sub(r"<=(?=\s*\d)", r"&lt;=", content)
        # Fix double-escaped: &lt;<= -> &lt;=
        content = content.replace("&lt;<=", "&lt;=")

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            rel = os.path.relpath(fpath, BASE)
            print(f"Fixed: {rel}")
            count += 1

print(f"\nDone. Fixed {count} files.")
