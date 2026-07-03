from app.services.topic.topic_service import extract_topics

def topic_extraction_node(state):

    chunks = state["chunks"]

    all_topics = []

    for chunk in chunks:

        topics = extract_topics(chunk)

        all_topics.append(topics)

    return {
        "all_topics": all_topics
    }