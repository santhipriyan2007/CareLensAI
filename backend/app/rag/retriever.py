"""
RAG Retriever

Responsibilities:
- Convert user queries into embeddings
- Search the FAISS vector store
- Map vector indices back to document chunks
- Return ranked, structured retrieval results
"""

from dataclasses import dataclass

from app.rag.chunker import TextChunk
from app.rag.embedder import EmbeddingService
from app.rag.vector_store import FAISSVectorStore


@dataclass
class RetrievedChunk:
    """
    Represents a retrieved document chunk together with
    its similarity score.
    """

    chunk: TextChunk
    score: float


class Retriever:
    """
    Performs semantic retrieval over indexed document chunks.
    """

    def __init__(
        self,
        embedder: EmbeddingService,
        vector_store: FAISSVectorStore,
        chunks: list[TextChunk],
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.chunks = chunks

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.

        Args:
            query: User's natural-language question.
            top_k: Maximum number of chunks to retrieve.

        Returns:
            Ranked list of RetrievedChunk objects.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not self.chunks:
            return []

        query_embedding = self.embedder.embed_text(
            query
        )

        indices, scores = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        results: list[RetrievedChunk] = []

        for index, score in zip(indices, scores):
            if index < 0 or index >= len(self.chunks):
                continue

            results.append(
                RetrievedChunk(
                    chunk=self.chunks[index],
                    score=float(score),
                )
            )

        return results