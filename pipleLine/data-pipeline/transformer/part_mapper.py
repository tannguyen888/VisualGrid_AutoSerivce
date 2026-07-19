"""
Purpose:
- Normalize parsed part payload into canonical part record.

Input:
- Parsed part dictionary.

Output:
- Canonical part payload.

Responsibilities:
- Standardize OEM number formatting.
- Normalize compatibility collection shape.

TODO implementation notes:
- Add canonical part naming dictionary.
- Add compatibility score by source confidence.
"""

from __future__ import annotations


class PartMapper:
    def map(self, part_data: dict) -> dict:
        compatibility = part_data.get("compatibility") or []
        return {
            "oem_number": str(part_data.get("oem_number") or "").strip().upper(),
            "name": str(part_data.get("name") or "").strip(),
            "component": part_data.get("component"),
            "compatibility": [str(item).strip() for item in compatibility if str(item).strip()],
            "assembly_ref": part_data.get("assembly_ref"),
            "source": part_data.get("source", "unknown"),
        }
