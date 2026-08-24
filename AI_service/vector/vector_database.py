"""
Purpose:
- Define vector database abstraction used by the RAG service.

Input:
- Text, embeddings, and retrieval queries.

Output:
- Retrieved search results with relevance scores.

Dependencies:
- models.response_model

Future implementation:
- Plug in FAISS and production-grade pgvector/chromadb adapters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from models.response_model import SearchResult


class VectorDatabase(Protocol):
    async def upsert(self, doc_id: str, title: str, content: str, source: str) -> None:
        ...

    async def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        ...

    async def delete(self, doc_id: str) -> None:
        ...


@dataclass(slots=True)
class _VectorDoc:
    doc_id: str
    title: str
    content: str
    source: str


class InMemoryVectorDatabase:
    def __init__(self) -> None:
        self._docs: dict[str, _VectorDoc] = {}

    async def upsert(self, doc_id: str, title: str, content: str, source: str) -> None:
        self._docs[doc_id] = _VectorDoc(doc_id=doc_id, title=title, content=content, source=source)

    async def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_tokens = {token.lower() for token in query.split() if token.strip()}
        ranked: list[tuple[float, _VectorDoc]] = []

        for doc in self._docs.values():
            doc_tokens = {token.lower() for token in (doc.title + " " + doc.content).split() if token.strip()}
            overlap = len(query_tokens.intersection(doc_tokens))
            if overlap == 0:
                continue
            score = overlap / max(1, len(query_tokens))
            ranked.append((score, doc))

        ranked.sort(key=lambda item: item[0], reverse=True)
        return [
            SearchResult(
                source=doc.source,
                title=doc.title,
                content=doc.content,
                score=score,
                doc_id=doc.doc_id,
            )
            for score, doc in ranked[:top_k]
        ]

    async def delete(self, doc_id: str) -> None:
        self._docs.pop(doc_id, None)
