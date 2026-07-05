import math
import random

from backend.models.vector_item import VectorItem
from backend.metrics.euclidean import euclidean_distance

class HNSWNode:
    """
    Represents one node in the HNSW graph.
    """
    
    def __init__(
        self,
        vector_item: VectorItem,
        level: int
    ):
        self.vector_item = vector_item
        self.level = level
        
        # neighbors[level] = list of connected nodes
        self.neighbors = {
            i: [] for i in range(level + 1)
        }


class HNSW:
    """
    Hierarchical Navigable Small World Graph.
    """
    
    def __init__(
        self,
        max_connections: int = 8
    ):
        self.entry_point = None
        self.max_level = -1
        self.max_connections = max_connections
        self.nodes = []

    def random_level(self, probability: float = 0.5) -> int:
        """
        Generate a random level for a new node.
        """
        level = 0
        while random.random() < probability:
            level += 1
        return level

    def connect_nodes(self, node1: HNSWNode, node2: HNSWNode, level: int):
        """
        Connect two nodes at a given level.
        """
        if node2 not in node1.neighbors[level]:
            node1.neighbors[level].append(node2)
            
        if node1 not in node2.neighbors[level]:
            node2.neighbors[level].append(node1)

    def distance(self, node: HNSWNode, query_vector: list[float]) -> float:
        """
        Calculate the Euclidean distance between a node's vector and the query vector.
        """
        return euclidean_distance(
            node.vector_item.vector,
            query_vector
        )

    def insert(self, vector_item: VectorItem):
        level = self.random_level()
        node = HNSWNode(
            vector_item,
            level
        )
        self.nodes.append(node)

        # Handle the First Node case
        if self.entry_point is None:
            self.entry_point = node
            self.max_level = level
            return

        # Update Global Highest Level if this node surpasses it
        if level > self.max_level:
            self.max_level = level
            self.entry_point = node

        # Step 2: Connections routed cleanly through the new connect_nodes function
        for existing in self.nodes[:-1]:
            max_shared_level = min(
                existing.level,
                node.level
            )
            
            for l in range(max_shared_level + 1):
                self.connect_nodes(existing, node, l)

    def search_layer(self, query_vector: list[float], entry_node: HNSWNode, level: int) -> HNSWNode:
        """
        Search a single HNSW layer using a greedy local neighbor check.
        """
        current = entry_node
        current_distance = self.distance(current, query_vector)
        
        changed = True
        while changed:
            changed = False
            
            # Scan all neighbors specifically on this layer level
            for neighbor in current.neighbors[level]:
                distance = self.distance(neighbor, query_vector)
                
                # If a neighbor gets us strictly closer to the target, move there
                if distance < current_distance:
                    current = neighbor
                    current_distance = distance
                    changed = True
                    
        return current

    def greedy_search(self, query_vector: list[float]):
        """
        Search from the highest graph layer down to layer 0.
        """
        if self.entry_point is None:
            return None
            
        current = self.entry_point
        
        # Walk down from the highest express layer to layer 0
        for level in range(self.max_level, -1, -1):
            current = self.search_layer(query_vector, current, level)
            
        return current.vector_item

    def search(self, query_vector: list[float]):
        """
        Public search execution layer.
        """
        return self.greedy_search(query_vector)