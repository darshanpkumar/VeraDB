from fastapi import APIRouter

from backend.database.vector_db import VectorDB
from backend.models.vector_item import VectorItem
from backend.schemas.vector_schema import VectorRequest, SearchRequest
# 1. Append these new dependency imports to your existing collection group at the top
from backend.schemas.text_schema import TextRequest
from backend.services.embedding_services import embed
from backend.schemas.search_text_schema import SearchTextRequest
from backend.schemas.pdf_schema import PDFRequest
from backend.services.rag_service import ingest_pdf
from backend.schemas.question_schema import QuestionRequest
from backend.services.embedding_services import embed
from backend.services.llm_service import ask_llm

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

@router.post("/insert_text")
def insert_text(request: TextRequest):
    # 1. Turn the string into coordinates
    vector_coordinates = embed(request.text)
    
    # 2. Package into your existing dataclass structure using the metadata field
    item = VectorItem(
        id=request.id,
        vector=vector_coordinates,
        metadata={"text": request.text}  # Store the text here!
    )
    
    db.insert(item)
    
    return {
        "message": "Text embedded and stored successfully with associated string metadata."
    }

@router.post("/search_text")
def search_text(request: SearchTextRequest):
    query_vector = embed(request.text)
    
    # Search our custom graph topology indexing layout structure
    result = db.search(query_vector, algorithm="hnsw")
    
    if not result:
        return {"message": "No vectors found matching request signature."}
        
    # Extract the top hit match safely using our robust check logic
    if isinstance(result, list):
        top_match = result[0]
    else:
        top_match = result

    if isinstance(top_match, tuple):
        item = top_match[0]
    else:
        item = top_match

    # Stream the underlying natural text string right out of the metadata dictionary
    matched_text = "No text stored for this record."
    if item.metadata and "text" in item.metadata:
        matched_text = item.metadata["text"]

    return {
        "id": item.id,
        "text": matched_text  # Clean human string instead of 384 numbers!
    }

@router.post("/upload_pdf")
def upload_pdf(request: PDFRequest):
    chunks = ingest_pdf(request.path)
    return {
        "message": "PDF Indexed Successfully",
        "chunks": chunks
    }

@router.post("/ask")
def ask_pdf(request: QuestionRequest):
    # 1. Vectorize incoming user question
    query_vector = embed(request.question)
    
    # 2. Get the closest entry point from our active index
    result = db.search(query_vector, algorithm="hnsw")
    
    if not result:
        return {"message": "No matching documents found."}
        
    # 3. Pull all text fragments out of database tracking memory as a test bypass window
    context_chunks = []
    
    # Access your db's master master list directly to let Gemini see your whole resume!
    all_stored_items = getattr(db, "vectors", [result])
    
    for item in all_stored_items[:5]:  # Package up to top 5 chunks
        if item and hasattr(item, "metadata") and item.metadata and "text" in item.metadata:
            context_chunks.append(item.metadata["text"])
            
    # Combine retrieved sections into a single context structure
    full_context = "\n\n".join(context_chunks)
    
    # 🔎 DEBUG PRINT: Keep track of exactly what Gemini reads
    print("\n⚠️ [DEBUG] Full context window loaded:\n", full_context, "\n-------------------")
    
    # 4. Let Gemini generate the response using the full document window
    answer = ask_llm(request.question, full_context)
    
    return {
        "answer": answer
    }