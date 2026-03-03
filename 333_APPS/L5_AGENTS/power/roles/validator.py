from __future__ import annotations

from importlib import import_module


def VALIDATOR():
    module = import_module("333_APPS.L5_AGENTS.agents.validator")
    return module.VALIDATOR()
