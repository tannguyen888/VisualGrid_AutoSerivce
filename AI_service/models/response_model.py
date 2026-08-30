"""
Purpose:
- Define API response contracts for diagnosis, chat, retrieval, and knowledge management.

Input:
- Service layer outputs.

Output:
- Typed Pydantic response models serialized by FastAPI.

Dependencies:
- pydantic

Future implementation:
- Add confidence scoring and trace/debug sections.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    source: str
    title: str
    content: str
    score: float
    doc_id: str = ""


class DiagnosisResponse(BaseModel):
    problem: str
    possible_causes: list[str] = Field(default_factory=list)
    recommended_steps: list[str] = Field(default_factory=list)
    parts_needed: list[str] = Field(default_factory=list)
    tools_needed: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    references: list[SearchResult] = Field(default_factory=list)


class ChatResponse(BaseModel):
    message: str
    safety_warnings: list[str] = Field(default_factory=list)
    references: list[SearchResult] = Field(default_factory=list)


class KnowledgeDocumentResponse(BaseModel):
    doc_id: str
    title: str
    content: str
    source: str
    metadata: dict[str, str] = Field(default_factory=dict)
