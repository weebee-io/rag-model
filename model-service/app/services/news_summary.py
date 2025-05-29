import asyncio
from openai import AsyncOpenAI
from typing import List, Dict

from app.core.config import settings
from app.services.prompt import (
    build_keyword_extraction_prompt,
    build_news_summary_prompt,
    build_keyword_explanation_prompt_with_context,
    build_llm_fallback_prompt,
)
from app.services.retriever import SearchService

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def extract_keywords(text: str) -> List[str]:
    """
    뉴스 본문에서 금융/경제 관련 주요 키워드를 추출합니다.
    """
    prompt = build_keyword_extraction_prompt(text)
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    keyword_str = response.choices[0].message.content.strip()
    return [k.strip() for k in keyword_str.split(",") if k.strip()]

async def get_keyword_explanation(keyword: str) -> str:
    """
    각 키워드에 대해, 검색 결과(hit)가 있으면 그 내용을 중심으로 LLM에게 설명을 생성합니다.
    검색 결과가 없으면 LLM에게 일반 설명을 요청합니다.
    """
    search = SearchService()
    hits = await search.fetch(keyword, top_k=2)
    if hits:
        # 검색 결과 텍스트들을 하나로 합침
        context = "\n".join(h['text'].strip().replace("\n", " ") for h in hits)
        # 검색 결과를 포함한 프롬프트로 LLM에게 설명 생성 요청
        prompt = build_keyword_explanation_prompt_with_context(keyword, context)
    else:
        # 검색 결과가 없으면 일반 설명 프롬프트 사용
        prompt = build_llm_fallback_prompt(keyword)
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

async def summarize_news(content: str) -> Dict:
    """
    뉴스 본문을 요약하고, 주요 키워드 및 각 키워드의 개념 설명을 반환합니다.
    """
    # 1. 키워드 추출
    keywords = await extract_keywords(content)

    # 2. 뉴스 요약 생성
    summary_prompt = build_news_summary_prompt(content, keywords)
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.3,
    )
    summary = response.choices[0].message.content.strip()

    # 3. 각 키워드별 설명 생성 (검색 결과 활용)
    explanations = await asyncio.gather(
        *[get_keyword_explanation(k) for k in keywords]
    )

    # 4. 출력 형식 맞춰 반환
    return {
        "summary": summary,
        "keywords": keywords,
        "explanation": "\n".join(explanations)
    }