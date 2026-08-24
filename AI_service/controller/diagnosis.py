from fastapi import APIRouter

from models.request_model import DiagnosisRequest
from models.response_model import DiagnosisResponse
from services.diagnosis_service import DiagnosisService


router = APIRouter()
service = DiagnosisService()


@router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_diagnosis(request: DiagnosisRequest) -> DiagnosisResponse:
    return await service.diagnose(request)
