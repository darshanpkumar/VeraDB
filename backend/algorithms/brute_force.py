from backend.models.vector_item import VectorItem

class BruteForceSearch:
    """
    Brute Force Nearest Neighbor Search.

    Compares the query vector with every vector
    stored in the database.
    """

    def search(
        self,
        vectors: list[VectorItem],
        query_vector: list[float],
        metric,
        top_k: int = 5,
        reverse: bool = True
    ):
        results = []

        for vector_item in vectors:
            score = metric(query_vector, vector_item.vector)
            results.append((vector_item, score))
        
        results.sort(
        key=lambda item: item[1],
        reverse=reverse
        )

        return results[:top_k]

