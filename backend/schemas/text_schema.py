from pydantic import BaseModel

class TextRequest(BaseModel):
    id: int
    text: str