"""
codebase/init/__init__.py — Init stage package

Provides canonical bootstrap functionality.
Note: 000_init modules should be imported via canonical_trinity or importlib
due to the digit-starting module name.
"""

import importlib.util
import sys
from pathlib import Path

# Load canonical_bootstrap using importlib (valid Python filename)
_cb_path = Path(__file__).parent / "000_init" / "canonical_bootstrap.py"
if _cb_path.exists():
    spec = importlib.util.spec_from_file_location("codebase.init.canonical_bootstrap", _cb_path)
    _cb = importlib.util.module_from_spec(spec)
    # Register module BEFORE exec_module (required for dataclass resolution)
    sys.modules["codebase.init.canonical_bootstrap"] = _cb
    spec.loader.exec_module(_cb)
    
    # Export canonical bootstrap components
    CanonicalBootstrap = _cb.CanonicalBootstrap
    fetch_canonical_state = _cb.fetch_canonical_state
    CanonicalBootstrapResult = _cb.CanonicalBootstrapResult
    CanonicalSourceResult = _cb.CanonicalSourceResult
    CanonicalConfigLoader = _cb.CanonicalConfigLoader
    get_bootstrap_config = _cb.get_bootstrap_config
    DEFAULT_CANONICAL_CONFIG = _cb.DEFAULT_CANONICAL_CONFIG

__all__ = [
    "CanonicalBootstrap",
    "fetch_canonical_state",
    "CanonicalBootstrapResult",
    "CanonicalSourceResult",
    "CanonicalConfigLoader",
    "get_bootstrap_config",
    "DEFAULT_CANONICAL_CONFIG",
]
