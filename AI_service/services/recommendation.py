"""
Purpose:
- Backward-compatible recommendation wrapper.

Input:
- Raw message string from legacy callers.

Output:
- Generated reply text.

Dependencies:
- asyncio
- models.request_model
- services.recommendation_service

Future implementation:
- Remove wrapper once all callers pass ChatRequest directly.
"""

from __future__ import annotations

import asyncio

from models.request_model import ChatRequest
from services.recommendation_service import RecommendationService as _RecommendationService


class RecommendationService:
    def __init__(self) -> None:
        self._service = _RecommendationService()

    def generate_reply(self, message: str) -> str:
        response = asyncio.run(self._service.generate_reply(ChatRequest(message=message)))
        return response.message
