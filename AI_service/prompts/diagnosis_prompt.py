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

from typing import Any

from models.request_model import DiagnosisRequest
from models.response_model import SearchResult


def build_diagnosis_prompt(
    request: DiagnosisRequest,
    docs: list[SearchResult],
    context: dict[str, Any] | None = None,
) -> str:
    context = context or {}
    known_repairs = context.get("existingProcedures") or []
    known_repairs_text = "\n".join(
        f"- {r.get('title')}: parts={r.get('parts')}, tools={r.get('tools')}" for r in known_repairs
    ) or "- None on record"

    context_lines = [
        f"Vehicle: {request.vehicle}",
        f"Make/Model/Trim/Year: {request.make} {request.model} {request.trim} {request.year or ''}".strip(),
        f"DTC code: {request.code}",
    ]
    if context.get("dtcDescription"):
        context_lines.append(f"DTC description (from backend): {context['dtcDescription']}")
    context_lines.append(f"Symptom: {request.symptom}")

    doc_context = "\n".join(
        [f"- [{doc.source}] {doc.title}: {doc.content}" for doc in docs]
    ) or "- No context found"

    return (
        "You are an automotive technician.\n"
        "Never guarantee repair success.\n"
        "Always include safety warnings and recommend verification steps.\n\n"
        f"{chr(10).join(context_lines)}\n\n"
        "Known repair procedures already on file for this DTC:\n"
        f"{known_repairs_text}\n\n"
        "Knowledge context:\n"
        f"{doc_context}\n\n"
        "Return sections exactly as headers followed by a bullet/ordered list:\n"
        "1) Problem\n"
        "2) Possible causes (bullet list)\n"
        "3) Recommended steps (ordered list)\n"
        "4) Parts needed (bullet list of part names, empty if none)\n"
        "5) Tools needed (bullet list of tool names, empty if none)\n"
        "6) Safety warnings (bullet list)\n"
    )
