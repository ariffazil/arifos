"""
arifOS Structured Logging (v55.5-HARDENED)

Production-grade logging with:
- Correlation IDs for request tracing
- Structured JSON output
- MCP tool invocation tracking
- Constitutional floor audit trail
- Railway/Cloudflare compatible

Usage:
    from aaa_mcp.infrastructure.logging import get_logger, correlation_id
    
    logger = get_logger(__name__)
    
    with correlation_id() as cid:
        logger.info("Processing request", extra={"tool": "apex_judge", "floor": "F1"})
"""

import logging
import json
import uuid
import time
import os
from datetime import datetime, timezone
from typing import Optional, Any, Dict
from contextvars import ContextVar
from functools import wraps

# Context variable for correlation ID
_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": _correlation_id.get(),
        }
        
        # Add extra fields
        if hasattr(record, "tool"):
            log_entry["tool"] = record.tool
        if hasattr(record, "floor"):
            log_entry["floor"] = record.floor
        if hasattr(record, "verdict"):
            log_entry["verdict"] = record.verdict
        if hasattr(record, "omega"):
            log_entry["omega"] = record.omega
        if hasattr(record, "latency_ms"):
            log_entry["latency_ms"] = record.latency_ms
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        
        # Add any other extra fields
        for key, value in record.__dict__.items():
            if key not in ("name", "msg", "args", "created", "filename", 
                          "funcName", "levelname", "levelno", "lineno",
                          "module", "msecs", "pathname", "process",
                          "processName", "relativeCreated", "stack_info",
                          "exc_info", "exc_text", "thread", "threadName",
                          "message", "tool", "floor", "verdict", "omega",
                          "latency_ms", "request_id"):
                if not key.startswith("_"):
                    log_entry[key] = value
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, default=str)


class ConsoleFormatter(logging.Formatter):
    """Human-readable formatter for development."""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        cid = _correlation_id.get()
        cid_str = f"[{cid[:8]}]" if cid else ""
        
        # Build extra info string
        extras = []
        if hasattr(record, "tool"):
            extras.append(f"tool={record.tool}")
        if hasattr(record, "floor"):
            extras.append(f"floor={record.floor}")
        if hasattr(record, "verdict"):
            extras.append(f"verdict={record.verdict}")
        if hasattr(record, "latency_ms"):
            extras.append(f"latency={record.latency_ms}ms")
        
        extra_str = f" ({', '.join(extras)})" if extras else ""
        
        return f"{color}{record.levelname:8}{self.RESET} {cid_str} {record.name}: {record.getMessage()}{extra_str}"


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Determine format based on environment
        is_production = os.environ.get("RAILWAY", "") == "true" or \
                       os.environ.get("RENDER", "") == "true" or \
                       os.environ.get("LOG_FORMAT", "").lower() == "json"
        
        handler = logging.StreamHandler()
        
        if is_production:
            handler.setFormatter(StructuredFormatter())
        else:
            handler.setFormatter(ConsoleFormatter())
        
        logger.addHandler(handler)
        
        # Set level from environment
        level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, level, logging.INFO))
    
    return logger


class correlation_id:
    """Context manager for correlation ID."""
    
    def __init__(self, cid: Optional[str] = None):
        self.cid = cid or str(uuid.uuid4())
        self.token = None
    
    def __enter__(self) -> str:
        self.token = _correlation_id.set(self.cid)
        return self.cid
    
    def __exit__(self, *args):
        _correlation_id.reset(self.token)


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID."""
    return _correlation_id.get()


def set_correlation_id(cid: str) -> None:
    """Set correlation ID (use context manager when possible)."""
    _correlation_id.set(cid)


def log_tool_call(logger: logging.Logger):
    """Decorator to log MCP tool calls with timing."""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cid = get_correlation_id() or str(uuid.uuid4())[:8]
            start = time.perf_counter()
            
            logger.info(
                f"Tool call started: {func.__name__}",
                extra={"tool": func.__name__, "correlation_id": cid}
            )
            
            try:
                result = await func(*args, **kwargs)
                latency = (time.perf_counter() - start) * 1000
                
                logger.info(
                    f"Tool call completed: {func.__name__}",
                    extra={
                        "tool": func.__name__,
                        "latency_ms": round(latency, 2),
                        "verdict": "SEAL"
                    }
                )
                return result
                
            except Exception as e:
                latency = (time.perf_counter() - start) * 1000
                logger.error(
                    f"Tool call failed: {func.__name__}: {e}",
                    extra={
                        "tool": func.__name__,
                        "latency_ms": round(latency, 2),
                        "verdict": "VOID"
                    },
                    exc_info=True
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cid = get_correlation_id() or str(uuid.uuid4())[:8]
            start = time.perf_counter()
            
            logger.info(
                f"Tool call started: {func.__name__}",
                extra={"tool": func.__name__}
            )
            
            try:
                result = func(*args, **kwargs)
                latency = (time.perf_counter() - start) * 1000
                
                logger.info(
                    f"Tool call completed: {func.__name__}",
                    extra={
                        "tool": func.__name__,
                        "latency_ms": round(latency, 2),
                        "verdict": "SEAL"
                    }
                )
                return result
                
            except Exception as e:
                latency = (time.perf_counter() - start) * 1000
                logger.error(
                    f"Tool call failed: {func.__name__}: {e}",
                    extra={
                        "tool": func.__name__,
                        "latency_ms": round(latency, 2),
                        "verdict": "VOID"
                    },
                    exc_info=True
                )
                raise
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# Pre-configured loggers
mcp_logger = get_logger("aaa_mcp")
tool_logger = get_logger("aaa_mcp.tools")
floor_logger = get_logger("aaa_mcp.floors")
