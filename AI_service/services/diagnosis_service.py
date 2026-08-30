"""
Purpose:
- Provide diagnosis workflow for OBD code + symptoms using RAG and LLM,
  grounded in vehicle/DTC context and existing repair procedures fetched
  from the Java backend, and persist the generated procedure back to it.

Input:
- DiagnosisRequest containing vehicle, code, symptom, and optional
  make/model/trim/year for backend context lookup.

Output:
- DiagnosisResponse with problem, causes, steps, parts, tools, and safety warnings.

Dependencies:
- services.rag_service
- services.backend_client
- llm.llm_client
- services.safety_layer
- prompts.diagnosis_prompt
- utils.section_parser

Future implementation:
- Ask the LLM for JSON output directly instead of parsing text sections.
"""

from __future__ import annotations

import logging

from llm.llm_client import LLMClient
from models.request_model import DiagnosisRequest
from models.response_model import DiagnosisResponse
from prompts.diagnosis_prompt import build_diagnosis_prompt
from services.backend_client import BackendClient
from services.embedding_service import EmbeddingService
from services.rag_service import RAGService
from services.safety_layer import SafetyLayer
from utils.section_parser import parse_diagnosis_sections

LOGGER = logging.getLogger(__name__)


class DiagnosisService:
    def __init__(self) -> None:
        embedding_service = EmbeddingService()
        self.rag_service = RAGService(embedding_service=embedding_service)
        self.llm_client = LLMClient()
        self.safety_layer = SafetyLayer()
        self.backend_client = BackendClient()

    async def diagnose(self, request: DiagnosisRequest) -> DiagnosisResponse:
        context: dict = {}
        try:
            context = await self.backend_client.get_context(
                code=request.code,
                make=request.make,
                model=request.model,
                trim=request.trim,
                year=request.year,
            )
        except Exception:
            LOGGER.warning("Failed to fetch backend context for code=%s", request.code, exc_info=True)

        query = f"{request.vehicle} {request.code} {request.symptom}".strip()
        references = await self.rag_service.retrieve(query=query, top_k=request.top_k)
        prompt = build_diagnosis_prompt(request=request, docs=references, context=context)
        generated = await self.llm_client.generate(prompt)
        safe_text, warnings = self.safety_layer.apply(generated)

        sections = parse_diagnosis_sections(safe_text or generated)
        problem = " ".join(sections["problem"]) or f"Potential issue related to {request.code} on {request.vehicle}"
        possible_causes = sections["possible_causes"] or [
            "Ignition or fuel delivery irregularity",
            "Sensor/circuit inconsistency",
            "Mechanical condition requiring inspection",
        ]
        recommended_steps = sections["recommended_steps"] or [
            "Read freeze-frame data and confirm active DTC.",
            "Inspect wiring/connectors and associated components.",
            "Run guided tests from service manual before replacement.",
        ]
        parts_needed = sections["parts_needed"]
        tools_needed = sections["tools_needed"]
        safety_warnings = sections["safety_warnings"] or warnings

        response = DiagnosisResponse(
            problem=problem,
            possible_causes=possible_causes,
            recommended_steps=recommended_steps,
            parts_needed=parts_needed,
            tools_needed=tools_needed,
            safety_warnings=safety_warnings,
            references=references,
        )

        try:
            await self.backend_client.save_repair_procedure(
                {
                    "dtcCode": request.code,
                    "vehicleMake": request.make,
                    "vehicleModel": request.model,
                    "vehicleTrim": request.trim,
                    "vehicleYear": request.year,
                    "title": problem,
                    "steps": "\n".join(recommended_steps),
                    "parts": [{"name": name} for name in parts_needed],
                    "tools": [{"name": name} for name in tools_needed],
                }
            )
        except Exception:
            LOGGER.warning("Failed to save repair procedure to backend for code=%s", request.code, exc_info=True)

        return response
