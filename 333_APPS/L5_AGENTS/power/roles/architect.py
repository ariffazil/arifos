from __future__ import annotations

from importlib import import_module


def ARCHITECT():
    module = import_module("333_APPS.L5_AGENTS.agents.architect")
    return module.ARCHITECT()
