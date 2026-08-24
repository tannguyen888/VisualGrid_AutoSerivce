"""
Purpose:
- pgvector adapter scaffold for vector retrieval operations.

Input:
- Queries and documents for indexing/retrieval.

Output:
- Search results from pgvector backend.

Dependencies:
- models.response_model

Future implementation:
- Implement SQLAlchemy + pgvector distance search.
"""

from __future__ import annotations

from models.response_model import SearchResult


class PgVectorStore:
    async def upsert(self, doc_id: str, title: str, content: str, source: str) -> None:
        _ = (doc_id, title, content, source)

    async def delete(self, doc_id: str) -> None:
        _ = doc_id

    async def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        _ = (query, top_k)
        return []
