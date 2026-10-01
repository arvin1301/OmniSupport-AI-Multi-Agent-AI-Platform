from voice_assistant.agents.rag.retriever import Retriever


def main():

    retriever = Retriever(top_k=5)

    questions = [
        "What is the impact of ChatGPT on business sectors?",
        "What are the benefits of ChatGPT for businesses?",
        "What challenges are associated with using ChatGPT?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION:")
        print(question)
        print("=" * 70)

        results = retriever.retrieve(question)

        print(f"\nRetrieved documents: {len(results)}")

        for i, result in enumerate(results, start=1):

            print(f"\n--- Result {i} ---")

            print(
                "Source:",
                result.get("source", "Unknown")
            )

            print(
                "Distance:",
                result.get("distance", "N/A")
            )

            print("\nText:")

            print(
                result["text"][:1000]
            )


if __name__ == "__main__":
    main()