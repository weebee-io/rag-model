from fastapi import APIRouter
from app.services.gpt_model.news_gpt import generate_summary
from app.models.schemas import NewsRequest, NewsResponse  # ← 요청 모델 추가

router = APIRouter()

@router.post(
    "/",
    response_model=NewsResponse,
    summary="gpt 모델을 이용한 뉴스 요약",
)
async def summarize_news(request: NewsRequest):
    return await generate_summary(news=request.news)
