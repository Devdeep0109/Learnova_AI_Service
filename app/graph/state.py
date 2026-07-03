from typing import TypedDict
class LearnovaState(TypedDict):

    document_id: str
    question_count: int
    difficulty: str
    focus_topic: str
    title: str

    chunks: list
    all_topics: list
    final_topics: dict
    blueprint: dict
    mcqs: list