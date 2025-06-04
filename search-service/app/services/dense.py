from .base import RetrieverStrategy
from ..clients.elastic import es_client
from transformers import AutoTokenizer, AutoModel
import torch
from ..core.config import settings
from ..api.v1.schemas import Hit

# 모델 로드 (싱글톤으로 앱 시작 시 로드해둘 수도 있음)
tokenizer = AutoTokenizer.from_pretrained(settings.embedding_model)
model = AutoModel.from_pretrained(settings.embedding_model)
model.eval()

class DenseRetriever(RetrieverStrategy):
    async def search(self, query: str, top_k: int):
        # 1) 임베딩 생성
        enc = tokenizer(query, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            vec = model(**enc).pooler_output[0].cpu().numpy().tolist()
        # 2) ES 스크립트 스코어 검색
        body = {
            "size": top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.vec, 'embedding') + 1.0",
                        "params": {"vec": vec}
                    }
                }
            }
        }
        resp = await es_client.search(index=settings.index_name, body=body)
        return [
            Hit(
                doc_id=hit["_id"],
                score=hit["_score"],
                source=hit["_source"]["source"],
                text=hit["_source"]["text"]
            )
            for hit in resp["hits"]["hits"]
        ]
