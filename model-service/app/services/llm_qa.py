# app/services/qa.py
from typing import Dict, List, Any

from openai import AsyncOpenAI
from app.core.config import settings
from .retriever import SearchService
from .prompt import build_qa_prompt   # ← 여기만 추가/변경

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def answer_question(
    q: str,
    mode: str = "dense",
    top_k: int = 5,
) -> Dict[str, Any]:
    search = SearchService()
    hits: List[dict] = await search.fetch(q, mode=mode, top_k=top_k)

    # 검색 결과가 없으면 즉시 회신
    # if not hits:
    #     return {"answer": "잘모르겠습니다", "sources": []}

    # 🔹 프롬프트를 외부 모듈에서 빌드
    prompt = build_qa_prompt(question=q, hits=hits)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    answer_text = response.choices[0].message.content.strip()

    return {"answer": answer_text, "sources": hits}
