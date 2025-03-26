"""
embeddings.py

This module handles how we generate embeddings. 
Below, I'm using sentence-transformers locally for embeddings, 
but you could swap it for the Together.ai embeddings API if you prefer.
"""

from sentence_transformers import SentenceTransformer

# Just picking a small, fast model. Switch to something else if you want more accuracy.
_EMBEDDER = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Returns a vector (list[float]) representing the semantic embedding 
    of the given text using our local sentence-transformers model.
    """
    return _EMBEDDER.encode(text)
