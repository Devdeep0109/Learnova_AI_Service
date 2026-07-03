from app.services.topic.clustering_service import cluster_topics


def build_canonical_map(topic_names):

    clusters = cluster_topics(topic_names)

    canonical_map = {}

    for cluster in clusters:

        canonical_topic = cluster[0]

        for topic in cluster:
            canonical_map[topic] = canonical_topic

    return canonical_map