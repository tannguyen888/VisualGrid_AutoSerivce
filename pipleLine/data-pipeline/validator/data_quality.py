"""
Purpose:
- Data quality validation for completeness, uniqueness, and value sanity checks.

Input:
- Canonical payload and optional previously-seen keys.

Output:
- Quality report with pass/fail and issue list.

Responsibilities:
- Check missing required fields.
- Check duplicate keys and invalid values.

TODO implementation notes:
- Add entity-specific quality rule registry.
- Add anomaly detection for sudden data shape drift.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DataQualityReport:
    passed: bool
    issues: list[str] = field(default_factory=list)


class DataQualityValidator:
    def check(self, payload: dict, required_fields: list[str], unique_key: str | None = None, seen_keys: set[str] | None = None) -> DataQualityReport:
        issues: list[str] = []

        for field_name in required_fields:
            value = payload.get(field_name)
            if value is None or (isinstance(value, str) and not value.strip()):
                issues.append(f"missing required field: {field_name}")

        if unique_key and seen_keys is not None:
            key = str(payload.get(unique_key, "")).strip()
            if not key:
                issues.append(f"empty unique key: {unique_key}")
            elif key in seen_keys:
                issues.append(f"duplicate key: {unique_key}={key}")
            else:
                seen_keys.add(key)

        return DataQualityReport(passed=not issues, issues=issues)
