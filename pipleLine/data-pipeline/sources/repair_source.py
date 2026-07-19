"""
Purpose:
- Repair source connector for procedures, maintenance records, and service content.

Input:
- Vehicle and component filter parameters.

Output:
- Raw repair provider JSON payload.

Responsibilities:
- Request repair content from external providers.
- Return raw response for parser/extractor stages.

TODO implementation notes:
- Add provider revision/version sync support.
- Add range-based incremental sync by updated timestamp.
"""

from __future__ import annotations

from typing import Any

from sources.base_source import BaseSource


class RepairSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        params = {
            "vehicle_id": kwargs.get("vehicle_id", ""),
            "system": kwargs.get("system", ""),
            "component": kwargs.get("component", ""),
        }
        return self._request_json(path="repairs", params=params)
