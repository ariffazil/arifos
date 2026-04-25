"""
Compatibility shim — renamed to sense.py
This file will be removed after one sprint.
"""
import warnings
warnings.warn("sense_observe.py is deprecated — use sense.py instead", DeprecationWarning, stacklevel=2)
from arifosmcp.tools.sense import *  # noqa: F401,F403
