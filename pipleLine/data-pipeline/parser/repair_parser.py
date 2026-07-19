"""
Purpose:
- Parse repair and maintenance documents into structured records.

Input:
- Raw repair payload or extracted text blocks.

Output:
- Parsed repair dictionary.

Responsibilities:
- Extract title, steps, tools, torque values, and safety notes.
- Return normalized parser output for mapping and validation.

TODO implementation notes:
- Add NLP-assisted extraction for unstructured manual content.
- Add multilingual extraction profiles.
"""

from __future__ import annotations

import re

TORQUE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\s*(?:Nm|N\.m|lb-ft)\b", re.IGNORECASE)


class RepairParser:
    def parse(self, raw_data: dict) -> dict:
        text = str(raw_data.get("text", ""))
        steps = raw_data.get("steps") or []
        if not steps and text:
            steps = [line.strip() for line in text.splitlines() if line.strip()]

        tools = raw_data.get("tools") or []
        safety_notes = raw_data.get("safety_notes") or raw_data.get("warnings") or []
        torque_values = raw_data.get("torque_values") or TORQUE_PATTERN.findall(text)

        return {
            "title": raw_data.get("title") or "Repair Procedure",
            "steps": steps,
            "tools": tools,
            "torque_values": torque_values,
            "safety_notes": safety_notes,
            "source": raw_data.get("source", "repair_provider"),
        }
