from app.services.question.generation_service import generate_complete_test


def mcq_generation_node(state):

    mcqs = generate_complete_test(

        blueprint=state["blueprint"],

        difficulty=state["difficulty"],

        document_id=state["document_id"]

    )

    return {
        "mcqs": mcqs
    }