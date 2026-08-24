"""
Purpose:
- Apply safety constraints to AI outputs before returning to users.

Input:
- Generated text and optional warning list.

Output:
- Sanitized text and mandatory safety warning messages.

Dependencies:
- None

Future implementation:
- Add policy classifier for high-risk instructions.
"""

from __future__ import annotations


DEFAULT_WARNINGS = [
    "Repair outcomes are not guaranteed; verify with official manual.",
    "Use protective equipment and follow manufacturer safety procedures.",
    "If unsure, consult a certified mechanic before performing repairs.",
]


class SafetyLayer:
    def apply(self, text: str, warnings: list[str] | None = None) -> tuple[str, list[str]]:
        merged = list(DEFAULT_WARNINGS)
        for warning in warnings or []:
            if warning not in merged:
                merged.append(warning)

        lowered = text.lower()
        if "guarantee" in lowered and "not guaranteed" not in lowered:
            text += "\n\nNote: Repair success is not guaranteed; validate each step carefully."

        return text, merged
