# app/api/v1/routers/search.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.core.config import settings
from app.services.factory import get_retriever
from app.api.v1.schemas import SearchResponse, Hit

router = APIRouter()

@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="사용자 질의"),
    mode: str = Query(settings.default_search_mode, description="dense | bm25 | hybrid"),
    top_k: int = Query(5, ge=1, le=100),
):
    retriever = get_retriever(mode)
    if retriever is None:
        raise HTTPException(status_code=400, detail=f"Unsupported mode: {mode}")
    hits: List[Hit] = await retriever.search(q, top_k)
    return SearchResponse(query=q, mode=mode, hits=hits)
