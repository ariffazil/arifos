"""Compatibility launcher.

Phase 4 default external runtime is `arifos_aaa_mcp`.
"""

from __future__ import annotations

def main() -> None:
    from arifos_aaa_mcp.__main__ import main as aaa_main

    aaa_main()


if __name__ == "__main__":
    main()
