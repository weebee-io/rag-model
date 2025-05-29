import asyncio
from openai import AsyncOpenAI
from typing import List, Dict

from app.core.config import settings
from app.services.retriever import SearchService
from app.services.prompt import (
    build_keyword_extraction_prompt,
    build_llm_fallback_prompt,
)

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


async def get_keyword_explanation(keyword: str) -> str:
    search = SearchService()
    hits = await search.fetch(keyword, top_k=1)

    if hits:
        text = hits[0]['text'].strip().replace("\n", " ")
        return f"[{keyword}: {text[:150]}...]"
    else:
        prompt = build_llm_fallback_prompt(keyword)
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()


async def generate_hint(question: str, choices: List[str]) -> Dict:
    full_text = f"{question}\n보기:\n" + "\n".join(f"- {c}" for c in choices)
    keywords = await extract_keywords(full_text)

    explanations = await asyncio.gather(
        *[get_keyword_explanation(k) for k in keywords]
    )

    hint_text = "\n".join(explanations)
    return {"keywords": keywords, "hint": hint_text}
