import math


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """
    Computes Cosine Similarity between two vectors.
    """

    if len(v1) != len(v2):
        raise ValueError("Vectors must have same dimensions.")

    dot_product = 0.0
    magnitude_a = 0.0
    magnitude_b = 0.0

    for a, b in zip(v1, v2):
        dot_product += a * b
        magnitude_a += a * a
        magnitude_b += b * b

    magnitude_a = math.sqrt(magnitude_a)
    magnitude_b = math.sqrt(magnitude_b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)