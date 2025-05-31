from fastapi import APIRouter
from app.models.schemas import (
    QAChoice,
    QAHintResponse,
    NewsRequest,
    NewsSummaryResponse,
)
from app.services.qa_hint import generate_hint
from app.services.news_summary import summarize_news

router = APIRouter()

@router.post("/hint", response_model=QAHintResponse)
async def get_hint(data: QAChoice):
    """
    문제 및 보기 입력 시 금융/경제 키워드에 대한 힌트를 반환합니다.
    힌트는 청크 기반 설명 우선, 없을 경우 LLM 설명으로 보완됩니다.
    """
    return await generate_hint(data.question, data.choices)


@router.post("/news", response_model=NewsSummaryResponse)
async def summarize(data: NewsRequest):
    """
    뉴스 기사 본문을 요약하고, 금융/경제 키워드 개념을 설명합니다.
    키워드 설명은 청크 기반 설명이 우선이며, 없을 경우 LLM으로 보완됩니다.
    """
    return await summarize_news(data.content)
