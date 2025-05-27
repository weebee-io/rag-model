# app/api/v1/routers/chat.py
from fastapi import APIRouter, HTTPException
from app.api.v1.schemas import ChatRequest, ChatResponse
from app.services.rag_chain import run_rag_chain

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        answer = await run_rag_chain(req.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))