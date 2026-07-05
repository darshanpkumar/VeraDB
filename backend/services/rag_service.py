from backend.services.pdf_service import extract_text
from backend.services.chunking_service import chunk_text
from backend.services.embedding_services import embed
from backend.models.document import Document
from backend.models.vector_item import VectorItem

def ingest_pdf(pdf_path):
    from backend.routes.vector_routes import db 
    
    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    
    for i, chunk in enumerate(chunks):
        vector = embed(chunk)
        
        # Package everything into a single VectorItem using the metadata field!
        item = VectorItem(
            id=i,
            vector=vector,
            metadata={"text": chunk}
        )
        
        db.insert(item)
        
    return len(chunks)