"""
RAG Context Builder

Responsibilities:
- Convert retrieved chunks into LLM-ready context
- Preserve source chunk information
- Keep context formatting deterministic
- Prevent empty or meaningless context from being passed downstream
"""

from app.rag.retriever import RetrievedChunk


class ContextBuilder:
    """
    Builds a structured context string from retrieved chunks.
    """

    def build(
        self,
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        """
        Build an LLM-ready context string.

        Args:
            retrieved_chunks:
                Ranked chunks returned by the retriever.

        Returns:
            Formatted context string.

        Raises:
            ValueError:
                If no retrieved chunks are provided.
        """

        if not retrieved_chunks:
            raise ValueError(
                "Cannot build context from empty retrieval results."
            )

        context_sections: list[str] = []

        for position, result in enumerate(
            retrieved_chunks,
            start=1,
        ):
            text = result.chunk.text.strip()

            if not text:
                continue

            context_sections.append(
                (
                    f"[Context {position}]\n"
                    f"{text}"
                )
            )

        if not context_sections:
            raise ValueError(
                "Retrieved chunks contain no usable text."
            )

        return "\n\n".join(context_sections)