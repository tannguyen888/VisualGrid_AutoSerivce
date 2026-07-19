"""
Purpose:
- Normalize assembly hierarchy data into canonical shape.

Input:
- Parsed assembly dictionary.

Output:
- Canonical assembly payload for validation/loading.

Responsibilities:
- Ensure stable assembly IDs and component list format.
- Preserve parent-child hierarchy fields.

TODO implementation notes:
- Add hierarchy integrity checks.
- Add generated display path for UI usage.
"""

from __future__ import annotations


class AssemblyMapper:
    def map(self, assembly_data: dict) -> dict:
        components = assembly_data.get("components") or []
        return {
            "assembly_id": str(assembly_data.get("assembly_id") or "").strip(),
            "name": str(assembly_data.get("name") or "").strip(),
            "parent_id": assembly_data.get("parent_id"),
            "components": [str(item).strip() for item in components if str(item).strip()],
            "source": assembly_data.get("source", "unknown"),
        }
