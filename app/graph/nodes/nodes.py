from app.services.topic.topic_service import extract_topics

from app.services.topic.flatten_service import flatten_topics
from app.services.topic.canonical_service import build_canonical_map
from app.services.topic.aggregation_service import aggregate_topics
from app.services.question.create_blueprint import create_blueprint

from concurrent.futures import ThreadPoolExecutor

from app.services.question.topic_mcq_service import generate_topic_mcqs
from app.services.question.mcq_deduplication_service import deduplicate_mcqs


def topic_extraction_node(state):

    chunks = state["chunks"]
    all_topics = []

    for chunk in chunks:

        topics = extract_topics(chunk)
        all_topics.append(topics)
    return {"all_topics": all_topics}


def blueprint_node(state):

    all_topics = state["all_topics"]
    flat_topics = flatten_topics(all_topics)
    canonical_map = build_canonical_map(flat_topics)
    final_topics = aggregate_topics(all_topics, canonical_map)
    blueprint = create_blueprint(final_topics, 20)

    return {"final_topics": final_topics, "blueprint": blueprint}


def process_topic(args):
    return generate_topic_mcqs(*args)
