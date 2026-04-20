/**
 * GEOX Status Polling Protocol
 * Verified State: Site/WebMCP (Live), MCP (Partial), A2A (Not Public)
 */

async function checkSubsurfaceHealth() {
    console.log("INITIATING_SUBSURFACE_HEALTH_QUERY...");
    const healthEndpoint = '/health';
    
    try {
        const response = await fetch(healthEndpoint);
        if (response.ok) {
            console.log("HEALTH_PAYLOAD_RECEIVED: [NOMINAL]");
        } else {
            console.warn("HEALTH_PAYLOAD_ERROR: [DEGRADED]");
        }
    } catch (e) {
        console.error("CONNECTION_FAILURE: [OFFLINE]");
    }
}

// Initial probe
document.addEventListener('DOMContentLoaded', () => {
    checkSubsurfaceHealth();
});
