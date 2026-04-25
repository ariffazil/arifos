"""
Compatibility shim — prompts.py renamed to prompt.py
This file will be removed after one sprint.
"""
import warnings
warnings.warn("prompts.py is deprecated — use prompt.py instead", DeprecationWarning, stacklevel=2)
from arifosmcp.runtime.prompt import *  # noqa: F401,F403
