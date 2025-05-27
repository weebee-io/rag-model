from fastapi import FastAPI
from .core.config import settings
from .api.v1.routers.search import router as search_router

app = FastAPI(
    title="Finance RAG Search Service",
    version="0.1.0",
)

# 헬스체크
@app.get("/health")
async def health():
    return {"status": "ok"}

# 검색 API v1
app.include_router(search_router, prefix="/v1/search", tags=["search"])
