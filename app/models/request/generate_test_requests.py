from pydantic import BaseModel

class GenerateTestRequest(BaseModel):
    document_id: str
    question_count: int
    difficulty: str
    focus_topic: str | None = None
    title: str