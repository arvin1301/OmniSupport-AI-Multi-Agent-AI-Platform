from pathlib import Path

import chromadb


class VectorStore:
    """
    ChromaDB-based vector store for the RAG system.
    """

    COLLECTION_NAME = "omnisupport_documents"

    def __init__(
        self,
        persist_directory: str = "data/vectorstore"
    ):

        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={
                    "description":
                    "OmniSupport AI RAG document collection"
                }
            )
        )

    # ========================================================
    # ADD DOCUMENTS
    # ========================================================

    def add_documents(
        self,
        chunks: list[dict],
        embeddings: list[list[float]]
    ) -> int:
        """
        Store document chunks and their embeddings.
        """

        if not chunks:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings "
                "must be the same."
            )

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            chunk_id = chunk.get(
                "id",
                f"chunk_{index}"
            )

            ids.append(chunk_id)

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                {
                    "source": chunk.get(
                        "source",
                        ""
                    ),
                    "chunk_index": chunk.get(
                        "chunk_index",
                        index
                    )
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(chunks)

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ) -> dict:
        """
        Search for the most relevant chunks.
        """

        if not query_embedding:
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": []
            }

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return {
            "documents": results.get(
                "documents",
                [[]]
            )[0],

            "metadatas": results.get(
                "metadatas",
                [[]]
            )[0],

            "distances": results.get(
                "distances",
                [[]]
            )[0],

            "ids": results.get(
                "ids",
                [[]]
            )[0]
        }

    # ========================================================
    # COUNT
    # ========================================================

    def count(self) -> int:
        """
        Return number of stored chunks.
        """

        return self.collection.count()

    # ========================================================
    # DELETE COLLECTION
    # ========================================================

    def clear(self):
        """
        Delete all stored RAG documents.
        """

        self.client.delete_collection(
            self.COLLECTION_NAME
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={
                    "description":
                    "OmniSupport AI RAG document collection"
                }
            )
        )