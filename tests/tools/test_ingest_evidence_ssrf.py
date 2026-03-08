"""
Tests for SSRF protection in ingest_evidence (F12 — Injection Defense).

Verifies that _validate_url_ssrf rejects:
  - Non-HTTPS schemes
  - Loopback addresses (127.x.x.x, ::1)
  - Private RFC-1918 ranges (10.x, 172.16-31.x, 192.168.x)
  - Link-local / cloud metadata endpoint (169.254.x)
  - Domains outside the optional allowlist

And allows:
  - Valid public HTTPS URLs
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from aaa_mcp.tools.ingest_evidence import _validate_url_ssrf

# ─────────────────────────────────────────────────────────────────────────────
# Scheme enforcement
# ─────────────────────────────────────────────────────────────────────────────


def test_http_scheme_blocked() -> None:
    result = _validate_url_ssrf("http://example.com/data")
    assert result is not None
    assert "Only https://" in result


def test_ftp_scheme_blocked() -> None:
    result = _validate_url_ssrf("ftp://example.com/file.txt")
    assert result is not None
    assert "Only https://" in result


def test_file_scheme_blocked() -> None:
    result = _validate_url_ssrf("file:///etc/passwd")
    assert result is not None
    assert "Only https://" in result


def test_no_scheme_blocked() -> None:
    result = _validate_url_ssrf("example.com/data")
    assert result is not None
    assert "Only https://" in result


# ─────────────────────────────────────────────────────────────────────────────
# Private / loopback / link-local address blocking
# ─────────────────────────────────────────────────────────────────────────────


def _mock_getaddrinfo(ip: str):
    """Return a getaddrinfo-compatible list for a single IPv4 address."""
    return [(2, 1, 6, "", (ip, 0))]


@pytest.mark.parametrize(
    "url, ip",
    [
        # Loopback
        ("https://localhost/admin", "127.0.0.1"),
        ("https://loopback.local/", "127.0.0.1"),
        # Private class A
        ("https://internal.example.com/", "10.0.0.1"),
        ("https://internal.example.com/", "10.255.255.254"),
        # Private class B
        ("https://internal.example.com/", "172.16.0.1"),
        ("https://internal.example.com/", "172.31.255.254"),
        # Private class C
        ("https://internal.example.com/", "192.168.1.1"),
        # Link-local / AWS cloud metadata
        ("https://metadata.internal/", "169.254.169.254"),
        ("https://metadata.internal/", "169.254.0.1"),
        # CGNAT
        ("https://cgnat.example.com/", "100.64.0.1"),
    ],
)
def test_private_ip_blocked(url: str, ip: str) -> None:
    with patch("socket.getaddrinfo", return_value=_mock_getaddrinfo(ip)):
        result = _validate_url_ssrf(url)
    assert result is not None, f"Expected SSRF block for {url} → {ip}"
    assert "SSRF" in result or "forbidden" in result.lower()


def test_ipv6_loopback_blocked() -> None:
    ipv6_addrs = [(10, 1, 6, "", ("::1", 0, 0, 0))]
    with patch("socket.getaddrinfo", return_value=ipv6_addrs):
        result = _validate_url_ssrf("https://v6host.example.com/")
    assert result is not None
    assert "forbidden" in result.lower()


# ─────────────────────────────────────────────────────────────────────────────
# Valid public HTTPS URL
# ─────────────────────────────────────────────────────────────────────────────


def test_public_https_allowed() -> None:
    public_ip = [(2, 1, 6, "", ("93.184.216.34", 0))]  # example.com
    with patch("socket.getaddrinfo", return_value=public_ip):
        result = _validate_url_ssrf("https://example.com/page")
    assert result is None, f"Expected None for public URL, got: {result}"


# ─────────────────────────────────────────────────────────────────────────────
# Optional domain allowlist
# ─────────────────────────────────────────────────────────────────────────────


def test_allowlist_blocks_unlisted_domain() -> None:
    public_ip = [(2, 1, 6, "", ("93.184.216.34", 0))]
    env = {"INGEST_EVIDENCE_ALLOWED_DOMAINS": "trusted.org,docs.mycompany.com"}
    with patch("socket.getaddrinfo", return_value=public_ip):
        with patch.dict(os.environ, env):
            result = _validate_url_ssrf("https://untrusted.net/data")
    assert result is not None
    assert "allowlist" in result.lower()


def test_allowlist_permits_exact_match() -> None:
    public_ip = [(2, 1, 6, "", ("93.184.216.34", 0))]
    env = {"INGEST_EVIDENCE_ALLOWED_DOMAINS": "trusted.org,example.com"}
    with patch("socket.getaddrinfo", return_value=public_ip):
        with patch.dict(os.environ, env):
            result = _validate_url_ssrf("https://example.com/page")
    assert result is None, f"Expected None for allowed domain, got: {result}"


def test_allowlist_permits_subdomain() -> None:
    public_ip = [(2, 1, 6, "", ("93.184.216.34", 0))]
    env = {"INGEST_EVIDENCE_ALLOWED_DOMAINS": "example.com"}
    with patch("socket.getaddrinfo", return_value=public_ip):
        with patch.dict(os.environ, env):
            result = _validate_url_ssrf("https://docs.example.com/api")
    assert result is None, f"Expected None for allowed subdomain, got: {result}"


def test_allowlist_not_set_permits_public_url() -> None:
    public_ip = [(2, 1, 6, "", ("93.184.216.34", 0))]
    with patch("socket.getaddrinfo", return_value=public_ip):
        with patch.dict(os.environ, {}, clear=False):
            # Ensure var is absent
            os.environ.pop("INGEST_EVIDENCE_ALLOWED_DOMAINS", None)
            result = _validate_url_ssrf("https://example.com/page")
    assert result is None


# ─────────────────────────────────────────────────────────────────────────────
# DNS resolution failure
# ─────────────────────────────────────────────────────────────────────────────


def test_unresolvable_hostname_blocked() -> None:
    import socket

    with patch("socket.getaddrinfo", side_effect=socket.gaierror("Name or service not known")):
        result = _validate_url_ssrf("https://nonexistent.invalid/data")
    assert result is not None
    assert "resolve" in result.lower()


# ─────────────────────────────────────────────────────────────────────────────
# ingest_evidence integration — BLOCKED_SSRF envelope
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_ingest_evidence_returns_blocked_ssrf_for_http() -> None:
    from aaa_mcp.tools.ingest_evidence import ingest_evidence

    result = await ingest_evidence(source_type="url", target="http://example.com")
    assert result["status"] == "BLOCKED_SSRF"
    assert "error" in result


@pytest.mark.asyncio
async def test_ingest_evidence_returns_blocked_ssrf_for_localhost() -> None:
    from aaa_mcp.tools.ingest_evidence import ingest_evidence

    loopback = [(2, 1, 6, "", ("127.0.0.1", 0))]
    with patch("socket.getaddrinfo", return_value=loopback):
        result = await ingest_evidence(source_type="url", target="https://localhost/admin")
    assert result["status"] == "BLOCKED_SSRF"
