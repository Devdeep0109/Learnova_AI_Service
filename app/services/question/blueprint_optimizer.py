from app.config import (
    BOOST_FACTOR,
)

def optimize_blueprint(
    blueprint: dict,
    important_topics: list[str],
    boost_factor: float = 0.30
):

    if not important_topics:
        return blueprint

    weighted_scores = {}

    for topic, count in blueprint.items():
        weight = count
        if topic in important_topics:
            weight *= (1 + boost_factor)

        weighted_scores[topic] = weight

    total_weight = sum(
        weighted_scores.values()
    )

    total_questions = sum(
        blueprint.values()
    )
    optimized = {}

    for topic, weight in weighted_scores.items():

        optimized[topic] = max(1,round(weight / total_weight * total_questions))

    difference = (
        total_questions -
        sum(optimized.values())
    )

    sorted_topics = sorted(
        optimized.items(),
        key=lambda x: x[1],
        reverse=True
    )

    index = 0
    while difference != 0:

        topic = sorted_topics[index][0]
        if difference > 0:
            optimized[topic] += 1
            difference -= 1

        elif optimized[topic] > 1:
            optimized[topic] -= 1
            difference += 1

        index = (index + 1) % len(sorted_topics)

    return optimized