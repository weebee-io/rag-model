from pydantic import BaseSettings

class Settings(BaseSettings):
    es_host: str
    es_port: int = 9200
    index_name: str
    default_search_mode: str = "dense"
    embedding_model: str
    batch_size: int = 32

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
