"""
Purpose:
- Backward-compatible diagnosis engine wrapper.

Input:
- Legacy DiagnosisRequest payload.

Output:
- Contract-compliant DiagnosisResponse.

Dependencies:
- asyncio
- services.diagnosis_service

Future implementation:
- Remove wrapper after callers migrate to DiagnosisService.
"""

from __future__ import annotations

import asyncio

from models.request_model import DiagnosisRequest
from models.response_model import DiagnosisResponse
from services.diagnosis_service import DiagnosisService


class DiagnosisEngine:
    def __init__(self) -> None:
        self.service = DiagnosisService()

    def analyze(self, request: DiagnosisRequest) -> DiagnosisResponse:
        return asyncio.run(self.service.diagnose(request))
