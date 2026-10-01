from voice_assistant.agents.rag.rag_agent import RAGAgent


def main():

    print("Initializing RAG Agent...")

    agent = RAGAgent(
        top_k=3
    )

    question = (
        "What vector database does "
        "the RAG system use?"
    )

    print("\nQuestion:")
    print(question)

    result = agent.ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print("-", source)


if __name__ == "__main__":
    main()