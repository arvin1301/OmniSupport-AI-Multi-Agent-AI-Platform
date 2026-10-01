import re


class TextChunker:
    """
    Splits documents into overlapping text chunks.

    Overlap helps preserve context between neighboring chunks.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120,
    ):

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ========================================================
    # CLEAN TEXT
    # ========================================================

    def _clean_text(self, text: str) -> str:
        """
        Normalize unnecessary whitespace.
        """

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    # ========================================================
    # CHUNK
    # ========================================================

    def split_text(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.
        """

        if not text or not text.strip():
            return []

        text = self._clean_text(text)

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = min(
                start + self.chunk_size,
                text_length
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            next_start = end - self.chunk_overlap

            # Try to break at a natural boundary.
            boundary_positions = [
                text.rfind("\n\n", start, end),
                text.rfind(". ", start, end),
                text.rfind(" ", start, end),
            ]

            valid_boundaries = [
                position
                for position in boundary_positions
                if position > start
            ]

            if valid_boundaries:

                boundary = max(
                    valid_boundaries
                )

                start = boundary + 1

            else:

                start = next_start

        return chunks

    # ========================================================
    # CHUNK WITH METADATA
    # ========================================================

    def create_chunks(
        self,
        text: str,
        source: str = "",
    ) -> list[dict]:
        """
        Return chunks together with metadata.
        """

        chunks = self.split_text(text)

        results = []

        for index, chunk in enumerate(
            chunks
        ):

            results.append(
                {
                    "id": f"chunk_{index}",
                    "text": chunk,
                    "source": source,
                    "chunk_index": index,
                }
            )

        return results