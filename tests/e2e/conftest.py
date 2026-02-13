
import pytest
import subprocess
import time
import socket
import os
import sys

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

    # Command to start the server. Assuming it's run as a module.
    # We will need to verify this and adjust if necessary.
    command = [
        sys.executable,
        "-m",
        "aaa_mcp.server",
        "--port",
        str(port),
    ]

    # Start the server as a background process
    server_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )

    # Wait for a moment to let the server start
    time.sleep(3)

    # Check if the process is still running
    if server_process.poll() is not None:
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

