"""
Purpose:
- Parse raw part payload into a normalized part structure.

Input:
- Raw part/OEM provider payload.

Output:
- Parsed part dictionary.

Responsibilities:
- Normalize key aliases for part identifiers and fitment.
- Provide consistent shape for transformer stage.

TODO implementation notes:
- Add smart parsing for multi-line compatibility strings.
- Add aliasing for regional OEM number formats.
"""

from __future__ import annotations


class PartParser:
    def parse(self, raw_data: dict) -> dict:
        compatibility = raw_data.get("compatibility") or raw_data.get("fitment") or []
        if isinstance(compatibility, str):
            compatibility = [item.strip() for item in compatibility.split(",") if item.strip()]
        return {
            "oem_number": raw_data.get("oem_number") or raw_data.get("oemNumber") or "",
            "name": raw_data.get("name") or raw_data.get("part_name") or "",
            "component": raw_data.get("component"),
            "compatibility": compatibility,
            "assembly_ref": raw_data.get("assembly_ref") or raw_data.get("assemblyId"),
            "source": raw_data.get("source", "parts_provider"),
        }
