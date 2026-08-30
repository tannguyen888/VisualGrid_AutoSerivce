"""
Purpose:
- Define API request contracts for diagnosis, chat, search, and knowledge CRUD.

Input:
- Incoming JSON payloads from Spring Boot backend.

Output:
- Typed Pydantic request models.

Dependencies:
- pydantic

Future implementation:
- Add tenant/user metadata and request tracing fields.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DiagnosisRequest(BaseModel):
    vehicle: str = Field(min_length=1, description="Vehicle identifier, e.g. Honda Civic 2020")
    code: str = Field(min_length=1, description="OBD/DTC code, e.g. P0301")
    symptom: str = Field(min_length=1, description="Observed symptom")
    top_k: int = Field(default=5, ge=1, le=20)
    make: str = Field(default="", description="Vehicle make, used to look up backend context")
    model: str = Field(default="", description="Vehicle model, used to look up backend context")
    trim: str = Field(default="", description="Vehicle trim, used to look up backend context")
    year: int | None = Field(default=None, description="Vehicle model year")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    vehicle: str = Field(default="")
    code: str = Field(default="")
    symptom: str = Field(default="")
    top_k: int = Field(default=5, ge=1, le=20)


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class KnowledgeDocumentCreate(BaseModel):
    doc_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    source: str = Field(default="manual")
    metadata: dict[str, str] = Field(default_factory=dict)


class KnowledgeDocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source: str | None = None
    metadata: dict[str, str] | None = None
