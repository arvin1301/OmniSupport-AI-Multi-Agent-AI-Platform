from voice_assistant.agents.rag.embeddings import EmbeddingModel


def main():

    embedding_model = EmbeddingModel()

    text = (
        "The RAG system uses ChromaDB "
        "for vector storage."
    )

    vector = embedding_model.embed_text(
        text
    )

    print(
        f"Embedding dimension: {len(vector)}"
    )

    print(
        "First 10 values:"
    )

    print(
        vector[:10]
    )

    query_vector = embedding_model.embed_query(
        "What vector database does the RAG system use?"
    )

    print(
        f"Query embedding dimension: "
        f"{len(query_vector)}"
    )


if __name__ == "__main__":
    main()