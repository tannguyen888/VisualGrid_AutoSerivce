from fastapi import APIRouter, Query

from models.embedding import SearchResult
from services.embedding_service import EmbeddingService


router = APIRouter()
embedding_service = EmbeddingService()


@router.get("/", response_model=list[SearchResult])
def search(query: str = Query(..., min_length=1)) -> list[SearchResult]:
    return embedding_service.search(query)
