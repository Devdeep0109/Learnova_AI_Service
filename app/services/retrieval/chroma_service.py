import uuid

import chromadb
from chromadb.config import Settings


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="storage/chroma_db",
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="learnova_documents"
        )

    def add_document(
        self,
        filename,
        chunks,
        embeddings
    ):

        document_id = str(
            uuid.uuid4()
        )

        ids = []
        metadatas = []

        for index in range(len(chunks)):

            ids.append(f"{document_id}_{index}")
            metadatas.append(
                {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": index
                }
            )

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return document_id

    def get_document(
        self,
        document_id: str
    ):

        result = self.collection.get(
            where={
                "document_id": document_id
            },
            include=[
                "documents",
                "embeddings"
            ]
        )

        return {
            "chunks": result["documents"],
            "embeddings": result["embeddings"]
        }

    def search_chunks(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int = 3
    ):

        result = self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

            where={
                "document_id": document_id
            }

        )

        documents = result.get(
            "documents",
            []
        )

        if not documents:
            return []

        return documents[0]


chroma_service = ChromaService()