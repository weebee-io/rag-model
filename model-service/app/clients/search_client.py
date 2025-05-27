# app/clients/search_client.py
import httpx
from app.core.config import settings

async def search(q: str, mode: str = None, top_k: int = None):
    params = {"q": q}
    if mode:
        params["mode"] = mode
    if top_k:
        params["top_k"] = top_k
    async with httpx.AsyncClient() as client:
        resp = await client.get(settings.search_api_url, params=params, timeout=30.0)
        resp.raise_for_status()
        return resp.json().get("hits", [])