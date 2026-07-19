"""
Purpose:
- VIN source connector for fetching raw vehicle details.

Input:
- VIN string.

Output:
- Raw provider JSON payload.

Responsibilities:
- Validate VIN input shape.
- Call VIN provider endpoint and return raw data.

TODO implementation notes:
- Add per-provider VIN checksum validation rules.
- Add fallback provider chain for failed lookups.
"""

from __future__ import annotations

from typing import Any

from sources.base_source import BaseSource


class VinSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        vin = str(kwargs.get("vin", "")).strip().upper()
        if not vin:
            raise ValueError("vin is required")
        return self._request_json(path="vin/decode", params={"vin": vin})
