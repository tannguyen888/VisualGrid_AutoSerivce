"""
Purpose:
- Backward-compatible PDF source adapter.

Input:
- Document URL.

Output:
- PDF bytes.

Responsibilities:
- Delegate PDF download to document source workflow.
- Keep compatibility with earlier pipeline imports.

TODO implementation notes:
- Remove adapter when all callers migrate to document_source.
"""

from __future__ import annotations

from sources.document_source import DocumentSource


class PdfSource(DocumentSource):
    def fetch(self, url: str) -> bytes:
        payload = super().fetch(url=url)
        return payload.get("content", b"")
