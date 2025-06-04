from fastapi import FastAPI
# from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_middleware import RequestResponseLoggerMiddleware

from app.api.qa_main import router as qa_router
from app.api.news_main import router as news_router
from app.api.hint_main import router as hint_router



app = FastAPI(title="LLM Chat API")

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 필요시 특정 도메인만 허용 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestResponseLoggerMiddleware)


app.include_router(qa_router, prefix="/api/qa", tags=["QA"])
app.include_router(news_router, prefix="/api/news", tags=["News"])
app.include_router(hint_router, prefix="/api/hint", tags=["Hint"])