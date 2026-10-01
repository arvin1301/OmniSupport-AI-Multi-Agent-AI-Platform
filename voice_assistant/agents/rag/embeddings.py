from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Creates vector embeddings for RAG documents and queries.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        print(
            f"Loading embedding model: {self.MODEL_NAME}"
        )

        self.model = SentenceTransformer(
            self.MODEL_NAME
        )

        print("Embedding model loaded.")

    # ========================================================
    # SINGLE TEXT
    # ========================================================

    def embed_text(self, text: str) -> list[float]:
        """
        Convert a single text into an embedding vector.
        """

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    # ========================================================
    # MULTIPLE TEXTS
    # ========================================================

    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """
        Convert multiple text chunks into embeddings.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    # ========================================================
    # QUERY
    # ========================================================

    def embed_query(
        self,
        query: str
    ) -> list[float]:
        """
        Convert a user question into an embedding.
        """

        return self.embed_text(query)

    # ========================================================
    # DIMENSION
    # ========================================================

    def dimension(self) -> int:
        """
        Return the embedding vector dimension.
        """

        return self.model.get_sentence_embedding_dimension()