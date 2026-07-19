"""
Purpose:
- Normalize parsed specification data into canonical technical attributes.

Input:
- Parsed specification dictionary.

Output:
- Canonical specification payload.

Responsibilities:
- Map field aliases (horsePower/hp/horsepower) into one key.
- Keep normalized spec keys for relational persistence.

TODO implementation notes:
- Add unit conversion to base units.
- Add spec source conflict resolution strategy.
"""

from __future__ import annotations


class SpecificationMapper:
    def map(self, specification_data: dict) -> dict:
        horsepower = (
            specification_data.get("horsepower")
            or specification_data.get("horsePower")
            or specification_data.get("hp")
        )
        return {
            "horsepower": horsepower,
            "torque": specification_data.get("torque"),
            "fuel_type": specification_data.get("fuel_type"),
            "drivetrain": specification_data.get("drivetrain"),
            "source": specification_data.get("source", "unknown"),
        }
