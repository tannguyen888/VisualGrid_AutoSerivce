from fastapi import APIRouter

from models.llm import ChatRequest, ChatResponse
from services.recommendation import RecommendationService


router = APIRouter()
recommendation_service = RecommendationService()


@router.post("/message", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    reply = recommendation_service.generate_reply(request.message)
    return ChatResponse(message=reply)
