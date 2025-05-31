from typing import List
from ..api.v1.schemas import Hit

class RetrieverStrategy:
    async def search(self, query: str, top_k: int) -> List[Hit]:
        """검색 결과를 Hit 리스트로 반환"""
        raise NotImplementedError
