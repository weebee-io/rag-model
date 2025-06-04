from openai import AsyncOpenAI
import asyncio
from typing import List, Dict

from app.core.config import settings
from app.services.retriever import SearchService
from app.services.prompt_main import (
    keyword_prompt,
    build_no_chunks_prompt,
    build_keyword_explanation,
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



async def get_answer(text: str, keyword: str) -> str:
    """
    1) 검색 결과(hits)가 있으면 → context로 합쳐 LLM에 전달
    2) 없으면 → fallback 프롬프트로 LLM 호출
    """
    search = SearchService()
    hits = await search.fetch(keyword, top_k=3)           # top_k 자유 조정

    if hits:
        context = hits_to_context(hits)                   # 텍스트 병합
        prompt = build_keyword_explanation(
            keyword=keyword,
            context=context,
        )
    else:
        prompt = build_no_chunks_prompt(keyword)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


async def get_keyword_explanation(text: str, keyword: str) -> str:
    """
    1) 검색 결과(hits)가 있으면 → context로 합쳐 LLM에 전달
    2) 없으면 → fallback 프롬프트로 LLM 호출
    """
    search = SearchService()
    hits = await search.fetch(keyword, top_k=3)           # top_k 자유 조정

    if hits:
        context = hits_to_context(hits)                   # 텍스트 병합
        prompt = build_keyword_explanation(
            keyword=keyword,
            context=context,
        )
    else:
        prompt = build_no_chunks_prompt(keyword)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()



async def generate_hint(question: str, choices: List[str]) -> Dict:
    """
    주어진 질문과 선택지로부터 키워드를 추출하고,
    각 키워드에 대한 개념 설명을 생성합니다.
    """
    full_text = f"{question}\n보기:\n" + "\n".join(f"- {c}" for c in choices)
    keywords = await extract_keywords(full_text)

    explanations = await asyncio.gather(
        *[get_keyword_explanation(k) for k in keywords]
    )

    hint_text = "\n".join(explanations)
    return {"keywords": keywords, "hint": hint_text}