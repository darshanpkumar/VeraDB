import unittest

from backend.algorithms.hnsw import HNSW
from backend.models.vector_item import VectorItem

class TestHNSW(unittest.TestCase):
    
    def test_insert(self):
        graph = HNSW()
        
        graph.insert(VectorItem(1, [1, 2]))
        graph.insert(VectorItem(2, [2, 3]))

    def test_search(self):
        graph = HNSW()
        
        graph.insert(VectorItem(1, [1, 2]))
        graph.insert(VectorItem(2, [2, 3]))
        graph.insert(VectorItem(3, [8, 8]))
        
        # A query near [2.1, 3.1] should match VectorItem 2 ([2, 3])
        result = graph.search([2.1, 3.1])
        
        self.assertEqual(result.id, 2)