import unittest
import math

from backend.metrics.euclidean import euclidean_distance
from backend.metrics.manhattan import manhattan_distance
from backend.metrics.cosine import cosine_similarity

class TestMetrics(unittest.TestCase):

    def setUp(self):
        # Sample vectors for testing
        self.v1 = [1.0, 2.0, 3.0]
        self.v2 = [4.0, 5.0, 6.0]
        self.zero_vector = [0.0, 0.0, 0.0]
        self.mismatched_vector = [1.0, 2.0]

    ## -----------------------------------------------------------------
    ## Cosine Similarity Tests
    ## -----------------------------------------------------------------
    def test_cosine_similarity_identical(self):
        # Identical vectors should have a similarity of 1.0
        self.assertAlmostEqual(cosine_similarity(self.v1, self.v1), 1.0, places=5)

    def test_cosine_similarity_calculated(self):
        # Hand-calculated or known true value test
        # dot_product = 1*4 + 2*5 + 3*6 = 32
        # mag_v1 = sqrt(1+4+9) = sqrt(14) ≈ 3.741657
        # mag_v2 = sqrt(16+25+36) = sqrt(77) ≈ 8.774964
        # expected = 32 / (sqrt(14) * sqrt(77)) ≈ 0.9746318
        expected = 32 / (math.sqrt(14) * math.sqrt(77))
        self.assertAlmostEqual(cosine_similarity(self.v1, self.v2), expected, places=5)

    def test_cosine_similarity_zero_vector(self):
        # Your code handles division by zero by returning 0.0
        self.assertEqual(cosine_similarity(self.v1, self.zero_vector), 0.0)

    def test_cosine_similarity_dimension_mismatch(self):
        # Verifies the ValueError is raised for dimension mismatch
        with self.assertRaises(ValueError):
            cosine_similarity(self.v1, self.mismatched_vector)

    ## -----------------------------------------------------------------
    ## Euclidean Distance Tests
    ## -----------------------------------------------------------------
    def test_euclidean_distance(self):
        # d = sqrt((1-4)^2 + (2-5)^2 + (3-6)^2) = sqrt(9 + 9 + 9) = sqrt(27) ≈ 5.19615
        expected = math.sqrt(27)
        self.assertAlmostEqual(euclidean_distance(self.v1, self.v2), expected, places=5)

    def test_euclidean_distance_mismatch(self):
        with self.assertRaises(ValueError):
            euclidean_distance(self.v1, self.mismatched_vector)

    ## -----------------------------------------------------------------
    ## Manhattan Distance Tests
    ## -----------------------------------------------------------------
    def test_manhattan_distance(self):
        # d = |1-4| + |2-5| + |3-6| = 3 + 3 + 3 = 9.0
        self.assertAlmostEqual(manhattan_distance(self.v1, self.v2), 9.0, places=5)

    def test_manhattan_distance_mismatch(self):
        with self.assertRaises(ValueError):
            manhattan_distance(self.v1, self.mismatched_vector)

if __name__ == '__main__':
    unittest.main()