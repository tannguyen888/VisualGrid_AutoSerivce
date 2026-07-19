"""
Purpose:
- Parse OBD DTC entries into diagnostic structures.

Input:
- Raw DTC payload.

Output:
- Parsed DTC dictionary.

Responsibilities:
- Normalize DTC code formatting.
- Extract symptom, cause, and suggested actions.

TODO implementation notes:
- Add cause taxonomy mapping.
- Add confidence scoring for generated suggestions.
"""

from __future__ import annotations


class DtcParser:
    def parse(self, raw_data: dict) -> dict:
        code = str(raw_data.get("code", "")).strip().upper()
        return {
            "code": code,
            "description": raw_data.get("description") or raw_data.get("meaning") or "",
            "possible_causes": raw_data.get("possible_causes") or raw_data.get("causes") or [],
            "recommended_actions": raw_data.get("recommended_actions") or raw_data.get("fixes") or [],
            "source": raw_data.get("source", "dtc_provider"),
        }
