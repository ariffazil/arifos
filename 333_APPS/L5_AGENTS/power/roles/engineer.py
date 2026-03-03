from __future__ import annotations

from importlib import import_module


def ENGINEER():
    module = import_module("333_APPS.L5_AGENTS.agents.engineer")
    return module.ENGINEER()
