"""
Purpose:
- Parse raw vehicle specification payloads into structured technical attributes.

Input:
- Raw specification provider payload.

Output:
- Parsed specification dictionary.

Responsibilities:
- Normalize spec keys across source variations.
- Keep unit labels for later transformer normalization.

TODO implementation notes:
- Add robust unit conversion normalization.
- Add structured handling for nested trim specs.
"""

from __future__ import annotations


class SpecificationParser:
    def parse(self, raw_data: dict) -> dict:
        return {
            "horsepower": raw_data.get("horsepower") or raw_data.get("hp") or raw_data.get("horsePower"),
            "torque": raw_data.get("torque"),
            "fuel_type": raw_data.get("fuel_type") or raw_data.get("fuelType"),
            "drivetrain": raw_data.get("drivetrain"),
            "source": raw_data.get("source", "spec_provider"),
        }
