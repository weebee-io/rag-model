from pydantic import BaseModel, Field
from typing import List, Dict , Any

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

class Chunk(BaseModel):
    """검색 서비스가 돌려주는 단일 청크 구조"""
    doc_id: str
    score: float
    text: str



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