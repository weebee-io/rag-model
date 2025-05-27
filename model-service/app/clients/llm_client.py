# app/clients/llm_client.py
import openai
from app.core.config import settings

openai.api_key = settings.openai_api_key

async def generate(prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
    resp = await openai.ChatCompletion.acreate(
        model=settings.llm_model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp.choices[0].message.content.strip()