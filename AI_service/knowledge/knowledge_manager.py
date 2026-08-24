"""
Purpose:
- Manage knowledge base documents and synchronize retrieval index.

Input:
- Document CRUD requests.

Output:
- Knowledge documents and indexing side effects.

Dependencies:
- models.request_model
- models.response_model
- services.embedding_service

Future implementation:
- Persist metadata in SQL database and add versioning/audit trail.
"""

from __future__ import annotations

from models.request_model import KnowledgeDocumentCreate, KnowledgeDocumentUpdate
from models.response_model import KnowledgeDocumentResponse
from services.embedding_service import EmbeddingService


class KnowledgeManager:
    def __init__(self) -> None:
        self._store: dict[str, KnowledgeDocumentResponse] = {}
        self.embedding_service = EmbeddingService()

    async def add_document(self, request: KnowledgeDocumentCreate) -> KnowledgeDocumentResponse:
        document = KnowledgeDocumentResponse(
            doc_id=request.doc_id,
            title=request.title,
            content=request.content,
            source=request.source,
            metadata=request.metadata,
        )
        self._store[request.doc_id] = document
        await self.embedding_service.index_document(
            doc_id=document.doc_id,
            title=document.title,
            content=document.content,
            source=document.source,
        )
        return document

    async def update_document(self, doc_id: str, request: KnowledgeDocumentUpdate) -> KnowledgeDocumentResponse:
        if doc_id not in self._store:
            raise KeyError(f"Document not found: {doc_id}")

        current = self._store[doc_id]
        updated = KnowledgeDocumentResponse(
            doc_id=doc_id,
            title=request.title if request.title is not None else current.title,
            content=request.content if request.content is not None else current.content,
            source=request.source if request.source is not None else current.source,
            metadata=request.metadata if request.metadata is not None else current.metadata,
        )
        self._store[doc_id] = updated
        await self.embedding_service.index_document(
            doc_id=updated.doc_id,
            title=updated.title,
            content=updated.content,
            source=updated.source,
        )
        return updated

    async def delete_document(self, doc_id: str) -> None:
        self._store.pop(doc_id, None)
        await self.embedding_service.remove_document(doc_id)

    async def get_document(self, doc_id: str) -> KnowledgeDocumentResponse:
        if doc_id not in self._store:
            raise KeyError(f"Document not found: {doc_id}")
        return self._store[doc_id]

    async def list_documents(self) -> list[KnowledgeDocumentResponse]:
        return list(self._store.values())
