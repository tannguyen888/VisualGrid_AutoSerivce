from pydantic import BaseModel, Field


class DiagnosisRequest(BaseModel):
    symptoms: list[str] = Field(default_factory=list)
    vehicle_info: str = ""


class DiagnosisResponse(BaseModel):
    summary: str
    prompt: str
    probable_causes: list[str]
    recommended_actions: list[str]


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
