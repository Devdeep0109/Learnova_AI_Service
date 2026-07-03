def flatten_topics(all_topics):

    result = []

    for chunk_topics in all_topics:

        for topic in chunk_topics:

            result.append(topic["topic"])

    return result