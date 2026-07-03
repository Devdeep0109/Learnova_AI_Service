from app.services.topic.flatten_service import flatten_topics
from app.services.topic.canonical_service import build_canonical_map
from app.services.topic.aggregation_service import aggregate_topics
from app.services.question.create_blueprint import create_blueprint
from app.services.question.topic_resolver import resolve_teacher_topics
from app.services.question.blueprint_optimizer import optimize_blueprint
from app.services.embedding.topic_embedding_service import embed_topics
import re
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("Learnova")

def blueprint_node(state):

    all_topics = state["all_topics"]

    flat_topics = flatten_topics(
        all_topics
    )

    canonical_map = build_canonical_map(
        flat_topics
    )

    final_topics = aggregate_topics(
        all_topics,
        canonical_map
    )
    logger.info("=" * 50)
    logger.info("FINAL TOPICS")
    logger.info(final_topics)
    logger.info("COUNT:", len(final_topics))

    blueprint = create_blueprint(
        aggregated_topics=final_topics,
        question_count=state["question_count"]
    )

    print("=" * 50)
    print("CREATED BLUEPRINT")
    print(blueprint)

    blueprint_topics = list(
        blueprint.keys()
    )

    blueprint_embeddings = embed_topics(
        blueprint_topics
    )
    
    focus_topic = re.sub(
        r"\s+and\s+",
        ",",
        state["focus_topic"],
        flags=re.IGNORECASE
    )

    focus_topic = (
        focus_topic
            .replace(";", ",")
            .replace("|", ",")
    )

    teacher_topics = [
        topic.strip()
        for topic in focus_topic.split(",")
        if topic.strip()
    ]

    resolved_topics = resolve_teacher_topics(
        teacher_topics=teacher_topics,
        blueprint_topics=blueprint_topics,
        blueprint_embeddings=blueprint_embeddings,
        document_id=state["document_id"]
    )

    blueprint = optimize_blueprint(
        blueprint=blueprint,
        important_topics=resolved_topics
    )
    print("=" * 50)
    print("Teacher Topics:", teacher_topics)
    print("Resolved Topics:", resolved_topics)
    print("Blueprint:")
    print(blueprint)

    return {
        "final_topics": final_topics,
        "blueprint": blueprint
    }