"""
aclip_cai/tools/chroma_query.py — Chroma Vector Store Query

ACLIP Console tool: lets AI agents query persistent memory
at C:\\Users\\User\\chroma_memory without re-reading files.
"""

from __future__ import annotations

import os
from typing import Any

from aclip_cai.tools.aclip_base import ok, partial, void

_DEFAULT_CHROMA_PATH = os.path.join(os.path.expanduser("~"), "chroma_memory")


def query_memory(
    query: str,
    collection: str = "default",
    n_results: int = 5,
    where: dict[str, Any] | None = None,
    include_embeddings: bool = False,
    chroma_path: str | None = None,
) -> dict[str, Any]:
    """Query the Chroma vector store with a natural language query."""
    path = chroma_path or os.environ.get("ARIFOS_CHROMA_PATH", _DEFAULT_CHROMA_PATH)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=path)
    except ImportError:
        return void("chromadb not installed", hint="uv pip install chromadb")
    except Exception as e:
        return void(f"Failed to open Chroma at {path}: {e}")

    try:
        col = client.get_collection(collection)
    except Exception:
        available = [c.name for c in client.list_collections()]
        return partial(
            {"available_collections": available},
            error=f"Collection '{collection}' not found",
            hint=f"Use one of: {available}" if available else "No collections found",
        )

    try:
        include = ["metadatas", "documents", "distances"]
        if include_embeddings:
            include.append("embeddings")

        results = col.query(
            query_texts=[query],
            n_results=min(n_results, col.count()) if col.count() > 0 else n_results,
            where=where,
            include=include,
        )
    except Exception as e:
        return void(f"Query failed: {e}")

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]
    embs = results.get("embeddings", [[]])[0] if include_embeddings else []

    hits = []
    for i, doc in enumerate(docs):
        hit = {
            "id": ids[i] if i < len(ids) else f"doc_{i}",
            "document": doc,
            "distance": round(dists[i], 4) if i < len(dists) else None,
            "metadata": metas[i] if i < len(metas) else {},
        }
        if include_embeddings and i < len(embs):
            hit["embedding"] = embs[i]
        hits.append(hit)

    return ok(
        {
            "collection": collection,
            "query": query,
            "count": len(hits),
            "results": hits,
        }
    )


def list_collections(chroma_path: str | None = None) -> dict[str, Any]:
    """List all available Chroma collections and their document counts."""
    path = chroma_path or os.environ.get("ARIFOS_CHROMA_PATH", _DEFAULT_CHROMA_PATH)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=path)
    except ImportError:
        return void("chromadb not installed", hint="uv pip install chromadb")
    except Exception as e:
        return void(str(e))

    try:
        cols = client.list_collections()
        return ok(
            {
                "chroma_path": path,
                "count": len(cols),
                "collections": [{"name": c.name, "documents": c.count()} for c in cols],
            }
        )
    except Exception as e:
        return void(str(e))
