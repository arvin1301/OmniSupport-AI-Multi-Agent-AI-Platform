from pathlib import Path

from .document_loader import DocumentLoader
from .chunker import TextChunker
from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class RAGIngestion:

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100,
    ):
        self.loader = DocumentLoader()

        self.chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def ingest(self, file_path: str):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        print(f"\n📄 Loading: {file_path.name}")

        # -----------------------------------------
        # 1. Load document
        # -----------------------------------------

        text = self.loader.load(
            str(file_path)
        )

        if not text.strip():
            raise ValueError(
                "No text could be extracted from document."
            )

        print(
            f"📖 Extracted {len(text)} characters"
        )

        # -----------------------------------------
        # 2. Create chunks
        # -----------------------------------------

        chunks = self.chunker.create_chunks(
            text,
            file_path.name,
        )

        print(
            f"✂️ Created {len(chunks)} chunks"
        )

        # -----------------------------------------
        # 3. Generate embeddings
        # -----------------------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_model.embed_documents(
                texts
            )
        )

        print(
            f"🧠 Generated {len(embeddings)} embeddings"
        )

        # -----------------------------------------
        # 4. Store in ChromaDB
        # -----------------------------------------

        self.vector_store.add_documents(
            chunks,
            embeddings,
        )

        print(
            "✅ Document successfully added to ChromaDB"
        )

        return {
            "file": file_path.name,
            "characters": len(text),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
        }