"""
FAISS Vector Store

Responsibilities:
- Create and manage a FAISS similarity index
- Store embedding vectors
- Perform similarity searches
- Return matching vector indices and similarity scores
"""

from __future__ import annotations

from typing import Sequence

import faiss
import numpy as np


class FAISSVectorStore:
    """
    Lightweight FAISS-based vector store.

    The store uses normalized vectors with an inner-product
    index, which allows inner product to represent cosine
    similarity.
    """

    def __init__(self, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be greater than zero.")

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)

    @property
    def size(self) -> int:
        """
        Return the number of vectors currently stored.
        """

        return self.index.ntotal

    def add_vectors(
        self,
        vectors: Sequence[Sequence[float]],
    ) -> None:
        """
        Add embedding vectors to the FAISS index.

        Args:
            vectors: Collection of embedding vectors.
        """

        if not vectors:
            return

        array = np.asarray(
            vectors,
            dtype=np.float32,
        )

        if array.ndim != 2:
            raise ValueError(
                "Vectors must be a 2-dimensional collection."
            )

        if array.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with dimension "
                f"{self.dimension}, but received "
                f"{array.shape[1]}."
            )

        faiss.normalize_L2(array)

        self.index.add(array)

    def search(
        self,
        query_vector: Sequence[float],
        top_k: int = 3,
    ) -> tuple[list[int], list[float]]:
        """
        Search for the most similar vectors.

        Args:
            query_vector: Embedding vector for the query.
            top_k: Maximum number of results to return.

        Returns:
            Tuple containing:
            - matching vector indices
            - similarity scores
        """

        if not query_vector:
            raise ValueError("query_vector cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if self.size == 0:
            return [], []

        query_array = np.asarray(
            [query_vector],
            dtype=np.float32,
        )

        if query_array.shape[1] != self.dimension:
            raise ValueError(
                f"Expected query vector with dimension "
                f"{self.dimension}, but received "
                f"{query_array.shape[1]}."
            )

        faiss.normalize_L2(query_array)

        k = min(top_k, self.size)

        scores, indices = self.index.search(
            query_array,
            k,
        )

        return (
            indices[0].tolist(),
            scores[0].tolist(),
        )