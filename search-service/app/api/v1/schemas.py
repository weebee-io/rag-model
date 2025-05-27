from pydantic import BaseModel
from typing import List

class Hit(BaseModel):
    doc_id: str
    score: float
    text: str

class SearchResponse(BaseModel):
    query: str
    mode: str
    hits: List[Hit]
