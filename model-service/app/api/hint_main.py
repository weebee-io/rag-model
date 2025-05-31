from fastapi import APIRouter
from app.services.gpt_model.hint_gpt import generate_hint
from app.models.schemas import HintRequest, HintResponse  # ← 요청 모델 추가

router = APIRouter()

@router.post(
    "/",
    response_model=HintResponse,
    summary="gpt 모델을 이용한 힌트",
)
async def hint(request: HintRequest):
    return await generate_hint(question=request.question, choices=request.choices)
