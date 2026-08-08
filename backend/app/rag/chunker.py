"""
Text Chunking Module

Responsibilities:
- Split large medical report text into smaller chunks
- Preserve contextual overlap between chunks
- Provide clean chunk metadata for downstream RAG components
"""

from dataclasses import dataclass


@dataclass
class TextChunk:
    """
    Represents a single chunk of document text.
    """

    chunk_id: int
    text: str


class TextChunker:
    """
    Splits large text into overlapping chunks.

    The chunker works at the word level rather than blindly
    cutting characters in the middle of medical terms.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> list[TextChunk]:
        """
        Split text into overlapping chunks.

        Args:
            text: Raw OCR/document text.

        Returns:
            A list of TextChunk objects.
        """

        if not text or not text.strip():
            return []

        words = text.split()

        chunks: list[TextChunk] = []

        start = 0
        chunk_id = 0

        step = self.chunk_size - self.chunk_overlap

        while start < len(words):
            end = min(start + self.chunk_size, len(words))

            chunk_text = " ".join(words[start:end]).strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                    )
                )

            chunk_id += 1
            start += step

        return chunks