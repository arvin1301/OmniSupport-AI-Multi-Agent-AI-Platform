from voice_assistant.agents.rag.document_loader import (
    DocumentLoader
)

from voice_assistant.agents.rag.chunker import (
    TextChunker
)

from voice_assistant.agents.rag.embeddings import (
    EmbeddingModel
)

from voice_assistant.agents.rag.vector_store import (
    VectorStore
)


def main():

    # --------------------------------------------------------
    # 1. Load document
    # --------------------------------------------------------

    loader = DocumentLoader()

    text = loader.load(
        "data/documents/test.txt"
    )

    print(
        f"Loaded characters: {len(text)}"
    )

    # --------------------------------------------------------
    # 2. Create chunks
    # --------------------------------------------------------

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = chunker.create_chunks(
        text,
        "test.txt"
    )

    print(
        f"Created chunks: {len(chunks)}"
    )

    # --------------------------------------------------------
    # 3. Create embeddings
    # --------------------------------------------------------

    embedding_model = EmbeddingModel()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = (
        embedding_model.embed_documents(
            texts
        )
    )

    print(
        f"Created embeddings: {len(embeddings)}"
    )

    print(
        f"Embedding dimension: "
        f"{len(embeddings[0])}"
    )

    # --------------------------------------------------------
    # 4. Store in ChromaDB
    # --------------------------------------------------------

    vector_store = VectorStore()

    added = vector_store.add_documents(
        chunks,
        embeddings
    )

    print(
        f"Documents stored: {added}"
    )

    print(
        f"Total vectors in database: "
        f"{vector_store.count()}"
    )

    # --------------------------------------------------------
    # 5. Test semantic search
    # --------------------------------------------------------

    query = (
        "What vector database does "
        "the RAG system use?"
    )

    query_embedding = (
        embedding_model.embed_query(
            query
        )
    )

    results = vector_store.search(
        query_embedding,
        top_k=3
    )

    print("\nQuery:")
    print(query)

    print("\nSearch results:")

    for index, document in enumerate(
        results["documents"]
    ):

        print(
            f"\n--- Result {index + 1} ---"
        )

        print(
            document
        )

        print(
            "Source:",
            results["metadatas"][index]
        )

        print(
            "Distance:",
            results["distances"][index]
        )


if __name__ == "__main__":
    main()