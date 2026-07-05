from sentence_transformers import SentenceTransformer

# Load the industry-standard all-MiniLM-L6-v2 model exactly once on initialization
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str) -> list[float]:
    """
    Transforms a natural language string input into a high-dimensional mathematical 
    dense vector array containing 384 feature coordinates.
    """
    # Generate the numpy array embeddings and transform directly into a standard list of floats
    return model.encode(text).tolist()