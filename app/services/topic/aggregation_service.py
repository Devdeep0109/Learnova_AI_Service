from collections import defaultdict

def aggregate_topics(
    all_topics,
    canonical_map
):

    result = defaultdict(
        lambda: {
            "score": 0,
            "chunk_ids": set()
        }
    )

    for chunk_id, topic_list in enumerate(all_topics):

        for topic in topic_list:

            original_topic = topic["topic"]

            topic_name = canonical_map.get(
                original_topic,
                original_topic
            )
            result[topic_name]["score"] += topic["importance"]
            result[topic_name]["chunk_ids"].add(chunk_id)

    return {
        topic: {
            "score": data["score"],
            "chunk_ids": list(data["chunk_ids"])
        }
        for topic, data in result.items()
    }