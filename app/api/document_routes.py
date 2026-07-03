from fastapi import APIRouter, UploadFile, File
import os

from app.services.document.pdf_service import extract_text_from_pdf
from app.services.document.chunk_service import create_chunks
from app.services.embedding.chunk_embedding_service import embed_chunks
from app.services.retrieval.chroma_service import chroma_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    pdf_data = extract_text_from_pdf(
        file_path
    )

    chunks = create_chunks(
        pdf_data["text"]
    )

    chunk_vectors = embed_chunks(
        chunks
    )

    # ChromaDB storage will be added next
    document_id = chroma_service.add_document(
        filename=file.filename,
        chunks=chunks,
        embeddings=chunk_vectors
    )

    return {
        "document_id": document_id,
        "message": "Document processed successfully."
    }