# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.chat import router as chat_router

app = FastAPI(title="RAG Service", version="0.1.0")

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])