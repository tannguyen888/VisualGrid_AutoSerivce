"""
Purpose:
- Load knowledge documents from files/directories for ingestion.

Input:
- File paths or directory path containing manuals/DTC docs.

Output:
- Normalized document dictionaries for indexing.

Dependencies:
- pathlib

Future implementation:
- Add PDF parsing and metadata extraction pipeline.
"""

from __future__ import annotations

from pathlib import Path


def load_text_file(file_path: str) -> dict[str, str]:
    path = Path(file_path)
    return {
        "doc_id": path.stem,
        "title": path.stem.replace("_", " ").title(),
        "content": path.read_text(encoding="utf-8"),
        "source": path.suffix.replace(".", "") or "text",
    }


def load_documents_from_directory(directory_path: str) -> list[dict[str, str]]:
    root = Path(directory_path)
    docs: list[dict[str, str]] = []
    for file_path in root.rglob("*.txt"):
        docs.append(load_text_file(str(file_path)))
    return docs
