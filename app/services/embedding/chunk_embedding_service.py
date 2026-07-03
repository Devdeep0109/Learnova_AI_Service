from app.services.embedding.embedding_service import embeddings
from app.utils.logger import logger


def embed_chunks(chunks):

    logger.info(f"Generating embeddings for {len(chunks)} chunks.")
    try:
        vectors = embeddings.embed_documents(chunks)
        logger.info("Chunk embeddings generated successfully.")
        return vectors

    except Exception:
        logger.exception("Failed to generate chunk embeddings.")
        raise