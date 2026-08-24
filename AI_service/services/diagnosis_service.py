"""
Purpose:
- Provide diagnosis workflow for OBD code + symptoms using RAG and LLM.

Input:
- DiagnosisRequest containing vehicle, code, and symptom.

Output:
- DiagnosisResponse with problem, causes, steps, and safety warnings.

Dependencies:
- services.rag_service
- llm.llm_client
- services.safety_layer
- prompts.diagnosis_prompt

Future implementation:
- Add deterministic post-processing for structured JSON outputs.
"""

from __future__ import annotations

from llm.llm_client import LLMClient
from models.request_model import DiagnosisRequest
from models.response_model import DiagnosisResponse
from prompts.diagnosis_prompt import build_diagnosis_prompt
from services.embedding_service import EmbeddingService
from services.rag_service import RAGService
from services.safety_layer import SafetyLayer


class DiagnosisService:
    def __init__(self) -> None:
        embedding_service = EmbeddingService()
        self.rag_service = RAGService(embedding_service=embedding_service)
        self.llm_client = LLMClient()
        self.safety_layer = SafetyLayer()

    async def diagnose(self, request: DiagnosisRequest) -> DiagnosisResponse:
        query = f"{request.vehicle} {request.code} {request.symptom}".strip()
        references = await self.rag_service.retrieve(query=query, top_k=request.top_k)
        prompt = build_diagnosis_prompt(request=request, docs=references)
        generated = await self.llm_client.generate(prompt)
        safe_text, warnings = self.safety_layer.apply(generated)

        problem = f"Potential issue related to {request.code} on {request.vehicle}"
        possible_causes = [
            "Ignition or fuel delivery irregularity",
            "Sensor/circuit inconsistency",
            "Mechanical condition requiring inspection",
        ]
        recommended_steps = [
            "Read freeze-frame data and confirm active DTC.",
            "Inspect wiring/connectors and associated components.",
            "Run guided tests from service manual before replacement.",
        ]

        if safe_text:
            recommended_steps.append("Review assistant notes: " + safe_text.splitlines()[0][:160])

        return DiagnosisResponse(
            problem=problem,
            possible_causes=possible_causes,
            recommended_steps=recommended_steps,
            safety_warnings=warnings,
            references=references,
        )
