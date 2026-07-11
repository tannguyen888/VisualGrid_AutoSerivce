from fastapi import APIRouter

from services.diagnosis_engine import DiagnosisEngine
from models.llm import DiagnosisRequest, DiagnosisResponse


router = APIRouter()
engine = DiagnosisEngine()


@router.post("/analyze", response_model=DiagnosisResponse)
def analyze_diagnosis(request: DiagnosisRequest) -> DiagnosisResponse:
    return engine.analyze(request)
