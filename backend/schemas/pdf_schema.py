from pydantic import BaseModel

class PDFRequest(BaseModel):
    path: str