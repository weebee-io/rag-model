# test_bm25 테스트를 위한 hybrid 모델

from .test_bm25 import TestBM25Retriever
from .dense import DenseRetriever
from ..api.v1.schemas import Hit

class TestHybridRetriever(TestBM25Retriever, DenseRetriever):
    async def search(self, query: str, top_k: int):
        bm25_hits = await TestBM25Retriever().search(query, top_k * 2)
        dense_hits = await DenseRetriever().search(query, top_k * 2)

        merged = {}
        for rank, h in enumerate(bm25_hits):
            merged.setdefault(h.doc_id, 0.0)
            merged[h.doc_id] += 1.0 / (rank + 1)
        for rank, h in enumerate(dense_hits):
            merged.setdefault(h.doc_id, 0.0)
            merged[h.doc_id] += 1.0 / (rank + 1)

        sorted_ids = sorted(merged, key=lambda id_: merged[id_], reverse=True)[:top_k]
        all_hits = {h.doc_id: h for h in bm25_hits + dense_hits}
        return [all_hits[id_] for id_ in sorted_ids]
