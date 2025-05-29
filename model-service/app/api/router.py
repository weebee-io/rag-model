from fastapi import APIRouter
from app.api import chat
from .qa import router as qa_router
from app.api import answer
from app.api import test_qa
from app.api.router_hint_news import router as ai_router

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

api_router.include_router(qa_router, prefix="/qa", tags=["QA"])
api_router.include_router(answer.router, prefix="/answer", tags=["Answer"])
api_router.include_router(test_qa.router, prefix="/test_qa", tags=["Test QA"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Assist"])