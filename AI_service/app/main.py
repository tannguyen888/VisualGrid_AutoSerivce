from fastapi import FastAPI

from controller.chatbot import router as chatbot_router
from controller.diagnosis import router as diagnosis_router
from controller.knowledge import router as knowledge_router
from controller.search import router as search_router


app = FastAPI(title="AI Service", version="0.1.0")

app.include_router(diagnosis_router, prefix="/api/diagnosis", tags=["diagnosis"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(search_router, prefix="/api/search", tags=["search"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["knowledge"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
