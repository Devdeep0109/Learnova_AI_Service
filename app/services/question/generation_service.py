from concurrent.futures import ThreadPoolExecutor

from app.config import MAX_WORKERS, MAX_RETRY
from app.services.question.mcq_deduplication_service import deduplicate_mcqs
from app.services.question.topic_mcq_service import generate_topic_mcqs
from app.utils.logger import logger

def process_topic(args):
    return generate_topic_mcqs(*args)


def generate_complete_test(
    blueprint: dict,
    difficulty: str,
    document_id: str
):

    target_questions = sum(
        blueprint.values()
    )

    all_mcqs = []

    current_blueprint = blueprint
    attempt = 0
    generated_history = {}

    while (
        len(all_mcqs) < target_questions
        and attempt < MAX_RETRY
    ):

        logger.info("=" * 50)
        logger.info(f"Attempt : {attempt + 1}")
        logger.info("Generating Blueprint")
        logger.info(current_blueprint)

        tasks = [
            (
                topic,
                question_count,
                difficulty,
                document_id,
                generated_history.get(topic, [])
            )
            for topic, question_count in current_blueprint.items()
        ]

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            results = list(
                executor.map(
                    process_topic,
                    tasks
                )
            )

        for mcqs in results:
            
            for mcq in mcqs:
                topic = mcq["topic"]
                generated_history.setdefault(topic,[]).append(mcq["question"])
            all_mcqs.extend(mcqs)

        result = deduplicate_mcqs(
            all_mcqs,
            blueprint
        )
        

        all_mcqs = result["mcqs"]
        current_blueprint = result["missing_topics"]

        logger.info("=" * 50)
        logger.info("Remaining Topics")
        logger.info(current_blueprint)

        logger.info("=" * 50)
        logger.info("Question History")
        logger.info(generated_history)

        if not current_blueprint:
            break

        attempt += 1

    return all_mcqs[:target_questions]