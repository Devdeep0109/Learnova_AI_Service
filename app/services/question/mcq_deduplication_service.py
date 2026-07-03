from app.services.embedding.embedding_service import embeddings
from app.services.topic.topic_similarity_service import calculate_similarity
from app.config import QUESTION_SIMILARITY_THRESHOLD

def deduplicate_mcqs(mcqs,blueprint):

    unique_mcqs = []
    unique_embeddings = []

    for mcq in mcqs:

        question_embedding = embeddings.embed_query(mcq["question"])
        duplicate = False

        for existing_embedding in unique_embeddings:

            similarity = calculate_similarity(
                question_embedding,
                existing_embedding
            )
            if similarity >= QUESTION_SIMILARITY_THRESHOLD:
                duplicate = True
                break

        if not duplicate:

            unique_mcqs.append(mcq)
            unique_embeddings.append(question_embedding)
        
    ## OUTSIDE the loop 
    remaining_topics = {}
    for mcq in unique_mcqs:
        topic = mcq["topic"]
        remaining_topics[topic] = (
            remaining_topics.get(topic, 0) + 1
        )
    missing_topics = {}
        
    for topic, expected in blueprint.items():
        generated = remaining_topics.get(topic,0)
        missing = expected - generated

        if missing > 0:
            missing_topics[topic] = missing

    return {
        "mcqs": unique_mcqs,
        "missing_topics": missing_topics
    }