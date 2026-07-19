"""
Purpose:
- Defines canonical repair schema for procedures and manuals.

Input:
- Mapped repair payload.

Output:
- Validated repair model instance.

Responsibilities:
- Keep structured steps, tools, torque values, and safety notes.
- Provide a consistent shape for MongoDB storage.

TODO implementation notes:
- Add multilingual text support.
- Add reference links to diagrams and assemblies.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RepairSchema(BaseModel):
    title: str = Field(min_length=1)
    steps: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    torque_values: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    source: str = Field(default="unknown")
