from concurrent.futures import ThreadPoolExecutor

from app.services.question.topic_mcq_service import generate_topic_mcqs
from app.services.question.mcq_deduplication_service import deduplicate_mcqs

def process_topic(args):
    return generate_topic_mcqs(*args)


def mcq_generation_node(state):

    blueprint = state["blueprint"]
    tasks = [
        (
            topic,
            question_count,
            state["difficulty"],
            state["document_id"]
        )
        for topic, question_count in blueprint.items()
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = list(
            executor.map(
                process_topic,
                tasks
            )
        )

    all_mcqs = []

    for mcqs in results:
        all_mcqs.extend(mcqs)

    all_mcqs = deduplicate_mcqs(
        all_mcqs
    )

    return {
        "mcqs": all_mcqs
    }