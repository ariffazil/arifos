from __future__ import annotations

from arifosmcp.runtime.prompts import register_prompts
from arifosmcp.runtime.public_registry import PUBLIC_PROMPT_SPECS


class _PromptCollector:
    def __init__(self) -> None:
        self.prompts: dict[str, object] = {}

    def prompt(self):  # type: ignore[no-untyped-def]
        def decorator(fn):  # type: ignore[no-untyped-def]
            self.prompts[fn.__name__] = fn
            return fn

        return decorator


def test_register_prompts_matches_public_registry() -> None:
    collector = _PromptCollector()
    register_prompts(collector)  # type: ignore[arg-type]

    expected_names = {spec.name for spec in PUBLIC_PROMPT_SPECS}
    assert set(collector.prompts) == expected_names

    dashboard_prompt = collector.prompts["open_apex_dashboard"]
    assert "open_apex_dashboard" in dashboard_prompt()

    bootstrap_prompt = collector.prompts["bootstrap_identity_prompt"]
    assert "bootstrap_identity" in bootstrap_prompt("Arif")
