#!/usr/bin/env python3
"""
Startup wrapper for arifOS MCP Server with error handling.
Logs all startup errors for debugging.
"""

import sys
import os
import logging
import traceback

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("arifos.startup")

def main():
    logger.info("=" * 60)
    logger.info("arifOS MCP Server Starting...")
    logger.info("=" * 60)
    
    # Log environment
    port = os.getenv("PORT", "8080")
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Environment: HOST={host}, PORT={port}")
    
    try:
        # Test imports
        logger.info("Testing imports...")
        from mcp_server.core.tool_registry import ToolRegistry
        from mcp_server.transports.sse import SSETransport
        logger.info("✓ Imports successful")
        
        # Initialize registry
        logger.info("Initializing tool registry...")
        registry = ToolRegistry()
        tool_count = len(registry.list_tools())
        logger.info(f"✓ Tool registry initialized: {tool_count} tools")
        
        # Initialize transport
        logger.info("Initializing SSE transport...")
        transport = SSETransport(registry)
        logger.info(f"✓ Transport initialized: {transport.name}")
        
        # Start server
        logger.info("Starting server...")
        import asyncio
        asyncio.run(transport.start())
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("STARTUP FAILED!")
        logger.error("=" * 60)
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
