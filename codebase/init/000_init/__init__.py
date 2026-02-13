"""
codebase/init/000_init/__init__.py

Note: This directory name starts with a digit (000_init) which is not a valid
Python identifier. Use importlib to import modules from this package:

    spec = importlib.util.spec_from_file_location("init_000", "codebase/init/000_init/init_000.py")
    module = importlib.util.module_from_spec(spec)

Or use the parent package:

    from codebase.init import mcp_000_init, InitResult
"""

# Export canonical_bootstrap (valid Python name)
from .canonical_bootstrap import (
    CanonicalBootstrap,
    fetch_canonical_state,
    CanonicalBootstrapResult,
    CanonicalSourceResult,
    CanonicalConfigLoader,
    CanonicalFetchEngine,
    get_bootstrap_config,
    DEFAULT_CANONICAL_CONFIG,
)

__all__ = [
    "CanonicalBootstrap",
    "fetch_canonical_state",
    "CanonicalBootstrapResult",
    "CanonicalSourceResult",
    "CanonicalConfigLoader",
    "CanonicalFetchEngine",
    "get_bootstrap_config",
    "DEFAULT_CANONICAL_CONFIG",
]
