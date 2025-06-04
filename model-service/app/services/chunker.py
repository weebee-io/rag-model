# app/services/chunker.py
from __future__ import annotations

from typing import List, Dict

from app.services.retriever import SearchService


async def fetch_hits(keyword: str, *, top_k: int = 3) -> List[Dict]:
    """
    지정한 키워드를 Elasticsearch(또는 SearchService)로 검색해 top-k 결과를 가져온다.
    반환값 예시: [{'text': '…'}, …]
    """
    search = SearchService()
    return await search.fetch(keyword, top_k=top_k)


def hits_to_context(hits: List[Dict]) -> str:
    """
    다수의 검색 결과(hits)를 하나의 문맥(Context) 문자열로 합친다.
    - 개행을 공백으로 치환해 LLM 프롬프트가 길어지는 것을 방지
    """
    return "\n".join(
        h["text"].strip().replace("\n", " ") for h in hits
    )
