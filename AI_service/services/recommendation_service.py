"""
Purpose:
- Generate conversational repair recommendations with RAG grounding.

Input:
- ChatRequest from application backend.

Output:
- ChatResponse with safe guidance and references.

Dependencies:
- services.rag_service
- llm.llm_client
- services.safety_layer
- prompts.repair_prompt

Future implementation:
- Add memory/session context and multilingual adaptation.
"""

from __future__ import annotations

from llm.llm_client import LLMClient
from models.request_model import ChatRequest
from models.response_model import ChatResponse
from prompts.repair_prompt import build_repair_prompt
from services.embedding_service import EmbeddingService
from services.rag_service import RAGService
from services.safety_layer import SafetyLayer


class RecommendationService:
    def __init__(self) -> None:
        embedding_service = EmbeddingService()
        self.rag_service = RAGService(embedding_service=embedding_service)
        self.llm_client = LLMClient()
        self.safety_layer = SafetyLayer()

    async def generate_reply(self, request: ChatRequest) -> ChatResponse:
        query = " ".join([request.message, request.vehicle, request.code, request.symptom]).strip()
        references = await self.rag_service.retrieve(query=query, top_k=request.top_k)
        prompt = build_repair_prompt(request=request, docs=references)
        generated = await self.llm_client.generate(prompt)
        safe_text, warnings = self.safety_layer.apply(generated)
        return ChatResponse(message=safe_text, safety_warnings=warnings, references=references)
