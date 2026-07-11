from models.llm import DiagnosisRequest, DiagnosisResponse
from utils.prompt_builder import build_diagnosis_prompt


class DiagnosisEngine:
    def analyze(self, request: DiagnosisRequest) -> DiagnosisResponse:
        prompt = build_diagnosis_prompt(request.symptoms, request.vehicle_info)
        return DiagnosisResponse(
            summary="Diagnosis draft generated",
            prompt=prompt,
            probable_causes=["Unknown - connect to LLM or rules engine"],
            recommended_actions=["Inspect DTC codes", "Check sensors", "Verify battery and wiring"],
        )
