# app/api/qa.py
from fastapi import APIRouter, Query  # 또는 Body 사용
from app.services.llm_qa import answer_question
from app.models.schemas import QAResponse   # ← 스키마 임포트만 남김

router = APIRouter()

@router.get(
    "/",
    response_model=QAResponse,
    summary="검색 기반 QA",
)
async def qa(
    q: str = Query(..., description="사용자 질문"),
    mode: str = Query("dense", description="검색 모드"),
    top_k: int = Query(5, ge=1, le=100, description="청크 개수(1~100)"),
):
    """
    1️⃣ search-service에 질문을 전달해 청크를 가져오고  
    2️⃣ 청크 **내** 정보만으로 답변을 생성합니다.  
    결과가 없으면 `"잘모르겠습니다"`를 반환합니다.
    """
    return await answer_question(q=q, mode=mode, top_k=top_k)
