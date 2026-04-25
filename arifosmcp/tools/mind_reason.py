"""
Compatibility shim — renamed to reason.py
This file will be removed after one sprint.
"""
import warnings
warnings.warn("mind_reason.py is deprecated — use reason.py instead", DeprecationWarning, stacklevel=2)
from arifosmcp.tools.reason import *  # noqa: F401,F403
