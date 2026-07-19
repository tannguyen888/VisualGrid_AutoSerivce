"""
Purpose:
- Defines canonical vehicle schema used across the ETL pipeline.

Input:
- Mapped vehicle payload from parser/transformer.

Output:
- Validated vehicle model instance.

Responsibilities:
- Validate critical vehicle identity fields.
- Enforce VIN and model year constraints.

TODO implementation notes:
- Add region-specific trim constraints.
- Add engine code reference validation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class VehicleSchema(BaseModel):
    vin: str | None = Field(default=None, min_length=11, max_length=17)
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1950, le=2100)
    engine: str | None = None
    source: str = Field(default="unknown")

    @field_validator("vin")
    @classmethod
    def _normalize_vin(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip().upper()
        return cleaned or None
