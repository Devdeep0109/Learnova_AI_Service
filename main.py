from fastapi import FastAPI
from app.api.document_routes import router as document_router
from app.api.test_routes import router as test_router

app = FastAPI(
    title="Learnova AI Service",
    version="1.0.0"
)

# app.include_router(router)
app.include_router(document_router)
app.include_router(test_router)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "learnova-ai-service"
    }