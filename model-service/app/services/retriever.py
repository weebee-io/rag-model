# app/services/retriever.py
from typing import List, Dict
import httpx


class SearchService:
    """
    search-service(127.0.0.1:8001/v1/search)와 통신해
    질문에 대한 청크(hits)를 비동기로 받아옵니다.
    """

    BASE_URL = "http://127.0.0.1:8001/v1/search"

    async def fetch(
        self,
        q: str,
        mode: str = "dense",
        top_k: int = 5,
        timeout: float = 10.0,
    ) -> List[Dict]:
        params = {"q": q, "mode": mode, "top_k": str(top_k)}

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(self.BASE_URL, params=params)
            resp.raise_for_status()

        data = resp.json()
        # search-service 측 스키마: {"hits":[{doc_id,score,text}, ...]}
        return data.get("hits", [])
