from backend.models.vector_item import VectorItem
from backend.metrics.euclidean import euclidean_distance


class KDNode:
    """
    Represents a single node in the KD-Tree.
    """

    def __init__(
        self,
        vector_item: VectorItem,
        axis: int
    ):
        self.vector_item = vector_item
        self.axis = axis

        self.left = None
        self.right = None


class KDTree:
    """
    KD-Tree implementation for nearest neighbor search.
    """

    def __init__(
        self,
        vectors: list[VectorItem]
    ):
        self.root = None
        self.best = None
        self.best_distance = float("inf")

        if vectors:
            self.root = self.build_tree(vectors, depth=0)

    def build_tree(
        self,
        vectors: list[VectorItem],
        depth: int
    ):
        if not vectors:
            return None

        dimensions = len(vectors[0].vector)
        axis = depth % dimensions

        vectors.sort(
            key=lambda item: item.vector[axis]
        )

        median = len(vectors) // 2

        node = KDNode(
            vector_item=vectors[median],
            axis=axis
        )

        node.left = self.build_tree(
            vectors[:median],
            depth + 1
        )

        node.right = self.build_tree(
            vectors[median + 1:],
            depth + 1
        )

        return node

    def search(self, query_vector):
        self.best = None
        self.best_distance = float("inf")

        self._search_recursive(
            self.root,
            query_vector
        )

        return self.best, self.best_distance

    def _search_recursive(
        self,
        node,
        query_vector
    ):
        if node is None:
            return

        distance = euclidean_distance(
            query_vector,
            node.vector_item.vector
        )

        if distance < self.best_distance:
            self.best_distance = distance
            self.best = node.vector_item

        axis = node.axis

        if query_vector[axis] < node.vector_item.vector[axis]:
            next_branch = node.left
            opposite_branch = node.right
        else:
            next_branch = node.right
            opposite_branch = node.left

        self._search_recursive(
            next_branch,
            query_vector
        )

        if abs(query_vector[axis] - node.vector_item.vector[axis]) < self.best_distance:
            self._search_recursive(
                opposite_branch,
                query_vector
            )