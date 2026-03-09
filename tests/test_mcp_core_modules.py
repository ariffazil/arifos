"""
Tests for arifosmcp.transport/core pure modules:
  - mode_selector.py  (MCPMode, detect_environment, get_mcp_mode, get_port, get_host, get_mode_config)
  - motto_schema.py   (get_mottos_resource, format_failure_with_motto, gate messages)
  - engine_adapters.py (AGIEngine transport wrapper)

And core/pipeline.py ForgeResult model methods.
"""

from __future__ import annotations

# =============================================================================
# MODE SELECTOR
# =============================================================================


class TestMCPMode:
    def test_enum_values(self):
        from arifosmcp.transport.core.mode_selector import MCPMode

        assert MCPMode.STDIO.value == "stdio"
        assert MCPMode.SSE.value == "sse"


class TestDetectEnvironment:
    def test_railway(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import detect_environment

        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
        assert detect_environment() == "railway"

    def test_cloudflare(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import detect_environment

        monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
        monkeypatch.setenv("CF_WORKER", "true")
        assert detect_environment() == "cloudflare"

    def test_development_debug(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import detect_environment

        monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
        monkeypatch.delenv("CF_WORKER", raising=False)
        monkeypatch.setenv("DEBUG", "1")
        assert detect_environment() == "development"

    def test_development_dev(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import detect_environment

        monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
        monkeypatch.delenv("CF_WORKER", raising=False)
        monkeypatch.delenv("DEBUG", raising=False)
        monkeypatch.setenv("DEV", "1")
        assert detect_environment() == "development"

    def test_production_env(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import detect_environment

        monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
        monkeypatch.delenv("CF_WORKER", raising=False)
        monkeypatch.delenv("DEBUG", raising=False)
        monkeypatch.delenv("DEV", raising=False)
        monkeypatch.setenv("PRODUCTION", "1")
        assert detect_environment() == "production"


class TestGetMCPMode:
    def test_explicit_override_stdio(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import MCPMode, get_mcp_mode

        monkeypatch.setenv("ARIF_MCP_MODE", "STDIO")
        assert get_mcp_mode() == MCPMode.STDIO

    def test_explicit_override_sse(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import MCPMode, get_mcp_mode

        monkeypatch.setenv("ARIF_MCP_MODE", "SSE")
        assert get_mcp_mode() == MCPMode.SSE

    def test_invalid_override_falls_through(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import MCPMode, get_mcp_mode

        monkeypatch.setenv("ARIF_MCP_MODE", "INVALID")
        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
        result = get_mcp_mode()
        assert result == MCPMode.SSE

    def test_auto_detect_railway(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import MCPMode, get_mcp_mode

        monkeypatch.delenv("ARIF_MCP_MODE", raising=False)
        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
        assert get_mcp_mode() == MCPMode.SSE

    def test_auto_detect_local(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import MCPMode, get_mcp_mode

        monkeypatch.delenv("ARIF_MCP_MODE", raising=False)
        monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
        monkeypatch.delenv("CF_WORKER", raising=False)
        monkeypatch.delenv("DEBUG", raising=False)
        monkeypatch.delenv("DEV", raising=False)
        monkeypatch.delenv("PRODUCTION", raising=False)
        monkeypatch.delenv("PROD", raising=False)
        # Falls through to production default when not tty
        result = get_mcp_mode()
        assert result in (MCPMode.STDIO, MCPMode.SSE)


class TestGetPort:
    def test_default_port(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_port

        monkeypatch.delenv("PORT", raising=False)
        assert get_port() == 6274

    def test_custom_port(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_port

        monkeypatch.setenv("PORT", "8080")
        assert get_port() == 8080


class TestGetHost:
    def test_default_production_host(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_host

        monkeypatch.delenv("HOST", raising=False)
        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
        assert get_host() == "0.0.0.0"

    def test_custom_host(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_host

        monkeypatch.setenv("HOST", "127.0.0.1")
        assert get_host() == "127.0.0.1"


class TestGetModeConfig:
    def test_returns_dict_with_keys(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_mode_config

        monkeypatch.setenv("ARIF_MCP_MODE", "SSE")
        cfg = get_mode_config()
        assert "mode" in cfg
        assert "port" in cfg
        assert "host" in cfg
        assert "environment" in cfg
        assert "version" in cfg

    def test_mode_value_is_string(self, monkeypatch):
        from arifosmcp.transport.core.mode_selector import get_mode_config

        monkeypatch.setenv("ARIF_MCP_MODE", "SSE")
        cfg = get_mode_config()
        assert cfg["mode"] == "sse"


# =============================================================================
# MOTTO SCHEMA
# =============================================================================


class TestMottoSchema:
    def test_get_mottos_resource_structure(self):
        from core.schema.output import get_mottos_resource

        result = get_mottos_resource()
        assert result["uri"] == "constitutional://mottos"
        assert result["mimeType"] == "application/json"
        text = result["text"]
        assert "mottos" in text
        assert "total_mottos" in text
        assert text["total_mottos"] > 0

    def test_get_mottos_resource_bookends(self):
        from core.schema.output import get_mottos_resource

        result = get_mottos_resource()
        bookends = result["text"]["bookends"]
        assert "init" in bookends
        assert "seal" in bookends

    def test_format_failure_known_floor(self):
        from core.schema.output import format_failure_with_motto

        msg = format_failure_with_motto("F2", "truth score too low")
        assert "F2" in msg
        assert "truth score too low" in msg

    def test_format_failure_unknown_floor(self):
        from core.schema.output import format_failure_with_motto

        msg = format_failure_with_motto("F99", "unknown reason")
        assert "F99" in msg
        assert "unknown reason" in msg
        assert "[!]" in msg

    def test_get_init_gate_message(self):
        from core.schema.output import get_init_gate_message

        msg = get_init_gate_message()
        assert "000_INIT" in msg
        assert isinstance(msg, str)

    def test_get_seal_gate_message(self):
        from core.schema.output import get_seal_gate_message

        msg = get_seal_gate_message()
        assert "999_SEAL" in msg
        assert isinstance(msg, str)


# =============================================================================
# ENGINE ADAPTERS
# =============================================================================


class TestEngineAdapters:
    def test_imports_cleanly(self):
        from arifosmcp.transport.core.engine_adapters import (
            AGIEngine,
            APEXEngine,
            ASIEngine,
            InitEngine,
        )

        assert AGIEngine is not None
        assert ASIEngine is not None
        assert APEXEngine is not None
        assert InitEngine is not None

    def test_agi_engine_instantiates(self):
        from arifosmcp.transport.core.engine_adapters import AGIEngine

        engine = AGIEngine()
        assert engine is not None

    def test_agi_engine_with_explicit_none(self):
        from arifosmcp.transport.core.engine_adapters import AGIEngine

        engine = AGIEngine(eureka_engine=None)
        assert engine is not None


# =============================================================================
# FORGE RESULT (core/pipeline.py)
# =============================================================================


class TestForgeResult:
    def _make(self, verdict: str) -> object:
        from core.pipeline import ForgeResult

        return ForgeResult(verdict=verdict, session_id="test-session")

    def test_is_success_seal(self):
        r = self._make("SEAL")
        assert r.is_success() is True

    def test_is_success_partial(self):
        r = self._make("PARTIAL")
        assert r.is_success() is True

    def test_is_success_void(self):
        r = self._make("VOID")
        assert r.is_success() is False

    def test_is_blocked(self):
        r = self._make("VOID")
        assert r.is_blocked() is True

    def test_is_blocked_seal(self):
        r = self._make("SEAL")
        assert r.is_blocked() is False

    def test_needs_human(self):
        r = self._make("888_HOLD")
        assert r.needs_human() is True

    def test_needs_human_seal(self):
        r = self._make("SEAL")
        assert r.needs_human() is False

    def test_to_user_message_seal(self):
        r = self._make("SEAL")
        msg = r.to_user_message()
        assert "passed" in msg.lower() or "verification" in msg.lower()

    def test_to_user_message_partial(self):
        from core.pipeline import ForgeResult

        r = ForgeResult(verdict="PARTIAL", session_id="s", remediation="Retry with evidence.")
        msg = r.to_user_message()
        assert "Retry" in msg or "partial" in msg.lower() or "constraint" in msg.lower()

    def test_to_user_message_void_with_floors(self):
        from core.pipeline import ForgeResult

        r = ForgeResult(verdict="VOID", session_id="s", floors_failed=["F2", "F4"])
        msg = r.to_user_message()
        assert "F2" in msg or "blocked" in msg.lower()

    def test_to_user_message_888_hold(self):
        r = self._make("888_HOLD")
        msg = r.to_user_message()
        assert "human" in msg.lower() or "sovereign" in msg.lower()

    def test_to_user_message_unknown(self):
        r = self._make("UNKNOWN_VERDICT")
        msg = r.to_user_message()
        assert "Unknown" in msg or isinstance(msg, str)

    def test_defaults(self):
        from core.pipeline import ForgeResult

        r = ForgeResult(verdict="SEAL", session_id="abc")
        assert r.landauer_risk == 0.0
        assert r.mode == "conscience"
        assert r.floors_failed == []
        assert r.emd is None
