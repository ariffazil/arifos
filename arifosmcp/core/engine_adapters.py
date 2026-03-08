"""Transport-facing engine adapter compatibility layer.

Kernel logic lives in `core.kernel.engine_adapters`.
This module keeps historical `aaa_mcp.core.engine_adapters` imports stable.
"""

from __future__ import annotations

from typing import Any

from core.kernel.engine_adapters import AGIEngine as _KernelAGIEngine
from core.kernel.engine_adapters import APEXEngine, ASIEngine, InitEngine

try:
    from aaa_mcp.vault.hardened import HardenedAnomalousContrastEngine
except ImportError:
    HardenedAnomalousContrastEngine = None


class AGIEngine(_KernelAGIEngine):
    """Transport wrapper that optionally wires EUREKA integration."""

    def __init__(self, eureka_engine: Any | None = None):
        if eureka_engine is None and HardenedAnomalousContrastEngine is not None:
            eureka_engine = HardenedAnomalousContrastEngine()
        super().__init__(eureka_engine=eureka_engine)


__all__ = ["InitEngine", "AGIEngine", "ASIEngine", "APEXEngine"]
