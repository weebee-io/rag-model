from .base import RetrieverStrategy
from ..clients.elastic import es_client
from ..api.v1.schemas import Hit
from ..core.config import settings
import re

class TestBM25Retriever(RetrieverStrategy):
    async def search(self, query: str, top_k: int):
        # 1. 검색어 전처리 (예: 조사/감탄사/불용어 제거)
        query_clean = self.preprocess_query(query)

        # 2. Elasticsearch 쿼리 구성 (nori_analyzer 기반 + 확장)
        body = {
            "size": top_k,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "text": {
                                    "query": query_clean,
                                    "analyzer": "nori_analyzer",
                                    "boost": 2  # 가중치 강화
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                "text": {
                                    "query": query_clean,
                                    "analyzer": "nori_analyzer",
                                    "boost": 1.5
                                }
                            }
                        },
                        {
                            "multi_match": {
                                "query": query_clean,
                                "fields": ["meta.keywords"],
                                "analyzer": "nori_analyzer",
                                "boost": 1
                            }
                        }
                    ],
                    "minimum_should_match": 1  # 하나 이상 매칭만 되어도 통과
                }
            }
        }

        # 3. 검색 수행
        resp = await es_client.search(index=settings.index_name, body=body)
        return [
            Hit(
                doc_id=hit["_id"],
                score=hit["_score"],
                text=hit["_source"]["text"]
            )
            for hit in resp["hits"]["hits"]
        ]

    def preprocess_query(self, query: str) -> str:
        # "채권이 뭐야?" → "채권"
        query = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", query)  # 특수문자 제거
        query = re.sub(r"\b(뭐야|알려줘|이란|이게|어때)\b", "", query)  # 자주 쓰는 질문형 조사 제거
        return query.strip()
