from app.services.question.mcq_service import generate_mcqs
from app.services.retrieval.chroma_service import chroma_service
from app.services.embedding.topic_embedding_service import embed_topics
from app.services.question.mcq_service import generate_mcqs


def generate_topic_mcqs(
    topic: str,
    question_count: int,
    difficulty: str,
    document_id: str,
    previous_questions: list[str]
):
    
    topic_embedding = embed_topics(
        [topic]
    )[0]

    relevant_chunks = chroma_service.search_chunks(
        document_id=document_id,
        query_embedding=topic_embedding,
        top_k=2
    )

    topic_content = "\n".join(
        relevant_chunks
    )

    mcqs = generate_mcqs(
        topic=topic,
        content=topic_content,
        question_count=question_count,
        difficulty=difficulty,
        previous_questions=previous_questions
    )

    for mcq in mcqs:
        mcq["topic"] = topic

    return mcqs