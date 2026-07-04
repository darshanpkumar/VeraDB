import unittest

from backend.algorithms.kdtree import KDTree
from backend.models.vector_item import VectorItem

class TestKDTree(unittest.TestCase):

    def setUp(self):
        self.vectors = [
            VectorItem(1, [2, 3]),
            VectorItem(2, [5, 4]),
            VectorItem(3, [9, 6]),
            VectorItem(4, [4, 7]),
            VectorItem(5, [8, 1]),
            VectorItem(6, [7, 2]),
        ]

        self.tree = KDTree(self.vectors)

    def test_root_exists(self):
        self.assertIsNotNone(self.tree.root)

    def test_root_axis(self):
        self.assertEqual(self.tree.root.axis, 0)

    def test_children_exist(self):
        self.assertIsNotNone(self.tree.root.left)
        self.assertIsNotNone(self.tree.root.right)

    def test_search_nearest_neighbor(self):
        query = [6, 3]
        best, distance = self.tree.search(query)
        self.assertEqual(best.id, 6)