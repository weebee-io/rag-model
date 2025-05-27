from .base import RetrieverStrategy
from ..clients.elastic import es_client
from ..api.v1.schemas import Hit

class BM25Retriever(RetrieverStrategy):
    async def search(self, query: str, top_k: int):
        body = {
            "size": top_k,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["text^2", "meta.keywords"],
                    "analyzer": "nori_analyzer"
                }
            }
        }
        resp = await es_client.search(index=settings.index_name, body=body)
        return [
            Hit(
                doc_id=hit["_id"],
                score=hit["_score"],
                text=hit["_source"]["text"]
            )
            for hit in resp["hits"]["hits"]
        ]
