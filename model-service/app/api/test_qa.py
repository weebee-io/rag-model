from fastapi import APIRouter
from app.models.schemas import QAChoice, QAExplanationResponse
from app.services.test_qa import answer_with_explanation

router = APIRouter(prefix="/explain", tags=["QA Explanation"])

@router.post("/", response_model=QAExplanationResponse)
async def explain_choice(q: QAChoice):
    result = await answer_with_explanation(question=q.question, choices=q.choices)
    return result
