"""Verify VAULT999 ledger integrity (chain continuity + JSON validity).

Usage:
    python scripts/verify_vault_integrity.py
    python scripts/verify_vault_integrity.py --vault-path VAULT999/BBB_LEDGER/vault.jsonl

Exit codes:
    0 — Vault OK or empty (acceptable for fresh install)
    1 — Chain integrity violation detected
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def verify(vault_path: Path) -> bool:
    """Return True if vault is valid (or empty). Print findings to stderr."""
    if not vault_path.exists():
        print(f"VAULT: {vault_path} not found — OK for fresh install", file=sys.stderr)
        return True

    entries: list[dict] = []
    with vault_path.open() as fh:
        for lineno, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                entries.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                print(f"VAULT ERROR: line {lineno} is not valid JSON: {exc}", file=sys.stderr)
                return False

    if not entries:
        print("VAULT: empty ledger — OK for fresh install", file=sys.stderr)
        return True

    # Verify hash chain continuity
    for i, entry in enumerate(entries):
        if i == 0:
            # Genesis entry: no previous link to validate
            continue

        prev = entries[i - 1]

        # Use consistent hash pairs only:
        #   - prev["entry_hash"]     ↔ entry["prev_hash"]
        #   - prev["current_hash"]   ↔ entry["previous_hash"]
        # For non-genesis entries, missing fields that prevent forming at least one
        # complete pair are treated as integrity failures.
        prev_entry_hash = prev.get("entry_hash")
        prev_current_hash = prev.get("current_hash")
        entry_prev_hash = entry.get("prev_hash")
        entry_previous_hash = entry.get("previous_hash")

        sequence = entry.get("sequence", i + 1)

        pair_entry_prev_possible = prev_entry_hash is not None and entry_prev_hash is not None
        pair_current_previous_possible = (
            prev_current_hash is not None and entry_previous_hash is not None
        )

        # If we cannot form at least one complete pair, the chain link is invalid.
        if not pair_entry_prev_possible and not pair_current_previous_possible:
            print(
                "VAULT ERROR: missing hash fields at sequence "
                f"{sequence}: cannot verify previous link "
                f"(prev_entry_hash={prev_entry_hash!r}, prev_current_hash={prev_current_hash!r}, "
                f"entry_prev_hash={entry_prev_hash!r}, entry_previous_hash={entry_previous_hash!r})",
                file=sys.stderr,
            )
            return False

        # Validate any possible pairs. All present pairs must match.
        if pair_entry_prev_possible and prev_entry_hash != entry_prev_hash:
            print(
                f"VAULT ERROR: chain break at sequence {sequence}: "
                f"expected prev_hash (from entry_hash)={prev_entry_hash!r}, "
                f"got {entry_prev_hash!r}",
                file=sys.stderr,
            )
            return False

        if pair_current_previous_possible and prev_current_hash != entry_previous_hash:
            print(
                f"VAULT ERROR: chain break at sequence {sequence}: "
                f"expected previous_hash (from current_hash)={prev_current_hash!r}, "
                f"got {entry_previous_hash!r}",
                file=sys.stderr,
            )
            return False
    print(
        f"VAULT OK: {len(entries)} entries, chain continuous ({vault_path})",
        file=sys.stderr,
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify VAULT999 ledger integrity")
    parser.add_argument(
        "--vault-path",
        default="VAULT999/BBB_LEDGER/vault.jsonl",
        help="Path to the vault JSONL ledger file",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    ok = verify(vault_path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
