from fastapi import APIRouter
from app.api import qa_main, hint_main, news_main


api_router = APIRouter()

api_router.include_router(qa_main.router, prefix="/qa", tags=["QA Main"])
api_router.include_router(hint_main.router, prefix="/hint", tags=["Hint Main"])
api_router.include_router(news_main.router, prefix="/news", tags=["News Main"])