"""
Purpose:
- Build repair-assistant prompt templates for general user questions.

Input:
- User message and retrieved context snippets.

Output:
- Prompt string for LLM generation.

Dependencies:
- None

Future implementation:
- Add role-based variants for novice vs advanced users.
"""

from __future__ import annotations

from models.request_model import ChatRequest
from models.response_model import SearchResult


def build_repair_prompt(request: ChatRequest, docs: list[SearchResult]) -> str:
    context = "\n".join(
        [f"- [{doc.source}] {doc.title}: {doc.content}" for doc in docs]
    ) or "- No context found"
    return (
        "You are an automotive DIY assistant.\n"
        "Do not provide dangerous instructions.\n"
        "Always include safety reminders and checks.\n\n"
        f"User question: {request.message}\n"
        f"Vehicle: {request.vehicle}\n"
        f"Code: {request.code}\n"
        f"Symptom: {request.symptom}\n\n"
        "Knowledge context:\n"
        f"{context}\n"
    )
