def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """
    Slices long continuous document strings into small discrete content 
    passages matching the target character count parameters.
    """
    chunks = []
    
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
        
    return chunks