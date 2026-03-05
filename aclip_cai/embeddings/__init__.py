from sentence_transformers import SentenceTransformer
import os
import logging

logger = logging.getLogger(__name__)
_model = None

def get_embedder():
    global _model
    if _model is None:
        # Default model name
        model_name = "BAAI/bge-small-en-v1.5"
        # Check if baked-in model exists
        baked_in_path = "/app/models/bge/bge-arifOS"
        if os.path.exists(baked_in_path):
            model_name = baked_in_path
            logger.info(f"Using baked-in BGE model at {baked_in_path}")
        else:
            logger.info(f"Downloading BGE model: {model_name}")
        
        _model = SentenceTransformer(model_name)
    return _model

def embed(text: str) -> list[float]:
    model = get_embedder()
    return model.encode(text).tolist()
