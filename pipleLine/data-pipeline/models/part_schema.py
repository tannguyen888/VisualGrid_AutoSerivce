"""
Purpose:
- Defines canonical part schema used in ETL.

Input:
- Mapped part payload.

Output:
- Validated part model instance.

Responsibilities:
- Validate OEM identifiers and compatibility list.
- Keep normalized fields for relational storage.

TODO implementation notes:
- Add manufacturer master-data validation.
- Add lifecycle/supersession constraints.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PartSchema(BaseModel):
    oem_number: str = Field(min_length=1)
    name: str = Field(min_length=1)
    component: str | None = None
    compatibility: list[str] = Field(default_factory=list)
    assembly_ref: str | None = None
    source: str = Field(default="unknown")
