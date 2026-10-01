from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class Retriever:
    """
    Retrieves relevant document chunks from ChromaDB.
    """

    def __init__(
        self,
        top_k: int = 5
    ):
        self.top_k = top_k

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        top_k: int | None = None
    ) -> list[dict]:
        """
        Retrieve the most relevant document chunks.
        """

        if not query or not query.strip():
            return []

        if top_k is None:
            top_k = self.top_k

        query_embedding = (
            self.embedding_model.embed_query(
                query
            )
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        documents = results.get(
            "documents",
            []
        )

        metadatas = results.get(
            "metadatas",
            []
        )

        distances = results.get(
            "distances",
            []
        )

        ids = results.get(
            "ids",
            []
        )

        retrieved = []

        for index, document in enumerate(
            documents
        ):

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            chunk_id = (
                ids[index]
                if index < len(ids)
                else None
            )

            retrieved.append(
                {
                    "id": chunk_id,
                    "text": document,
                    "source": metadata.get(
                        "source",
                        ""
                    ),
                    "chunk_index": metadata.get(
                        "chunk_index",
                        index
                    ),
                    "distance": distance,
                }
            )

        return retrieved

    # ========================================================
    # CONTEXT
    # ========================================================

    def get_context(
        self,
        query: str,
        top_k: int | None = None
    ) -> str:
        """
        Build a context string from retrieved chunks.
        """

        results = self.retrieve(
            query,
            top_k
        )

        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(
            results,
            start=1
        ):

            source = result["source"]

            context_parts.append(
                f"[Source {index}: {source}]\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )

    # ========================================================
    # DATABASE STATUS
    # ========================================================

    def count(self) -> int:
        """
        Return the number of chunks in the vector store.
        """

        return self.vector_store.count()