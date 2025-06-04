from .bm25 import BM25Retriever
from .dense import DenseRetriever
from ..api.v1.schemas import Hit

class HybridRetriever(BM25Retriever, DenseRetriever):
    async def search(self, query: str, top_k: int):
        bm25_hits = await BM25Retriever().search(query, top_k*2)
        dense_hits = await DenseRetriever().search(query, top_k*2)
        # 간단 RRF 예시: 순위 기반 가중 합
        merged = {}
        for rank, h in enumerate(bm25_hits):
            merged.setdefault(h.doc_id, 0.0)
            merged[h.doc_id] += 1.0 / (rank+1)
        for rank, h in enumerate(dense_hits):
            merged.setdefault(h.doc_id, 0.0)
            merged[h.doc_id] += 1.0 / (rank+1)
        # 상위 top_k 선별
        sorted_ids = sorted(merged, key=lambda id_: merged[id_], reverse=True)[:top_k]
        
        all_hits = {}
        for h in bm25_hits + dense_hits:
            all_hits[h.doc_id] = Hit(
                doc_id=h.doc_id,
                score=h.score,
                text=h.text,
                source=getattr(h, "source", "")
            )
        #all_hits = {h.doc_id: h for h in bm25_hits + dense_hits}
        
        return [all_hits[id_] for id_ in sorted_ids]
