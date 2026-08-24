"""
Purpose:
- Expose knowledge base CRUD APIs for adding/updating/removing documents.

Input:
- Knowledge document payloads.

Output:
- Stored document records and operation status.

Dependencies:
- fastapi
- knowledge.knowledge_manager
- models.request_model
- models.response_model

Future implementation:
- Add pagination, filtering, and batch import endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from knowledge.knowledge_manager import KnowledgeManager
from models.request_model import KnowledgeDocumentCreate, KnowledgeDocumentUpdate
from models.response_model import KnowledgeDocumentResponse


router = APIRouter()
knowledge_manager = KnowledgeManager()


@router.post("/documents", response_model=KnowledgeDocumentResponse)
async def add_document(request: KnowledgeDocumentCreate) -> KnowledgeDocumentResponse:
    return await knowledge_manager.add_document(request)


@router.get("/documents", response_model=list[KnowledgeDocumentResponse])
async def list_documents() -> list[KnowledgeDocumentResponse]:
    return await knowledge_manager.list_documents()


@router.get("/documents/{doc_id}", response_model=KnowledgeDocumentResponse)
async def get_document(doc_id: str) -> KnowledgeDocumentResponse:
    try:
        return await knowledge_manager.get_document(doc_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/documents/{doc_id}", response_model=KnowledgeDocumentResponse)
async def update_document(doc_id: str, request: KnowledgeDocumentUpdate) -> KnowledgeDocumentResponse:
    try:
        return await knowledge_manager.update_document(doc_id, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str) -> dict[str, str]:
    await knowledge_manager.delete_document(doc_id)
    return {"status": "deleted", "doc_id": doc_id}
