from pathlib import Path

import pymupdf
from docx import Document


class DocumentLoader:
    """
    Loads supported documents and converts them into plain text.

    Supported formats:
        - PDF
        - TXT
        - DOCX
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".docx",
    }

    def load(self, file_path: str) -> str:
        """
        Load a document and return its text.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document type: {extension}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".txt":
            return self._load_txt(path)

        if extension == ".docx":
            return self._load_docx(path)

        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    # ========================================================
    # PDF
    # ========================================================

    def _load_pdf(self, path: Path) -> str:
        """
        Extract text from a PDF file.
        """

        pages = []

        with pymupdf.open(path) as document:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                text = page.get_text().strip()

                if text:
                    pages.append(
                        f"[Page {page_number}]\n{text}"
                    )

        return "\n\n".join(pages)

    # ========================================================
    # TXT
    # ========================================================

    def _load_txt(self, path: Path) -> str:
        """
        Load a plain text file.
        """

        return path.read_text(
            encoding="utf-8"
        ).strip()

    # ========================================================
    # DOCX
    # ========================================================

    def _load_docx(self, path: Path) -> str:
        """
        Extract text from a DOCX file.
        """

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)