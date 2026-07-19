"""
Purpose:
- Normalize parsed repair payload for canonical internal schema.

Input:
- Parsed repair dictionary.

Output:
- Canonical repair payload for validation/loading.

Responsibilities:
- Standardize list fields and remove empty entries.
- Keep format stable for document-oriented storage.

TODO implementation notes:
- Add cross-linking to parts and assembly references.
- Add procedure version metadata.
"""

from __future__ import annotations


class RepairMapper:
    def map(self, repair_data: dict) -> dict:
        def _compact(items: list[str] | None) -> list[str]:
            return [str(item).strip() for item in (items or []) if str(item).strip()]

        return {
            "title": str(repair_data.get("title") or "Repair Procedure").strip(),
            "steps": _compact(repair_data.get("steps")),
            "tools": _compact(repair_data.get("tools")),
            "torque_values": _compact(repair_data.get("torque_values")),
            "safety_notes": _compact(repair_data.get("safety_notes")),
            "source": repair_data.get("source", "unknown"),
        }
