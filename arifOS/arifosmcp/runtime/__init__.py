"""
Shim: arifOS.arifosmcp.runtime → arifos.runtime
arifOS package is namespace-only (no package dir), so all imports route through arifos.
"""
from arifos.runtime import *
from arifos.runtime import __all__
