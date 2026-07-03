import math

def create_blueprint(
    aggregated_topics: dict,
    question_count: int,
    top_n: int = 5
):

    sorted_topics = sorted(
        aggregated_topics.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    selected_topics = sorted_topics[:top_n]

    total_score = sum(
        data["score"]
        for _, data in selected_topics
    )

    blueprint = {}
    remainders = []
    allocated = 0

    # -----------------------
    # Hamilton Method
    # -----------------------

    for topic, data in selected_topics:

        exact = (
            data["score"] / total_score
        ) * question_count

        floor_questions = math.floor(
            exact
        )

        blueprint[topic] = floor_questions

        allocated += floor_questions

        remainders.append(
            (
                exact - floor_questions,
                topic
            )
        )

    # -----------------------
    # Distribute Remaining Questions
    # -----------------------

    remaining = question_count - allocated

    remainders.sort(
        reverse=True
    )

    for _, topic in remainders[:remaining]:
        blueprint[topic] += 1

    return blueprint