import unittest
from backend.models.vector_item import VectorItem
from backend.algorithms.brute_force import BruteForceSearch
from backend.metrics.cosine import cosine_similarity
from backend.metrics.euclidean import euclidean_distance
from backend.metrics.manhattan import manhattan_distance

class TestBruteForceSearch(unittest.TestCase):

    def setUp(self):
        self.searcher = BruteForceSearch()
        
        # Sample database vectors as VectorItem objects
        self.vectors = [
            VectorItem(id=1, vector=[1.0, 2.0, 3.0]),
            VectorItem(id=2, vector=[4.0, 5.0, 6.0]),
            VectorItem(id=3, vector=[1.1, 2.1, 3.1]),
            VectorItem(id=4, vector=[0.0, 0.0, 0.0])
        ]
        self.query = [1.0, 2.0, 2.9]

    def test_search_with_euclidean(self):
        # Euclidean: Lower distance is closer. For ascending order, reverse=False.
        # Vector 1 [1, 2, 3] is clearly the closest to [1, 2, 2.9].
        results = self.searcher.search(
            vectors=self.vectors,
            query_vector=self.query,
            metric=euclidean_distance,
            top_k=2,
            reverse=False
        )
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0].id, 1)  # Best match should be ID 1
        self.assertEqual(results[1][0].id, 3)  # Second best should be ID 3

    def test_search_with_manhattan(self):
        # Manhattan: Lower distance is closer. For ascending order, reverse=False.
        results = self.searcher.search(
            vectors=self.vectors,
            query_vector=self.query,
            metric=manhattan_distance,
            top_k=1,
            reverse=False
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].id, 1)

    def test_search_with_cosine(self):
        # Cosine: Higher similarity score is closer. For descending order, reverse=True.
        results = self.searcher.search(
            vectors=self.vectors,
            query_vector=self.query,
            metric=cosine_similarity,
            top_k=2,
            reverse=True
        )
        
        self.assertEqual(len(results), 2)
        # ID 1 and ID 3 point in almost the exact same direction as the query
        self.assertIn(results[0][0].id, [1, 3]) 

    def test_search_top_k_limit(self):
        # Verify that requesting top_k=2 returns exactly 2 elements
        results = self.searcher.search(
            vectors=self.vectors,
            query_vector=self.query,
            metric=euclidean_distance,
            top_k=2,
            reverse=False
        )
        self.assertEqual(len(results), 2)

if __name__ == '__main__':
    unittest.main()