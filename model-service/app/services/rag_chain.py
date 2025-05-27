# app/services/rag_chain.py
from app.services.retriever import retrieve
from app.services.generator import generate_answer
from app.core.config import settings

async def run_rag_chain(question: str) -> str:
    hits = await retrieve(question, top_k=settings.max_context_docs)
    contexts = [hit.get('text') for hit in hits]
    return await generate_answer(question, contexts)