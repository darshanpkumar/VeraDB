import os
from backend.services.pdf_service import extract_text
from backend.services.chunking_service import chunk_text

# 1. Check if the testing file exists to prevent path faults
if not os.path.exists("backend/sample.pdf"):
    print("❌ Error: Place a file named 'sample.pdf' in the project root folder first!")
else:
    # 2. Execute extraction
    raw_text = extract_text("backend/sample.pdf")
    print(f"✅ Extracted character count length: {len(raw_text)}")
    
    # 3. Execute text chunking
    text_chunks = chunk_text(raw_text, chunk_size=500)
    print(f"✅ Generated number of chunk blocks: {len(text_chunks)}")
    
    if text_chunks:
        print("\n--- First Parsed Chunk Content Slice Preview ---")
        print(text_chunks[0][:200] + "...")