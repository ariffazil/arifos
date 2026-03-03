from __future__ import annotations

from importlib import import_module


def AUDITOR():
    module = import_module("333_APPS.L5_AGENTS.agents.auditor")
    return module.AUDITOR()
