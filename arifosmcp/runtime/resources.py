"""
Compatibility shim — resources.py renamed to resource.py
This file will be removed after one sprint.
"""
import warnings
warnings.warn("resources.py is deprecated — use resource.py instead", DeprecationWarning, stacklevel=2)
from arifosmcp.runtime.resource import *  # noqa: F401,F403
