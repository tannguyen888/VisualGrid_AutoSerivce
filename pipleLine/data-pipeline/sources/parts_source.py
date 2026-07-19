"""
Purpose:
- Parts source connector for OEM parts and compatibility payloads.

Input:
- Query string, OEM number, or provider-specific filters.

Output:
- Raw parts provider JSON payload.

Responsibilities:
- Submit source requests for part catalog data.
- Return unmodified provider response to ETL extractors.

TODO implementation notes:
- Add pagination loop support.
- Add provider-specific query builders.
"""

from __future__ import annotations

from typing import Any

from sources.base_source import BaseSource


class PartsSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        query = str(kwargs.get("query", "")).strip()
        oem_number = str(kwargs.get("oem_number", "")).strip()
        params = {"query": query, "oem_number": oem_number}
        return self._request_json(path="parts/search", params=params)
