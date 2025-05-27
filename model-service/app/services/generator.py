# app/services/generator.py
from app.clients.llm_client import generate

async def generate_answer(question: str, contexts: list) -> str:
    context_str = "\n---\n".join(contexts)
    prompt = f"Use the following context to answer the question:\n{context_str}\nQuestion: {question}\nAnswer:"
    return await generate(prompt)