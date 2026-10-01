from voice_assistant.agents.rag.document_loader import DocumentLoader
from voice_assistant.agents.rag.chunker import TextChunker


def main():

    loader = DocumentLoader()

    text = loader.load(
        "data/documents/test.txt"
    )

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = chunker.create_chunks(
        text,
        "test.txt"
    )

    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks:

        print(
            f"\n--- {chunk['id']} ---"
        )

        print(chunk["text"])


if __name__ == "__main__":
    main()