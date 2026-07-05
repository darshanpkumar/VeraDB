from fastapi import APIRouter

from backend.database.vector_db import VectorDB
from backend.models.vector_item import VectorItem
from backend.schemas.vector_schema import VectorRequest, SearchRequest

router = APIRouter()

# Create a single global database instance that stays alive with the server
db = VectorDB()

@router.get("/")
def home():
    return {
        "message": "Welcome to VeraDB 🚀"
    }

@router.post("/insert")
def insert_vector(request: VectorRequest):
    # 1. Map incoming JSON validation fields to our structural class entity
    vector = VectorItem(
        id=request.id,
        vector=request.vector
    )
    
    # 2. Inject it cleanly into the parallel orchestration indexing layer
    db.insert(vector)
    
    return {
        "message": "Vector inserted successfully."
    }

@router.post("/search")
def search_vector(request: SearchRequest):
    # 1. Dispatch search details down into our unified database routing manager
    results = db.search(
        query_vector=request.query,
        algorithm=request.algorithm
    )
    
    response = []
    
    # 2. Extract item details out of returned matches (handling fallback formats gracefully)
    if isinstance(results, list):
        for res in results:
            # Check if engine returned (item, score) tuples or raw VectorItems
            if isinstance(res, tuple):
                item, score = res[0], res[1]
            else:
                item, score = res, 0.0
                
            response.append({
                "id": item.id,
                "score": score
            })
    elif results is not None:
        response.append({
            "id": results.id,
            "score": 0.0
        })
        
    return response

@router.get("/stats")
def stats():
    """
    Retrieve live health metrics, index statuses, and internal entry point profiles.
    """
    return db.get_statistics()


@router.delete("/delete/{vector_id}")
def delete_vector(vector_id: int):
    """
    Remove a vector point permanently across active in-memory collections.
    """
    # Filter the master vector record list inline via list comprehension
    db.vectors = [
        v for v in db.vectors
        if v.id != vector_id
    ]
    
    return {
        "message": "Vector deleted successfully."
    }


@router.get("/algorithms")
def algorithms():
    """
    Expose active index configurations and geometric distance frameworks supported by the engine.
    """
    return {
        "algorithms": [
            "brute_force",
            "kd_tree",
            "hnsw"
        ],
        "metrics": [
            "euclidean",
            "manhattan",
            "cosine"
        ]
    }