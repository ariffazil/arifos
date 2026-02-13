
import httpx

def test_server_health_and_root_e2e(mcp_server):
    """E2E smoke test for the Railway entrypoint routes."""
    health_resp = httpx.get(f"{mcp_server}/health", timeout=10)
    health_resp.raise_for_status()
    health_data = health_resp.json()
    assert health_data["status"] == "ok"

    root_resp = httpx.get(f"{mcp_server}/", timeout=10)
    root_resp.raise_for_status()
    root_data = root_resp.json()
    assert root_data["status"] == "operational"
    assert "endpoints" in root_data
    assert root_data["endpoints"]["sse"] == "/sse"

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

