
import pytest
import subprocess
import time
import socket
import os
import sys
import httpx

def find_free_port():
    """Finds a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="session")
def mcp_server():
    """
    A pytest fixture to start and stop the aaa_mcp server for E2E tests.
    """
    port = find_free_port()
    base_url = f"http://localhost:{port}"

    env = os.environ.copy()
    env["PORT"] = str(port)
    env.setdefault("HOST", "127.0.0.1")

    # Start the same Starlette/SSE entrypoint used on Railway.
    command = [
        sys.executable,
        "scripts/start_server.py",
    ]

    # Start the server as a background process
    server_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    # Probe health endpoint until ready.
    health_url = f"{base_url}/health"
    started = False
    for _ in range(40):
        if server_process.poll() is not None:
            break
        try:
            response = httpx.get(health_url, timeout=0.5)
            if response.status_code == 200:
                started = True
                break
        except Exception:
            pass
        time.sleep(0.25)

    # Check if the process is still running
    if server_process.poll() is not None or not started:
        # Process has terminated, something went wrong
        stdout, stderr = server_process.communicate()
        raise RuntimeError(
            f"""Failed to start mcp_server.
            Exit code: {server_process.returncode}
            Stdout: {stdout.decode()}
            Stderr: {stderr.decode()}"""
        )

    print(f"MCP Server started on {base_url}")

    # Yield the base URL to the tests
    yield base_url

    # Teardown: stop the server
    print("Stopping MCP Server...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
    print("MCP Server stopped.")

