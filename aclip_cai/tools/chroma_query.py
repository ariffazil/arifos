"""
aclip_cai/tools/chroma_query.py — Chroma Vector Store Query

ACLIP Console tool: lets AI agents query persistent memory
at C:\\Users\\User\\chroma_memory without re-reading files.
"""

from __future__ import annotations

import os
from typing import Any, Optional

_DEFAULT_CHROMA_PATH = r"C:\Users\User\chroma_memory"


def query_memory(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    chroma_path: Optional[str] = None,
) -> dict[str, Any]:
    """Query the Chroma vector store with a natural language query."""
    path = chroma_path or os.environ.get("ARIFOS_CHROMA_PATH", _DEFAULT_CHROMA_PATH)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=path)
    except ImportError:
        return {
            "status": "VOID",
            "error": "chromadb not installed",
            "hint": "uv pip install chromadb",
        }
    except Exception as e:
        return {"status": "VOID", "error": f"Failed to open Chroma at {path}: {e}"}

    try:
        col = client.get_collection(collection)
    except Exception:
        available = [c.name for c in client.list_collections()]
        return {
            "status": "PARTIAL",
            "error": f"Collection '{collection}' not found",
            "available_collections": available,
            "hint": f"Use one of: {available}" if available else "No collections found",
        }

    try:
        results = col.query(query_texts=[query], n_results=min(top_k, col.count()))
    except Exception as e:
        return {"status": "VOID", "error": f"Query failed: {e}"}

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    hits = [
        {
            "id": ids[i] if i < len(ids) else f"doc_{i}",
            "content": doc,
            "distance": round(dists[i], 4) if i < len(dists) else None,
            "metadata": metas[i] if i < len(metas) else {},
        }
        for i, doc in enumerate(docs)
    ]

    return {
        "status": "SEAL",
        "collection": collection,
        "query": query,
        "count": len(hits),
        "results": hits,
    }


def list_collections(chroma_path: Optional[str] = None) -> dict[str, Any]:
    """List all available Chroma collections and their document counts."""
    path = chroma_path or os.environ.get("ARIFOS_CHROMA_PATH", _DEFAULT_CHROMA_PATH)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=path)
    except ImportError:
        return {
            "status": "VOID",
            "error": "chromadb not installed",
            "hint": "uv pip install chromadb",
        }
    except Exception as e:
        return {"status": "VOID", "error": str(e)}

    try:
        cols = client.list_collections()
        return {
            "status": "SEAL",
            "chroma_path": path,
            "count": len(cols),
            "collections": [{"name": c.name, "documents": c.count()} for c in cols],
        }
    except Exception as e:
        return {"status": "VOID", "error": str(e)}
