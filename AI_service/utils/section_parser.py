"""
Purpose:
- Parse the section-formatted text produced by the diagnosis prompt into
  structured lists (causes/steps/parts/tools/safety warnings).

Input:
- Raw LLM output text following the "N) Header" convention from
  prompts.diagnosis_prompt.

Output:
- dict mapping section key -> list[str] of bullet/ordered list items.

Dependencies:
- re

Future implementation:
- Ask the LLM for JSON output directly and drop text parsing once prompts
  reliably support structured output mode.
"""

from __future__ import annotations

import re

_SECTION_KEYS = {
    "problem": "problem",
    "possible causes": "possible_causes",
    "recommended steps": "recommended_steps",
    "parts needed": "parts_needed",
    "tools needed": "tools_needed",
    "safety warnings": "safety_warnings",
}

_HEADER_RE = re.compile(r"^\s*\d+\)\s*([A-Za-z ]+)", re.IGNORECASE)
_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*(.+)$")


def parse_diagnosis_sections(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {key: [] for key in _SECTION_KEYS.values()}
    current_key: str | None = None

    for line in text.splitlines():
        header_match = _HEADER_RE.match(line)
        if header_match:
            label = header_match.group(1).strip().lower()
            current_key = _SECTION_KEYS.get(label)
            continue

        if current_key is None:
            continue

        item_match = _ITEM_RE.match(line)
        if item_match:
            result[current_key].append(item_match.group(1).strip())
        elif current_key == "problem" and line.strip():
            result["problem"].append(line.strip())

    return result
