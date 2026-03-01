"""
ACLIP_CAI Embeddings Module
BGE Integration for Vector Search and Semantic Memory

This module provides:
- Text → Vector conversion (BGE model)
- Semantic similarity search
- Integration with Qdrant vector database

No external HTTP calls - everything in-process.
"""

import os
import logging
from typing import List, Union, Optional
import numpy as np

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available, embeddings disabled")

logger = logging.getLogger(__name__)

class BGEEmbedder:
    """
    BGE Embedding Engine for aclip_cai
    
    Loads BGE model and provides text-to-vector conversion.
    768 dimensions, optimized for semantic search.
    """
    
    _instance = None  # Singleton pattern
    
    def __new__(cls, model_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_path: Optional[str] = None):
        if self._initialized:
            return
            
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.model = None
            self.dimensions = 0
            self._initialized = True
            return
        
        # Default path: bundled with aclip_cai
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(__file__), 
                "bge-arifOS"
            )
        
        self.model_path = model_path
        self.dimensions = 768  # BGE-base dimension
        self.model = None
        
        try:
            logger.info(f"Loading BGE model from {model_path}")
            self.model = SentenceTransformer(model_path)
            logger.info(f"✅ BGE model loaded: {self.dimensions} dimensions")
            self._initialized = True
        except Exception as e:
            logger.error(f"❌ Failed to load BGE model: {e}")
            self.model = None
    
    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Convert text to vector(s)
        
        Args:
            text: String or list of strings to embed
            
        Returns:
            Vector (768 dims) or list of vectors
        """
        if self.model is None:
            logger.error("BGE model not loaded, returning zeros")
            if isinstance(text, str):
                return [0.0] * self.dimensions
            return [[0.0] * self.dimensions for _ in text]
        
        try:
            # Encode with normalization (cosine similarity ready)
            embeddings = self.model.encode(text, normalize_embeddings=True)
            
            # Convert to Python lists
            if isinstance(text, str):
                return embeddings.tolist()
            return [e.tolist() for e in embeddings]
            
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            if isinstance(text, str):
                return [0.0] * self.dimensions
            return [[0.0] * self.dimensions for _ in text]
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        Returns: 0.0 to 1.0 (1.0 = identical meaning)
        """
        if self.model is None:
            return 0.0
        
        try:
            vec1 = np.array(self.encode(text1))
            vec2 = np.array(self.encode(text2))
            
            # Cosine similarity (already normalized, so just dot product)
            similarity = np.dot(vec1, vec2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0

# Global embedder instance (lazy loaded)
_embedder: Optional[BGEEmbedder] = None

def get_embedder() -> BGEEmbedder:
    """Get or create the global BGE embedder instance"""
    global _embedder
    if _embedder is None:
        _embedder = BGEEmbedder()
    return _embedder

def embed(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    """Quick access: text → vector"""
    return get_embedder().encode(text)

def similarity(text1: str, text2: str) -> float:
    """Quick access: semantic similarity"""
    return get_embedder().similarity(text1, text2)

__all__ = ['BGEEmbedder', 'get_embedder', 'embed', 'similarity']
