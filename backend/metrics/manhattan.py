def manhattan_distance(v1: list[float], v2: list[float]) -> float:
    """
    Computes Manhattan Distance between two vectors.
    """

    if len(v1) != len(v2):
        raise ValueError("Vectors must have same dimensions.")

    distance = 0.0

    for a, b in zip(v1, v2):
        distance += abs(a - b)

    return distance