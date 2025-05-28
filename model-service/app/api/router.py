from fastapi import APIRouter
from app.api import chat
from .qa import router as qa_router
from app.api import answer

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

api_router.include_router(qa_router, prefix="/qa", tags=["QA"])
api_router.include_router(answer.router, prefix="/answer", tags=["Answer"])
