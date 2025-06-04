from pydantic import BaseModel, Field
from typing import List, Optional, Dict , Any

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

class QuestionRequest(BaseModel):
    question: str
    
class QuestionResponse(BaseModel):
    answer: str

class Chunk(BaseModel):
    """검색 서비스가 돌려주는 단일 청크 구조"""
    doc_id: str
    score: float
    text: str

class HintRequest(BaseModel):
    question: str
    choices: List[str]

class HintResponse(BaseModel):
    hint: str


# 입력 스키마
class NewsRequest(BaseModel):
    news: str  # 뉴스 기사 전문

# 출력 스키마
class NewsResponse(BaseModel):
    summary: str  # 요약 및 키워드 설명이 포함된 텍스트


# ---- 옛날
class QARequest(BaseModel):
    """(선택) 클라이언트가 보내는 파라미터를 바디로 받는 경우"""
    q: str = Field(..., description="사용자 질문")
    mode: str = Field("dense", description="검색 모드")
    top_k: int = Field(5, ge=1, le=100, description="청크 개수(1~100)")


class QAResponse(BaseModel):
    """/qa 응답 스키마"""
    answer: str = Field(..., description="LLM이 생성한 답변")
    # sources: List[Chunk] = Field(
    #     ..., description="검색해서 사용한 원문 청크"
    # )


class QAChoice(BaseModel):
    question: str
    choices: List[str]

class QAExplanationResponse(BaseModel):
    answer: str
    keywords: List[str]


# 🔸 기능 1: 퀴즈 힌트
class QAChoice(BaseModel):
    question: str
    choices: List[str]


class QAHintResponse(BaseModel):
    keywords: List[str]
    hint: str

