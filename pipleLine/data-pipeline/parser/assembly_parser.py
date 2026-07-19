"""
Purpose:
- Parse assembly hierarchy and component relationships.

Input:
- Raw assembly payload from provider.

Output:
- Parsed assembly dictionary.

Responsibilities:
- Extract parent-child hierarchy fields.
- Keep component list in structured format.

TODO implementation notes:
- Add graph validation and orphan detection.
- Add parser profile by provider source.
"""

from __future__ import annotations


class AssemblyParser:
    def parse(self, raw_data: dict) -> dict:
        components = raw_data.get("components") or []
        if isinstance(components, str):
            components = [value.strip() for value in components.split(",") if value.strip()]
        return {
            "assembly_id": raw_data.get("assembly_id") or raw_data.get("id") or "",
            "name": raw_data.get("name") or raw_data.get("assembly_name") or "",
            "parent_id": raw_data.get("parent_id"),
            "components": components,
            "source": raw_data.get("source", "assembly_provider"),
        }
