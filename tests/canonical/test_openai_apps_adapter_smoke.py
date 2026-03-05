"""Smoke tests for OpenAI Apps adapter resource helpers."""

from __future__ import annotations

from adapters.openai_apps import ui_resources


class _MCPStub:
    def __init__(self) -> None:
        self.registered: list[dict[str, object]] = []

    def resource(self, uri: str, **kwargs):
        def _decorator(fn):
            self.registered.append({"uri": uri, "kwargs": kwargs, "fn": fn})
            return fn

        return _decorator


def test_alias_resolution_smoke() -> None:
    assert ui_resources.resolve_canonical_tool_name("search") == "search_reality"
    assert ui_resources.resolve_canonical_tool_name("fetch") == "fetch_content"
    assert ui_resources.resolve_canonical_tool_name("health_check") == "check_vital"
    assert ui_resources.resolve_canonical_tool_name("anchor_session") == "anchor_session"


def test_visualizer_html_loader_smoke() -> None:
    html = ui_resources.load_constitutional_visualizer_html()
    assert isinstance(html, str)
    assert "<html" in html.lower()


def test_register_resource_smoke() -> None:
    stub = _MCPStub()
    ui_resources.register_constitutional_visualizer_resource(stub)

    assert len(stub.registered) == 1
    entry = stub.registered[0]
    assert entry["uri"] == ui_resources.UI_RESOURCE_URI
    kwargs = entry["kwargs"]
    assert kwargs["name"] == ui_resources.UI_RESOURCE_NAME
    assert kwargs["mime_type"] == ui_resources.UI_RESOURCE_MIME

    fn = entry["fn"]
    html = fn()
    assert isinstance(html, str)
    assert len(html) > 0
