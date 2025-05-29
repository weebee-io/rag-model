from openai import AsyncOpenAI
from typing import List, Dict, Any
from app.core.config import settings
from app.services.retriever import SearchService
from app.services.prompt import build_keyword_extraction_prompt, build_qa_prompt
from app.models.schemas import QAExplanationResponse, QAChoice

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def extract_keywords(text: str) -> List[str]:
    prompt = build_keyword_extraction_prompt(text)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    keyword_str = response.choices[0].message.content.strip()
    return [k.strip() for k in keyword_str.split(",") if k.strip()]

async def answer_with_explanation(question: str, choices: List[str], mode: str = "dense", top_k: int = 5) -> Dict[str, Any]:
    search = SearchService()

    full_text = f"{question}\n보기:\n" + "\n".join(f"- {c}" for c in choices)
    keywords = await extract_keywords(full_text)
    keyword_query = ", ".join(keywords)
    hits = await search.fetch(keyword_query, mode=mode, top_k=top_k)
    prompt = build_qa_prompt(question=full_text, hits=hits)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    answer_text = response.choices[0].message.content.strip()

    return {
        "answer": answer_text,
        "keywords": keywords,
        # "sources": hits  # 원할 경우 사용
    }
