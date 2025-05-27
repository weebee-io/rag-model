# app/services/retriever.py
from app.clients.search_client import search

async def retrieve(question: str, mode: str = None, top_k: int = None):
    return await search(q=question, mode=mode, top_k=top_k)