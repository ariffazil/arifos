
import pytest
import httpx

# The base URL of the running server is provided by the `mcp_server` fixture
# in conftest.py.

def test_init_gate_e2e(mcp_server):
    """
    E2E test for the L0 init_gate tool.
    
    Given: The aaa_mcp server is running.
    When: A request is made to the init_gate tool's endpoint.
    Then: The server should return a successful response, indicating the
          session has been initialized.
    """
    # Arrange
    # The tool name is 'init_gate'. We assume the endpoint is /tools/init_gate
    # and it accepts POST requests, as is common for tool-based APIs.
    # We will need to verify the exact endpoint and method from the server's code
    # or documentation.
    tool_endpoint = f"{mcp_server}/tools/init_gate"
    
    # The request payload might include authorization details or session parameters.
    # For a first test, we'll send an empty payload.
    request_payload = {
        "params": {}
    }

    # Act
    try:
        response = httpx.post(tool_endpoint, json=request_payload, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    except httpx.RequestError as e:
        pytest.fail(f"Failed to connect to the mcp_server at {tool_endpoint}. "
                    f"Make sure the server is running and the endpoint is correct. "
                    f"Error: {e}")

    # Assert
    assert response.status_code == 200
    
    # The response should contain some data. We'll check for the presence of
    # a 'result' key in the JSON response, which is a common pattern.
    response_data = response.json()
    assert "result" in response_data
    
    # The result for init_gate might contain a session ID or a status message.
    # Let's check for a 'status' key in the result.
    assert "status" in response_data["result"]
    assert response_data["result"]["status"] == "OK"

# To expand this, we would add more tests for the other 8 canonical tools.
# For example:
#
# def test_agi_sense_e2e(mcp_server):
#     """E2E test for the L1 agi_sense tool."""
#     # ... similar arrange, act, assert steps ...
#
# def test_reality_search_e2e(mcp_server):
#     """E2E test for the L6 reality_search tool."""
#     # Arrange
#     tool_endpoint = f"{mcp_server}/tools/reality_search"
#     request_payload = {
#         "params": {
#             "query": "latest news on Gemini",
#             "max_results": 5
#         }
#     }
#     # Act
#     response = httpx.post(tool_endpoint, json=request_payload, timeout=30)
#     # Assert
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "result" in response_data
#     assert "results" in response_data["result"]
#     assert len(response_data["result"]["results"]) > 0

