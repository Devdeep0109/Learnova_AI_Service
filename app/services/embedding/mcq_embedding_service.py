from app.services.embedding.embedding_service import embeddings
from app.utils.logger import logger


def embed_questions(questions):

    logger.info(f"Generating embeddings for {len(questions)} questions.")
    try:
        vectors = embeddings.embed_documents(questions)
        logger.info("Question embeddings generated successfully.")
        return vectors

    except Exception:
        logger.exception("Failed to generate question embeddings.")
        raise