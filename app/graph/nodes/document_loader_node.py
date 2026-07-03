from app.services.retrieval.chroma_service import chroma_service


def document_loader_node(state):

    document = chroma_service.get_document(
        state["document_id"]
    )

    return {
        "chunks": document["chunks"]
    }