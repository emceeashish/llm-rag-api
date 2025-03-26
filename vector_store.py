"""
vector_store.py

Implements a simple FAISS-based vector store for our function metadata.
We'll embed each function's description and store them. 
Later, when a user prompt comes in, we'll embed it and retrieve the closest function.
"""

import faiss
import numpy as np
from embeddings import get_embedding
from function_registry import FUNCTIONS_METADATA

class FunctionVectorStore:
    def __init__(self):
        # Our FAISS index
        self.index = None
        # We'll store function info in parallel arrays (or we can store them in a single list)
        self.function_info = []
        # Build the index right away so it's ready to go.
        self._build_index()

    def _build_index(self):
        # We'll gather embeddings for each function's description.
        embeddings = []
        for func_data in FUNCTIONS_METADATA:
            emb = get_embedding(func_data["description"])
            embeddings.append(emb)
            self.function_info.append(func_data)

        # Convert them into a float32 matrix, which FAISS wants
        embeddings_matrix = np.vstack(embeddings).astype("float32")

        # Dimension is the length of each embedding
        dimension = embeddings_matrix.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_matrix)

    def search(self, query: str, top_k: int = 1):
        """
        Given a user query, find the top-k matching functions from our store.
        Returns the best match (or a list if top_k > 1).
        """
        # 1) Embed the user's query
        query_emb = get_embedding(query)
        query_emb = np.array([query_emb]).astype("float32")

        # 2) Perform the search in FAISS
        distances, indices = self.index.search(query_emb, top_k)

        # 3) If we only need one, return the single best match
        if top_k == 1:
            best_idx = indices[0][0]
            return self.function_info[best_idx]
        else:
            # Return a list of matches
            matches = []
            for i in range(top_k):
                idx = indices[0][i]
                matches.append(self.function_info[idx])
            return matches
