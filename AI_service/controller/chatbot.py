from fastapi import APIRouter

from models.request_model import ChatRequest
from models.response_model import ChatResponse
from services.recommendation_service import RecommendationService


router = APIRouter()
recommendation_service = RecommendationService()


@router.post("/message", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await recommendation_service.generate_reply(request)
