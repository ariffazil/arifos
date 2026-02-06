"""
Minimal arifOS Server — Without MCP dependencies

This version avoids the problematic MCP dependencies to at least get the core service running.
"""

import os
from flask import Flask, jsonify

# Railway provides PORT and HOST via environment
port = int(os.environ.get("PORT", 3000))  # Default to 3000 instead of 8080
host = os.environ.get("HOST", "0.0.0.0")

app = Flask(__name__)

@app.route('/')
def health():
    """Health endpoint for service status"""
    return jsonify({
        "status": "running", 
        "service": "arifOS", 
        "constitution": "13 Floors",
        "theory": "Reverse Transformer",
        "version": "v55.4-SEAL"
    })

@app.route('/health')
def simple_health():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host=host, port=port, debug=False)