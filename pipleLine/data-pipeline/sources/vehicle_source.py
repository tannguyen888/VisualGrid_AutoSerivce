"""
Purpose:
- Vehicle source connector for provider vehicle catalog and specification payloads.

Input:
- Provider filters such as make/model/year.

Output:
- Raw vehicle catalog JSON payload.

Responsibilities:
- Handle provider request parameters.
- Return raw data without transformation.

TODO implementation notes:
- Add pagination support for catalog syncing.
- Add checkpoint-based incremental fetch.
"""

from __future__ import annotations

from typing import Any

from sources.base_source import BaseSource


class VehicleSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        params = {
            "make": kwargs.get("make", ""),
            "model": kwargs.get("model", ""),
            "year": kwargs.get("year", ""),
        }
        return self._request_json(path="vehicles", params=params)
