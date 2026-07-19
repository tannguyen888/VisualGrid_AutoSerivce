"""
Purpose:
- Normalize parsed vehicle payload into canonical internal format.

Input:
- Parsed vehicle dictionary.

Output:
- Canonical vehicle payload for validation and loading.

Responsibilities:
- Resolve field aliases and normalize value casing.
- Keep output stable across multiple data providers.

TODO implementation notes:
- Add confidence scoring for conflicting values.
- Add source priority rules for field conflict resolution.
"""

from __future__ import annotations


class VehicleMapper:
    def map(self, vehicle_data: dict) -> dict:
        return {
            "vin": str(vehicle_data.get("vin") or "").strip().upper() or None,
            "make": str(vehicle_data.get("make") or "").strip().title(),
            "model": str(vehicle_data.get("model") or "").strip(),
            "year": int(vehicle_data.get("year") or 0),
            "engine": vehicle_data.get("engine"),
            "source": vehicle_data.get("source", "unknown"),
        }
