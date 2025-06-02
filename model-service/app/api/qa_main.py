# app/api/qa.py

from fastapi import APIRouter
from app.services.gpt_model.qa_gpt import answer_question
from app.models.schemas import QuestionResponse, QuestionRequest  # ← 요청 모델 추가

router = APIRouter(
     tags=["QA"],
)

@router.post(
    "/",
    response_model=QuestionResponse,
    summary="gpt 모델을 이용한 질문 응답",
)
async def qa(request: QuestionRequest):
    return await answer_question(question=request.question)
