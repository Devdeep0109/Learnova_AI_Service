from app.services.embedding.topic_embedding_service import embed_topics
from app.services.topic.topic_similarity_service import calculate_similarity


def cluster_topics(
    topic_names,
    threshold=0.70
):

    vectors = embed_topics(topic_names)

    clusters = []

    for i, topic in enumerate(topic_names):

        placed = False

        for cluster in clusters:

            representative = cluster[0]

            rep_index = topic_names.index(
                representative
            )

            similarity = calculate_similarity(
                vectors[i],
                vectors[rep_index]
            )

            if similarity >= threshold:

                cluster.append(topic)
                placed = True
                break

        if not placed:
            clusters.append([topic])

    return clusters