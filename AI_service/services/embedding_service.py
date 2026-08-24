"""
Purpose:
- Convert knowledge documents into retrieval-ready vectors and perform search.

Input:
- Document content for indexing and query text for retrieval.

Output:
- Ranked search results used by RAG.

Dependencies:
- models.response_model
- vector.vector_database

Future implementation:
- Replace in-memory scoring with real embedding vectors.
"""

from __future__ import annotations

from models.response_model import SearchResult
from vector.vector_database import InMemoryVectorDatabase, VectorDatabase


class EmbeddingService:
    def __init__(self, vector_db: VectorDatabase | None = None) -> None:
        self.vector_db = vector_db or InMemoryVectorDatabase()

    async def index_document(self, doc_id: str, title: str, content: str, source: str) -> None:
        await self.vector_db.upsert(doc_id=doc_id, title=title, content=content, source=source)

    async def remove_document(self, doc_id: str) -> None:
        await self.vector_db.delete(doc_id)

    async def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        return await self.vector_db.search(query=query, top_k=top_k)
