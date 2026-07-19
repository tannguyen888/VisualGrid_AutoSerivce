"""
Purpose:
- Parse raw vehicle payload into semantic fields.

Input:
- Raw provider vehicle payload.

Output:
- Parsed vehicle dictionary.

Responsibilities:
- Extract make/model/year/engine/vin across varying key names.
- Return parser-normalized representation for mapper stage.

TODO implementation notes:
- Add trim-level parsing and market variants.
- Add provider-specific parser profiles.
"""

from __future__ import annotations


class VehicleParser:
    def parse(self, raw_data: dict) -> dict:
        return {
            "vin": raw_data.get("vin") or raw_data.get("VIN"),
            "make": raw_data.get("make") or raw_data.get("manufacturer") or "",
            "model": raw_data.get("model") or raw_data.get("vehicleModel") or "",
            "year": raw_data.get("year") or raw_data.get("modelYear") or 0,
            "engine": raw_data.get("engine") or raw_data.get("engineType"),
            "source": raw_data.get("source", "vehicle_provider"),
        }
