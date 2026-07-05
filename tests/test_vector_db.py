import unittest

from backend.database.vector_db import VectorDB
from backend.models.vector_item import VectorItem

class TestVectorDB(unittest.TestCase):
    
    def test_insert(self):
        db = VectorDB()
        
        db.insert(VectorItem(1, [1, 2]))
        db.insert(VectorItem(2, [2, 3]))
        
        self.assertEqual(len(db.vectors), 2)

    def test_statistics(self):
        db = VectorDB()
        
        db.insert(VectorItem(1, [1, 2]))
        stats = db.get_statistics()
        
        self.assertEqual(stats["vectors"], 1)