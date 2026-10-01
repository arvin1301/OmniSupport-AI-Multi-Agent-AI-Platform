from voice_assistant.agents.rag.retriever import Retriever


def main():

    retriever = Retriever(
        top_k=3
    )

    print(
        "Stored chunks:",
        retriever.count()
    )

    query = (
        "What vector database does "
        "OmniSupport AI use?"
    )

    print("\nQuery:")
    print(query)

    results = retriever.retrieve(
        query
    )

    print(
        f"\nRetrieved results: {len(results)}"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {index} ---"
        )

        print(
            "ID:",
            result["id"]
        )

        print(
            "Source:",
            result["source"]
        )

        print(
            "Distance:",
            result["distance"]
        )

        print(
            "Text:",
            result["text"]
        )

    print("\n===== COMBINED CONTEXT =====\n")

    context = retriever.get_context(
        query
    )

    print(context)


if __name__ == "__main__":
    main()