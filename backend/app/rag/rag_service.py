"""
RAG Service

Responsibilities:
- Orchestrate document chunking
- Generate document embeddings
- Build the FAISS vector store
- Configure semantic retrieval
- Build LLM-ready context
- Provide a simple interface for indexing and retrieval
"""

from app.rag.chunker import TextChunk, TextChunker
from app.rag.context_builder import ContextBuilder
from app.rag.embedder import EmbeddingService
from app.rag.retriever import RetrievedChunk, Retriever
from app.rag.vector_store import FAISSVectorStore


class RAGService:
    """
    Orchestrates the complete document retrieval pipeline.
    """

    def __init__(
        self,
        chunker: TextChunker | None = None,
        embedder: EmbeddingService | None = None,
        context_builder: ContextBuilder | None = None,
    ) -> None:
        self.chunker = chunker or TextChunker()
        self.embedder = embedder or EmbeddingService()
        self.context_builder = (
            context_builder or ContextBuilder()
        )

        self.chunks: list[TextChunk] = []
        self.vector_store: FAISSVectorStore | None = None
        self.retriever: Retriever | None = None

    def index_document(
        self,
        text: str,
    ) -> int:
        """
        Chunk and index a document for semantic retrieval.

        Args:
            text: Document text to index.

        Returns:
            Number of chunks created.

        Raises:
            ValueError: If the document is empty.
        """

        if not text or not text.strip():
            raise ValueError(
                "Document text cannot be empty."
            )

        self.chunks = self.chunker.split_text(text)

        if not self.chunks:
            raise ValueError(
                "No chunks were generated from the document."
            )

        chunk_texts = [
            chunk.text
            for chunk in self.chunks
        ]

        embeddings = self.embedder.embed_texts(
            chunk_texts
        )

        if not embeddings:
            raise ValueError(
                "No embeddings were generated."
            )

        self.vector_store = FAISSVectorStore(
            dimension=len(embeddings[0])
        )

        self.vector_store.add_vectors(
            embeddings
        )

        self.retriever = Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store,
            chunks=self.chunks,
        )

        return len(self.chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.

        Args:
            query: Natural-language search query.
            top_k: Number of chunks to retrieve.

        Returns:
            Ranked list of RetrievedChunk objects.

        Raises:
            RuntimeError: If no document has been indexed.
        """

        if self.retriever is None:
            raise RuntimeError(
                "No document has been indexed. "
                "Call index_document() first."
            )

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

    def retrieve_context(
        self,
        query: str,
        top_k: int = 3,
    ) -> str:
        """
        Retrieve relevant chunks and build an
        LLM-ready context string.

        Args:
            query: Natural-language search query.
            top_k: Number of chunks to retrieve.

        Returns:
            Formatted context string.
        """

        retrieved_chunks = self.retrieve(
            query=query,
            top_k=top_k,
        )

        return self.context_builder.build(
            retrieved_chunks
        )

    @property
    def is_indexed(self) -> bool:
        """
        Return whether a document is currently indexed.
        """

        return self.retriever is not None

    @property
    def chunk_count(self) -> int:
        """
        Return the number of indexed chunks.
        """

        return len(self.chunks)