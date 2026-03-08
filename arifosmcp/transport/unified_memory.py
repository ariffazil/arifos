"""
Unified Memory System for arifOS

Combines constitutional corpus (000_THEORY, APEX-THEORY) with 
Google Drive documents into a unified semantic search.

This module extends vector_memory to search across both sources.
"""

import os
import sys
from dataclasses import dataclass
from typing import Any

sys.path.insert(0, '/srv/arifOS')

from qdrant_client import QdrantClient

from arifosmcp.intelligence.embeddings import embed


@dataclass
class MemoryResult:
    """Unified memory result."""
    source: str  # 'constitutional' or 'gdrive'
    path: str
    content: str
    score: float
    metadata: dict[str, Any]


class UnifiedMemory:
    """
    Unified semantic memory across constitutional corpus and Google Drive.
    
    Collections searched:
    - arifos_constitutional: Core constitutional documents
    - gdrive_documents: Google Drive synced documents (if available)
    """
    
    def __init__(self, qdrant_url: str = None):
        self.qdrant_url = qdrant_url or os.getenv('QDRANT_URL', 'http://qdrant:6333')
        self.client = QdrantClient(url=self.qdrant_url)
        
        self.collections = {
            'constitutional': 'arifos_constitutional',
            'gdrive': 'gdrive_documents'
        }
    
    def _collection_exists(self, name: str) -> bool:
        """Check if a collection exists."""
        try:
            collections = self.client.get_collections()
            return any(c.name == name for c in collections.collections)
        except:
            return False
    
    def search_constitutional(
        self, 
        query: str, 
        top_k: int = 5,
        source_filter: str = None
    ) -> list[MemoryResult]:
        """Search constitutional corpus."""
        collection = self.collections['constitutional']
        
        if not self._collection_exists(collection):
            return []
        
        # Generate embedding
        query_vector = embed(query)
        
        # Search with payload filter if source_filter provided
        results = self.client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        ).points
        
        memories = []
        for r in results:
            payload = r.payload or {}
            source = payload.get('source', 'unknown')
            
            # Apply source filter
            if source_filter and source_filter not in source:
                continue
            
            memories.append(MemoryResult(
                source='constitutional',
                path=f"{source}/{payload.get('file_name', 'unknown')}",
                content=payload.get('content', '')[:800],
                score=r.score,
                metadata={
                    'jaccard_score': r.score,
                    'collection': collection,
                    **payload
                }
            ))
        
        return memories
    
    def search_gdrive(
        self, 
        query: str, 
        top_k: int = 5
    ) -> list[MemoryResult]:
        """Search Google Drive documents."""
        collection = self.collections['gdrive']
        
        if not self._collection_exists(collection):
            return []
        
        # Generate embedding
        query_vector = embed(query)
        
        # Search
        results = self.client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        ).points
        
        memories = []
        for r in results:
            payload = r.payload or {}
            
            memories.append(MemoryResult(
                source='gdrive',
                path=f"gdrive/{payload.get('file_name', 'unknown')}",
                content=payload.get('content_preview', '')[:800],
                score=r.score,
                metadata={
                    'jaccard_score': r.score,
                    'file_id': payload.get('file_id'),
                    'web_view_link': payload.get('web_view_link'),
                    'mime_type': payload.get('mime_type'),
                    'modified_time': payload.get('modified_time'),
                    'account': payload.get('account'),
                    'collection': collection,
                    **payload
                }
            ))
        
        return memories
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        domain: str = "all"
    ) -> list[MemoryResult]:
        """
        Unified search across all memory sources.
        
        Args:
            query: Search query
            top_k: Number of results per source
            domain: 'all', 'canon', 'manifesto', 'gdrive'
        
        Returns:
            Merged and ranked results from all sources
        """
        all_results = []
        
        # Search constitutional based on domain
        if domain in ('all', 'canon', 'manifesto'):
            source_filter = None
            if domain == 'canon':
                source_filter = '000_THEORY'
            elif domain == 'manifesto':
                source_filter = 'APEX-THEORY'
            
            constitutional = self.search_constitutional(
                query, top_k=top_k, source_filter=source_filter
            )
            all_results.extend(constitutional)
        
        # Search Google Drive
        if domain in ('all', 'gdrive', 'docs'):
            gdrive = self.search_gdrive(query, top_k=top_k)
            all_results.extend(gdrive)
        
        # Sort by score (descending)
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        # Return top results
        return all_results[:top_k]
    
    def get_stats(self) -> dict[str, Any]:
        """Get memory system statistics."""
        stats = {
            'sources': {}
        }
        
        for name, collection in self.collections.items():
            if self._collection_exists(collection):
                count = self.client.count(collection)
                stats['sources'][name] = {
                    'available': True,
                    'collection': collection,
                    'document_count': count.count
                }
            else:
                stats['sources'][name] = {
                    'available': False,
                    'collection': collection,
                    'document_count': 0
                }
        
        stats['total_documents'] = sum(
            s['document_count'] for s in stats['sources'].values()
        )
        
        return stats


# Singleton instance
_unified_memory = None


def get_unified_memory() -> UnifiedMemory:
    """Get or create unified memory instance."""
    global _unified_memory
    if _unified_memory is None:
        _unified_memory = UnifiedMemory()
    return _unified_memory


# For direct testing
if __name__ == '__main__':
    import json
    
    memory = get_unified_memory()
    
    # Show stats
    stats = memory.get_stats()
    print("Memory System Stats:")
    print(json.dumps(stats, indent=2))
    
    # Interactive search
    print("\n" + "="*60)
    print("Unified Memory Search")
    print("="*60)
    
    while True:
        query = input("\nQuery (or 'quit'): ").strip()
        if query.lower() in ('quit', 'exit', 'q'):
            break
        
        domain = input("Domain [all/canon/gdrive]: ").strip() or "all"
        
        results = memory.search(query, top_k=5, domain=domain)
        
        print(f"\nFound {len(results)} results:")
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r.path} (score: {r.score:.4f})")
            print(f"    Source: {r.source}")
            print(f"    Preview: {r.content[:150]}...")
            if r.source == 'gdrive':
                print(f"    Link: {r.metadata.get('web_view_link', 'N/A')}")
