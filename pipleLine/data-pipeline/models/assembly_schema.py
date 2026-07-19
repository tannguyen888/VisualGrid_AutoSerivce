"""
Purpose:
- Defines canonical assembly schema for system/component hierarchy.

Input:
- Mapped assembly payload.

Output:
- Validated assembly model instance.

Responsibilities:
- Preserve parent-child structure and component references.
- Ensure downstream storage receives a stable shape.

TODO implementation notes:
- Add cycle detection and hierarchy depth limits.
- Add graph consistency checks across sources.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AssemblySchema(BaseModel):
    assembly_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    parent_id: str | None = None
    components: list[str] = Field(default_factory=list)
    source: str = Field(default="unknown")
