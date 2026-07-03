from app.services.embedding.topic_embedding_service import embed_topics
from app.services.topic.topic_similarity_service import calculate_similarity
from app.services.retrieval.chroma_service import chroma_service
from app.config import (SIMILARITY_THRESHOLD)

def resolve_teacher_topics(
    teacher_topics: list[str],
    blueprint_topics: list[str],
    blueprint_embeddings: list[list[float]],
    document_id: str
):

    if not teacher_topics:
        return []

    resolved_topics = []

    for teacher_topic in teacher_topics:

        # Embed teacher topic
        teacher_embedding = embed_topics(
            [teacher_topic]
        )[0]

        best_similarity = 0
        best_topic = None

        # Compare against every blueprint topic
        for topic, embedding in zip(
            blueprint_topics,
            blueprint_embeddings
        ):

            similarity = calculate_similarity(
                teacher_embedding,
                embedding
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_topic = topic

        # Existing blueprint topic found
        if best_similarity >= SIMILARITY_THRESHOLD:

            resolved_topics.append(
                best_topic
            )
            continue

        # Otherwise search inside the uploaded document
        chunks = chroma_service.search_chunks(
            document_id=document_id,
            query_embedding=teacher_embedding,
            top_k=1
        )

        # If document contains something relevant,
        # keep the teacher topic.
        if chunks:
            resolved_topics.append(
                teacher_topic
            )

        # Otherwise ignore it.

    return list(
        set(resolved_topics)
    )