"""
Purpose:
- Schema-level validation for canonical ETL payloads.

Input:
- Entity name and transformed payload.

Output:
- Validated model dumped as dictionary.

Responsibilities:
- Validate records against Pydantic schema models.
- Return structured errors for invalid records.

TODO implementation notes:
- Add granular error codes for monitoring dashboards.
- Add strict mode for production hard-fail enforcement.
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from models.assembly_schema import AssemblySchema
from models.part_schema import PartSchema
from models.repair_schema import RepairSchema
from models.vehicle_schema import VehicleSchema


MODEL_BY_ENTITY = {
    "vehicle": VehicleSchema,
    "part": PartSchema,
    "repair": RepairSchema,
    "assembly": AssemblySchema,
}


class SchemaValidator:
    def validate(self, entity: str, payload: dict[str, Any]) -> dict[str, Any]:
        model = MODEL_BY_ENTITY.get(entity)
        if model is None:
            raise ValueError(f"Unsupported entity for schema validation: {entity}")
        try:
            return model.model_validate(payload).model_dump()
        except ValidationError as exc:
            raise ValueError(f"Schema validation failed for {entity}: {exc}") from exc
