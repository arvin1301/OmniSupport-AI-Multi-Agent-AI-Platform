from voice_assistant.agents.rag.rag_agent import RAGAgent


def main():

    agent = RAGAgent()

    questions = [
        "What are the benefits of ChatGPT for businesses?",
        "How can ChatGPT help e-commerce businesses?",
        "What industries are discussed in the document?",
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print("QUESTION:")
        print(question)
        print("=" * 70)

        result = agent.answer(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(f"- {source}")


if __name__ == "__main__":
    main()