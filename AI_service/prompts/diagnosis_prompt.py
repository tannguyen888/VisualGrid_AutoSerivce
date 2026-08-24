"""
Purpose:
- Build diagnosis-specific prompt templates for automotive troubleshooting.

Input:
- Vehicle, code, symptom, and retrieved context documents.

Output:
- Prompt text for LLM inference.

Dependencies:
- None

Future implementation:
- Add multilingual template variants and constrained output format.
"""

from __future__ import annotations

from models.request_model import DiagnosisRequest
from models.response_model import SearchResult


def build_diagnosis_prompt(request: DiagnosisRequest, docs: list[SearchResult]) -> str:
    context = "\n".join(
        [f"- [{doc.source}] {doc.title}: {doc.content}" for doc in docs]
    ) or "- No context found"
    return (
        "You are an automotive technician.\n"
        "Never guarantee repair success.\n"
        "Always include safety warnings and recommend verification steps.\n\n"
        f"Vehicle: {request.vehicle}\n"
        f"DTC code: {request.code}\n"
        f"Symptom: {request.symptom}\n\n"
        "Knowledge context:\n"
        f"{context}\n\n"
        "Return sections:\n"
        "1) Problem\n"
        "2) Possible causes (bullet list)\n"
        "3) Recommended steps (ordered list)\n"
        "4) Safety warnings (bullet list)\n"
    )
