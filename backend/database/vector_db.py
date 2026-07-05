from backend.algorithms.brute_force import BruteForceSearch
from backend.algorithms.kdtree import KDTree
from backend.algorithms.hnsw import HNSW

from backend.models.vector_item import VectorItem

class VectorDB:
    
    def __init__(self):
        self.vectors = []
        self.brute_force = BruteForceSearch()
        self.kdtree = None
        self.hnsw = HNSW()

    def insert(self, vector_item: VectorItem):
        # 1. Track the element in our primary master record list
        self.vectors.append(vector_item)
        
        # 2. Rebuild the KD-Tree structure completely from the new collection array
        self.kdtree = KDTree(self.vectors)
        
        # 3. Stream the entry dynamically into our continuous HNSW graph
        self.hnsw.insert(vector_item)

    def insert_many(self, vectors: list[VectorItem]):
        for vector in vectors:
            self.insert(vector)

    def search(self, query_vector: list[float], algorithm: str = "brute_force"):
        if algorithm == "brute_force":
            return self.brute_force.search(self.vectors, query_vector)
            
        elif algorithm == "kdtree":
            return self.kdtree.search(query_vector)
            
        elif algorithm == "hnsw":
            return self.hnsw.search(query_vector)
            
        else:
            raise ValueError("Unknown search algorithm.")

    def get_statistics(self) -> dict:
        return {
            "vectors": len(self.vectors),
            "kdtree": self.kdtree is not None,
            "hnsw_nodes": len(self.hnsw.nodes)
        }