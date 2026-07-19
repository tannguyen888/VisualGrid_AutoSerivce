"""
Purpose:
- PDF extractor for repair manuals and service documents.

Input:
- PDF payload as bytes.

Output:
- Extracted plain text preserving page boundaries.

Responsibilities:
- Read each PDF page and collect text blocks.
- Return combined text for parser stage.

TODO implementation notes:
- Add table/image extraction output channels.
- Add OCR fallback for scanned documents.
"""

from __future__ import annotations


class PdfExtractor:
    def extract(self, pdf_bytes: bytes) -> str:
        if not pdf_bytes:
            return ""

        try:
            import fitz  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("PyMuPDF is required: pip install pymupdf") from exc

        page_texts: list[str] = []
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            for page_index, page in enumerate(document, start=1):
                text = page.get_text("text").strip()
                page_texts.append(f"[PAGE {page_index}]\n{text}")
        return "\n\n".join(page_texts)
