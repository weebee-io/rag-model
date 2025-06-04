# app/api/v1/routers/test_search.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.core.config import settings
from app.api.v1.schemas import SearchResponse, Hit

from app.services.test_bm25 import TestBM25Retriever
from app.services.dense import DenseRetriever
from app.services.test_hybrid import TestHybridRetriever

router = APIRouter()

@router.get("", response_model=SearchResponse)
async def test_search(
    q: str = Query(..., description="사용자 질의"),
    mode: str = Query(
        "hybrid",
        enum=["bm25", "dense", "hybrid"],
        description="bm25 | dense | hybrid"
    ),
    top_k: int = Query(5, ge=1, le=100),
):
    if mode == "bm25":
        retriever = TestBM25Retriever()
    elif mode == "dense":
        retriever = DenseRetriever()
    elif mode == "hybrid":
        retriever = TestHybridRetriever()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported mode: {mode}")

    hits: List[Hit] = await retriever.search(q, top_k)
    return SearchResponse(query=q, mode=mode, hits=hits)

test_search_router = router



"""# app/api/v1/routers/search_2.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Literal
from app.core.config import settings
from app.api.v1.schemas import SearchResponse, Hit

# from app.services.factory import get_retriever
from app.services.test_bm25 import TestBM25Retriever
from app.services.dense import DenseRetriever
from app.services.test_hybrid import TestHybridRetriever

router = APIRouter()

@router.get("", response_model=SearchResponse)
async def test_search(
    q: str = Query(..., description="사용자 질의"),
    mode: Literal["bm25_improved", "dense", "hybrid_improved"] = Query("hybrid_improved"),
    top_k: int = Query(5, ge=1, le=100),
):
    # 직접 리트리버 선택
    if mode == "bm25_improved":
        retriever = TestBM25Retriever()
    elif mode == "dense":
        retriever = DenseRetriever()
    elif mode == "hybrid_improved":
        retriever = TestHybridRetriever()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported mode: {mode}")

    hits: List[Hit] = await retriever.search(q, top_k)
    return SearchResponse(query=q, mode=mode, hits=hits)

test_search_router = router  # main.py에서 import할 이름
"""