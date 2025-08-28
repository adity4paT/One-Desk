from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore

from app.config import settings


class Embeddings:
    """Text embedding service using SentenceTransformer with Redis caching."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.embedding_model)
        self._dim = getattr(self.model, "get_sentence_embedding_dimension", lambda: None)() or 0

    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.zeros((0, self._dim), dtype=np.float32) if self._dim else np.zeros((0, 0), dtype=np.float32)

        # Generate embeddings for all texts
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        
        return embeddings

    def embed_one(self, text: str) -> np.ndarray:
        """Embed a single text string."""
        return self.embed([text])[0]


# Global embedding instance
embeddings = Embeddings()


