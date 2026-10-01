from groq import Groq

from ...config import (
    GROQ_API_KEY,
    RAG_LLM_MODEL,
    LLM_TEMPERATURE,
)

from .retriever import Retriever


class RAGAgent:

    def __init__(self):

        print("Initializing RAG Agent...")

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.retriever = Retriever(
            top_k=5
        )

        self.model = RAG_LLM_MODEL

    def answer(self, question: str):

        if not question or not question.strip():
            return {
                "answer": "",
                "sources": []
            }

        # ----------------------------------------
        # Retrieve relevant document chunks
        # ----------------------------------------

        results = self.retriever.retrieve(
            question
        )

        if not results:
            return {
                "answer": (
                    "I couldn't find relevant "
                    "information in the uploaded "
                    "documents."
                ),
                "sources": []
            }

        # ----------------------------------------
        # Build context
        # ----------------------------------------

        context_parts = []
        sources = []

        for result in results:

            source = result.get(
                "source",
                "Unknown"
            )

            text = result.get(
                "text",
                ""
            )

            context_parts.append(
                f"Source: {source}\n"
                f"{text}"
            )

            if source not in sources:
                sources.append(source)

        context = "\n\n---\n\n".join(
            context_parts
        )

        # ----------------------------------------
        # System prompt
        # ----------------------------------------

        system_prompt = """
You are the RAG agent for OmniSupport AI.

Your job is to answer questions using ONLY
the supplied document context.

Rules:

1. Use only information contained in the
   retrieved document context.

2. Do not invent facts.

3. Do not use outside knowledge.

4. If the answer cannot be found in the
   supplied context, clearly say that the
   information was not found in the uploaded
   documents.

5. Give a clear and useful answer.

6. Do not mention the retrieval process
   unless necessary.

7. Keep the answer reasonably concise.
"""

        # ----------------------------------------
        # User prompt
        # ----------------------------------------

        user_prompt = f"""
DOCUMENT CONTEXT:

{context}


QUESTION:

{question}


Answer the question using only the
document context.
"""

        # ----------------------------------------
        # Groq
        # ----------------------------------------

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=LLM_TEMPERATURE,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "sources": sources,
        }