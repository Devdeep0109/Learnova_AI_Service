from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(vector1, vector2):

    similarity = cosine_similarity(
        [vector1],
        [vector2]
    )

    return float(similarity[0][0])