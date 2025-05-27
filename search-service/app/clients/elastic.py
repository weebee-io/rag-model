# app/clients/elastic.py
from elasticsearch import AsyncElasticsearch
from app.core.config import settings

es_client = AsyncElasticsearch(
    hosts=[{"host": settings.es_host, "port": settings.es_port, "scheme": "http"}],
    timeout=30,
    max_retries=3,
    retry_on_timeout=True,
)
