"""
Embedding Service

Responsibilities:
- Load the Sentence Transformer embedding model
- Convert text into dense numerical vectors
- Provide embeddings for documents and queries
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates semantic embeddings using Sentence Transformers.
    """

    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector as a list of floats.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors.
        """

        if not texts:
            return []

        cleaned_texts = [
            text.strip()
            for text in texts
            if text and text.strip()
        ]

        if not cleaned_texts:
            return []

        embeddings = self.model.encode(
            cleaned_texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()