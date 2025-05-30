from .base import RetrieverStrategy
from ..clients.elastic import es_client
from ..api.v1.schemas import Hit
from ..core.config import settings
import re

class TestBM25Retriever(RetrieverStrategy):

    def preprocess_query(self, query: str) -> str:
        # "채권이 뭐야?" → "채권"
        query = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", query)  # 특수문자 제거
        query = re.sub(r"\b(뭐야|알려줘|이란|이게|어때)\b", "", query)  # 자주 쓰는 질문형 조사 제거
        return query.strip()
    

    def is_text_clean(self, text: str, query_keywords: list[str]) -> bool:
        # 공백 제거한 실제 텍스트 길이
        clean_text_len = len(re.sub(r"\s+", "", text))

        # 특수문자 찾기 (한글, 영문, 숫자, 공백 제외)
        special_chars = re.findall(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", text)
        special_char_count = len(special_chars)

        # 디버깅용 출력
        if special_char_count / max(clean_text_len, 1) >= 0.2:
            print("🚫 특수문자 비율 높음:", round(special_char_count / clean_text_len, 2), "| 내용:", text[:50])
            return False


        # 질의 키워드가 포함되어 있지 않으면 제거
        if not any(keyword in text for keyword in query_keywords):
            return False

        return True

    def post_filter_hits(self, hits: list[dict], query_keywords: list[str], top_k: int = 3) -> list[dict]:
        filtered = [
            hit for hit in hits
            if self.is_text_clean(hit["_source"]["text"], query_keywords)
            ]
        return filtered[:top_k]

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
                        },
                            # 오타 검색 추가 (Fuzzy Matching)
                        {
                            "fuzzy": {
                                "text": {
                                    "value": query_clean,
                                    "fuzziness": "AUTO",
                                    "boost": 0.5  # 낮은 가중치
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 2  # 두 조건 이상 매칭되면 통과
                }
            }
        }

        # 3. 검색 요청
        resp = await es_client.search(index=settings.index_name, body=body)
        
        query_keywords = query_clean.split()
        filtered_hits = self.post_filter_hits(resp["hits"]["hits"], query_keywords, top_k)

        return [
            Hit(
                doc_id=hit["_id"],
                score=hit["_score"],
                source=hit["_source"]["source"],
                text=hit["_source"]["text"]
            )
            for hit in filtered_hits
        ]
