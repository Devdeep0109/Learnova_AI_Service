from app.services.embedding.embedding_service import embeddings
from app.utils.logger import logger


def embed_topics(topic_names):

    logger.info(f"Generating embeddings for {len(topic_names)} topics.")
    try:
        vectors = embeddings.embed_documents(topic_names)
        logger.info("Topic embeddings generated successfully.")
        return vectors

    except Exception:
        logger.exception("Failed to generate topic embeddings.")
        raise