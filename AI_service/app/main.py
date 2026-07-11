from fastapi import FastAPI

from api.chatbot import router as chatbot_router
from api.diagnosis import router as diagnosis_router
from api.search import router as search_router


app = FastAPI(title="AI Service", version="0.1.0")

app.include_router(diagnosis_router, prefix="/api/diagnosis", tags=["diagnosis"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(search_router, prefix="/api/search", tags=["search"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
