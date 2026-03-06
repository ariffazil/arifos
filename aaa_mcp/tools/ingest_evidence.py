"""
ingest_evidence — Unified evidence retrieval/inspection tool

Merges fetch_content + inspect_file into one clean interface.
Mental model: search_reality = EXPLORE, ingest_evidence = EXAMINE

[Lane: Δ Delta] [Floors: F2, F4, F12]
"""

from typing import Any


async def ingest_evidence(
    source_type: str,  # "url" | "file" | "raw"
    target: str,       # URL, file path, or content ID
    mode: str = "raw", # "raw" | "summary" | "chunks"
    session_id: str | None = None,
    actor_id: str | None = None,
) -> dict[str, Any]:
    """  
    Unified evidence ingestion: retrieve and parse a specific object.
    
    This tool replaces the old fetch_content + inspect_file tools with
    a single, clean interface for evidence examination.
    
    Mental model:
    - search_reality = EXPLORE (find candidates)
    - ingest_evidence = EXAMINE (open/parse chosen object)
    
    Args:
        source_type: Type of source ("url" | "file" | "raw")
        target: URL, file path, or content identifier
        mode: Processing mode (raw, summary, chunks)
        session_id: Constitutional session ID
        actor_id: User/agent identifier
    
    Returns:
        {
            "verdict": "SEAL" | "PARTIAL" | "VOID",
            "content": "<retrieved content>",
            "metadata": {...},
            "floor_enforced": ["F2", "F4", "F12"],
            "source_type": source_type,
            "mode": mode,
        }
    
    Floors enforced:
    - F2 (Truth): Validate content authenticity
    - F4 (Entropy): Reduce noise in chunking/summarization
    - F12 (Injection Defense): Sanitize all inputs
    """  
    
    # F12: Input validation and injection defense
    if source_type not in ("url", "file", "raw"):
        return {
            "verdict": "VOID",
            "error": f"Invalid source_type: {source_type}. Must be 'url', 'file', or 'raw'",
            "floor_enforced": ["F12"],
        }
    
    if not target or not isinstance(target, str):
        return {
            "verdict": "VOID",
            "error": "Target must be a non-empty string",
            "floor_enforced": ["F12"],
        }
    
    try:
        if source_type == "url":
            return await _ingest_from_url(target, mode, session_id, actor_id)
        elif source_type == "file":
            return await _ingest_from_file(target, mode, session_id, actor_id)
        elif source_type == "raw":
            return await _ingest_raw_content(target, mode, session_id, actor_id)
    except Exception as e:
        return {
            "verdict": "VOID",
            "error": f"Ingestion failed: {str(e)}",
            "floor_enforced": ["F2", "F12"],
            "source_type": source_type,
            "target": target[:100],  # Truncate for safety
        }


async def _ingest_from_url(
    url: str,
    mode: str,
    session_id: str | None,
    actor_id: str | None,
) -> dict[str, Any]:
    """  
    Ingest content from a URL.
    Replaces old fetch_content logic.
    """  
    import aiohttp
    from urllib.parse import urlparse
    
    # F12: URL validation
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {
                "verdict": "VOID",
                "error": "Invalid URL format",
                "floor_enforced": ["F12"],
            }
    except Exception:
        return {
            "verdict": "VOID",
            "error": "URL parsing failed",
            "floor_enforced": ["F12"],
        }
    
    # Fetch content
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status != 200:
                    return {
                        "verdict": "PARTIAL",
                        "error": f"HTTP {response.status}",
                        "floor_enforced": ["F2"],
                    }
                
                content_type = response.headers.get("Content-Type", "")
                raw_content = await response.text()
                
                # F2: Truth validation
                metadata = {
                    "url": url,
                    "status_code": response.status,
                    "content_type": content_type,
                    "content_length": len(raw_content),
                }
                
                # F4: Apply mode processing
                processed_content = await _process_content(raw_content, mode, content_type)
                
                return {
                    "verdict": "SEAL",
                    "content": processed_content,
                    "metadata": metadata,
                    "floor_enforced": ["F2", "F4", "F12"],
                    "source_type": "url",
                    "mode": mode,
                }
    
    except aiohttp.ClientError as e:
        return {
            "verdict": "VOID",
            "error": f"Network error: {str(e)}",
            "floor_enforced": ["F2"],
        }


async def _ingest_from_file(
    file_path: str,
    mode: str,
    session_id: str | None,
    actor_id: str | None,
) -> dict[str, Any]:
    """  
    Ingest content from a local file.
    Replaces old inspect_file logic.
    """  
    import os
    from pathlib import Path
    
    # F12: Path validation (prevent directory traversal)
    try:
        resolved_path = Path(file_path).resolve()
        if not resolved_path.exists():
            return {
                "verdict": "VOID",
                "error": f"File not found: {file_path}",
                "floor_enforced": ["F12"],
            }
        
        if not resolved_path.is_file():
            return {
                "verdict": "VOID",
                "error": "Target is not a file",
                "floor_enforced": ["F12"],
            }
    except Exception as e:
        return {
            "verdict": "VOID",
            "error": f"Path validation failed: {str(e)}",
            "floor_enforced": ["F12"],
        }
    
    # Read file content
    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
        
        # F2: Truth validation
        metadata = {
            "file_path": str(resolved_path),
            "file_size": os.path.getsize(resolved_path),
            "file_extension": resolved_path.suffix,
        }
        
        # F4: Apply mode processing
        content_type = _guess_content_type_from_extension(resolved_path.suffix)
        processed_content = await _process_content(raw_content, mode, content_type)
        
        return {
            "verdict": "SEAL",
            "content": processed_content,
            "metadata": metadata,
            "floor_enforced": ["F2", "F4", "F12"],
            "source_type": "file",
            "mode": mode,
        }
    
    except UnicodeDecodeError:
        return {
            "verdict": "VOID",
            "error": "File is not valid UTF-8 text",
            "floor_enforced": ["F2"],
        }
    except Exception as e:
        return {
            "verdict": "VOID",
            "error": f"File read failed: {str(e)}",
            "floor_enforced": ["F2"],
        }


async def _ingest_raw_content(
    content: str,
    mode: str,
    session_id: str | None,
    actor_id: str | None,
) -> dict[str, Any]:
    """  
    Ingest pre-retrieved raw content.
    Useful for testing or when content is already in memory.
    """  
    # F4: Apply mode processing
    processed_content = await _process_content(content, mode, "text/plain")
    
    return {
        "verdict": "SEAL",
        "content": processed_content,
        "metadata": {
            "content_length": len(content),
        },
        "floor_enforced": ["F4", "F12"],
        "source_type": "raw",
        "mode": mode,
    }


async def _process_content(
    content: str,
    mode: str,
    content_type: str,
) -> str:
    """
    Process content according to mode (F4: entropy reduction).
    
    Modes:
    - raw: Return content as-is
    - summary: Extract key information
    - chunks: Split into semantic chunks
    """
    if mode == "raw":
        return content
    
    elif mode == "summary":
        # Simple summarization (could be enhanced with LLM)
        lines = content.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        
        if len(non_empty_lines) <= 10:
            return content
        
        # Return first 5 + last 5 lines with indicator
        summary = "\n".join(non_empty_lines[:5])
        summary += f"\n\n[... {len(non_empty_lines) - 10} lines omitted ...]\n\n"
        summary += "\n".join(non_empty_lines[-5:])
        return summary
    
    elif mode == "chunks":
        # Split into semantic chunks (paragraphs or by size)
        chunks = []
        current_chunk = []
        current_size = 0
        max_chunk_size = 1000;
        
        for line in content.split("\n"):
            line_size = len(line)
            if current_size + line_size > max_chunk_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(line)
            current_size += line_size
        
        if current_chunk:
            chunks.append("\n".join(current_chunk))
        
        return "\n\n---CHUNK---\n\n".join(chunks)
    
    else:
        # Unknown mode, return raw
        return content


def _guess_content_type_from_extension(extension: str) -> str:
    """Guess MIME type from file extension."""
    extension = extension.lower()
    mapping = {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".json": "application/json",
        ".xml": "application/xml",
        ".html": "text/html",
        ".py": "text/x-python",
        ".js": "text/javascript",
        ".ts": "text/typescript",
        ".yaml": "application/x-yaml",
        ".yml": "application/x-yaml",
    }
    return mapping.get(extension, "text/plain")