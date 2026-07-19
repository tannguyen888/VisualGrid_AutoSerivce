"""
Purpose:
- OEM source connector for manufacturer reference data.

Input:
- OEM part number or catalog key.

Output:
- Raw OEM provider JSON payload.

Responsibilities:
- Query OEM provider endpoints.
- Return raw payload for downstream parsing.

TODO implementation notes:
- Add OEM supersession chain retrieval.
- Add localized part naming support.
"""

from __future__ import annotations

from typing import Any

from sources.base_source import BaseSource


class OemSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        oem_number = str(kwargs.get("oem_number", "")).strip()
        if not oem_number:
            raise ValueError("oem_number is required")
        return self._request_json(path="oem/catalog", params={"oem_number": oem_number})
