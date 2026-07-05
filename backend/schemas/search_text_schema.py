from pydantic import BaseModel

class SearchTextRequest(BaseModel):
    text: str