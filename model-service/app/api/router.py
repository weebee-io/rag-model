from fastapi import APIRouter
from app.api import chat
from .qa import router as qa_router

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

api_router.include_router(qa_router, prefix="/qa", tags=["QA"])
