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

    init_prompt = collector.prompts["init_anchor_state_prompt"]
    assert "init_anchor_state" in init_prompt("Arif")
