import fitz  # PyMuPDF engine layer

def extract_text(pdf_path: str) -> str:
    """
    Opens a localized PDF document file pathway and crawls every 
    page sequential grid layout to parse out its raw text characters.
    """
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text()
        
    return text