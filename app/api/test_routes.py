from fastapi import APIRouter

from app.models.request.generate_test_requests import GenerateTestRequest
from app.graph.graph_builder import learnova_graph

router = APIRouter(
    prefix="/tests",
    tags=["Tests"]
)

@router.post("/generate")
async def generate_test(request: GenerateTestRequest):

    result = learnova_graph.invoke(
        {
            "document_id": request.document_id,
            "question_count": request.question_count,
            "difficulty": request.difficulty,
            "focus_topic": request.focus_topic,
            "title": request.title
        }
    )

    return {
        "title": request.title,
        "mcqs": result["mcqs"]
    }