from pydantic import BaseModel

class VectorRequest(BaseModel):
    id: int
    vector: list[float]

class SearchRequest(BaseModel):
    query: list[float]
    algorithm: str = "hnsw"
    metric: str = "cosine"
    top_k: int = 5