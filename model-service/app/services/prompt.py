def build_prompt(user_input: str) -> str:
    return f"Answer the following question concisely:\n{user_input}"


# models/schemas.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str