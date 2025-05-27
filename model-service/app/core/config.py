# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    search_api_url: str
    openai_api_key: str
    llm_model_name: str
    max_context_docs: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()