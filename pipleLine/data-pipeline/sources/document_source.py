"""
Purpose:
- Document source connector for downloading manuals, diagrams, and document artifacts.

Input:
- Document URL or provider document identifier.

Output:
- Binary file content and minimal metadata.

Responsibilities:
- Download file content with optional authentication.
- Return bytes to extractor/storage layers.

TODO implementation notes:
- Add checksum/hash verification.
- Add support for streaming large documents.
"""

from __future__ import annotations

from typing import Any

import requests

from sources.base_source import BaseSource, SourceError


class DocumentSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        url = str(kwargs.get("url", "")).strip()
        if not url and self.base_url:
            path = str(kwargs.get("path", "")).strip()
            url = f"{self.base_url}/{path.lstrip('/')}"
        if not url:
            raise ValueError("url or path is required")

        try:
            response = requests.get(url, headers=self._headers(), timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SourceError(str(exc)) from exc

        return {
            "content": response.content,
            "content_type": response.headers.get("Content-Type", "application/octet-stream"),
            "source_url": url,
        }
