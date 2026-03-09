"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""Environment bootstrap for arifOS runtime entrypoints.

Load order (first existing file wins):
1) ENV_FILE (explicit path)
2) ~/.arifos/env (solo sovereign global profile)
3) <repo>/.env (local compatibility stub)

Shell-exported variables always take precedence (override=False).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


def _candidate_env_files() -> list[Path]:
    candidates: list[Path] = []

    explicit = os.getenv("ENV_FILE", "").strip()
    if explicit:
        candidates.append(Path(explicit).expanduser())

    candidates.append(Path.home() / ".arifos" / "env")
    candidates.append(Path(__file__).resolve().parent.parent / ".env")
    return candidates


@lru_cache(maxsize=1)
def bootstrap_environment() -> str | None:
    """Load a canonical environment file once per process.

    Returns the path that was loaded, or None if no file was loaded.
    """

    try:
        from dotenv import load_dotenv
    except Exception:
        return None

    for path in _candidate_env_files():
        if not path.is_file():
            continue

        load_dotenv(dotenv_path=path, override=False)
        os.environ.setdefault("ARIFOS_ENV_SOURCE", str(path))
        return str(path)

    return None
