from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    es_host: str
    es_port: int
    index_name: str
    default_search_mode: str
    embedding_model: str
    batch_size: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
