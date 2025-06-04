import asyncio
from openai import AsyncOpenAI
from typing import List, Dict

from app.core.config import settings
from app.services.retriever import SearchService
from app.services.prompt_main import (
    keyword_prompt,
    build_news_prompt,
    build_news_rag_prompt,
    build_news_llm_prompt,
)
from app.services.chunker import hits_to_context

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def extract_keywords(text: str) -> List[str]:
    prompt = keyword_prompt(text)
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    keyword_str = response.choices[0].message.content.strip()
    return [k.strip() for k in keyword_str.split(",") if k.strip()]



async def generate_summary(news: str) -> str:
    keywords = await extract_keywords(news)

    if not keywords:                       # 키워드가 없으면 곧바로 LLM으로
        prompt = build_news_prompt(news)
        resp = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return {"answer": resp.choices[0].message.content.strip()}

    # 1. 키워드 추출
    keywords_str = ", ".join(keywords)

    # 2. 키워드 전체를 검색 쿼리로 사용하여 관련 청크를 한 번에 받아옴
    search = SearchService()
    hits = await search.fetch(keywords_str, top_k=5)  # top_k는 필요에 따라 조정

    if hits:
        context = hits_to_context(hits)                   # 텍스트 병합
        prompt = build_news_rag_prompt(
            text=news,
            keyword=keywords,
            context=context,
        )
    else:
        prompt = build_news_llm_prompt(news, keywords)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()
 

    return {"summary": summary}
