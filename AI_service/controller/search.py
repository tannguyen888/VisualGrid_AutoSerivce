from fastapi import APIRouter, Query

from models.response_model import SearchResult
from services.embedding_service import EmbeddingService


router = APIRouter()
embedding_service = EmbeddingService()


@router.get("/", response_model=list[SearchResult])
async def search(
    query: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=50),
) -> list[SearchResult]:
    return await embedding_service.search(query=query, top_k=top_k)
