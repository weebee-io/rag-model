from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm import generate_answer
from app.services.prompt import build_prompt

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    prompt = build_prompt(request.question)
    answer = generate_answer(prompt)
    return ChatResponse(answer=answer)