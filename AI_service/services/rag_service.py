"""
Purpose:
- Implement Retrieval-Augmented Generation workflow utilities.

Input:
- User query and desired retrieval depth.

Output:
- Relevant documents for prompt grounding.

Dependencies:
- services.embedding_service
- models.response_model

Future implementation:
- Add hybrid retrieval and reranking strategies.
"""

from __future__ import annotations

from models.response_model import SearchResult
from services.embedding_service import EmbeddingService


class RAGService:
    def __init__(self, embedding_service: EmbeddingService) -> None:
        self.embedding_service = embedding_service

    async def retrieve(self, query: str, top_k: int = 5) -> list[SearchResult]:
        return await self.embedding_service.search(query=query, top_k=top_k)
