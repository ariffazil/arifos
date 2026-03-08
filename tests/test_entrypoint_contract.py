"""Contract tests: required entrypoint files and importable modules."""

from __future__ import annotations

from pathlib import Path


def test_required_entrypoint_files_exist() -> None:
    for path in (
        "arifosmcp.transport/__main__.py",
        "arifosmcp.transport/server.py",
        "arifosmcp.transport/rest.py",
        "arifosmcp.transport/streamable_http_server.py",
        "Dockerfile",
        "fastmcp.json",
        "server.json",
    ):
        assert Path(path).exists(), f"Required entrypoint file missing: {path}"


def test_server_json_version_matches_pyproject() -> None:
    import json
    import tomllib

    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    py_ver = pyproject["project"]["version"]
    server = json.loads(Path("server.json").read_text(encoding="utf-8"))
    assert (
        py_ver == server["version"]
    ), f"Version mismatch: pyproject={py_ver}, server.json={server['version']}"
    assert server["name"] == "io.github.ariffazil/arifos-mcp"


def test_aaa_mcp_main_importable() -> None:
    import importlib

    importlib.import_module("arifosmcp.transport.__main__")


def test_aaa_mcp_rest_importable() -> None:
    import importlib

    importlib.import_module("arifosmcp.transport.rest")


def test_aaa_mcp_streamable_http_importable() -> None:
    import importlib

    importlib.import_module("arifosmcp.transport.streamable_http_server")


def test_dockerfile_has_oci_label() -> None:
    content = Path("Dockerfile").read_text(encoding="utf-8")
    assert (
        'io.modelcontextprotocol.server.name="io.github.ariffazil/arifos-mcp"' in content
    ), "Dockerfile missing required OCI label"
